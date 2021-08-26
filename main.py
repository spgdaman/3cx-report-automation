import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type as guess_mime_type

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'simon.waigi@gmail.com'

def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service
service = gmail_authenticate()

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    else:
        print("did not find what you are looking for")
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

search_results = search_messages(service, "3cx")
search_results

import os

import requests,json
import pandas as pd

first_email_search_result_id = search_results[0]

# utility functions
def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def parse_parts(service, parts):
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
            # elif mimeType == "text/html":
            #     # if the email part is an HTML content
            #     # save the HTML file and optionally open it in the browser
            #     if not filename:
            #         filename = "index.html"
            #     filepath = os.path.join(folder_name, filename)
            #     print("Saving HTML to", filepath)
            #     with open(filepath, "wb") as f:
            #         f.write(urlsafe_b64decode(data))
            # else:
            #     # attachment other than a plain text or HTML
            #     for part_header in part_headers:
            #         part_header_name = part_header.get("name")
            #         part_header_value = part_header.get("value")
            #         if part_header_name == "Content-Disposition":
            #             if "attachment" in part_header_value:
            #                 # we get the attachment ID 
            #                 # and make another request to get the attachment itself
            #                 print("Saving the file:", filename, "size:", get_size_format(file_size))
            #                 attachment_id = body.get("attachmentId")
            #                 attachment = service.users().messages() \
            #                             .attachments().get(id=attachment_id, userId='me', messageId=msg['id']).execute()
            #                 data = attachment.get("data")
            #                 filepath = os.path.join(folder_name, filename)
            #                 if data:
            #                     with open(filepath, "wb") as f:
            #                         f.write(urlsafe_b64decode(data))


def read_message(service, message_id):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message_id['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    body = payload.get("body")
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            if name.lower() == "subject":
                # make a directory with the name of the subject
                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
            
    parse_parts(service, parts)

    data = body['data']
    data = data.replace("-","+").replace("_","/")

    import base64
    from bs4 import BeautifulSoup
    decoded_data = base64.b64decode(data)

    # Now, the data obtained is in lxml. So, we will parse
    # it with BeautifulSoup library
    soup = BeautifulSoup(decoded_data, features="html.parser")
    body = soup.body()
    # print(soup.prettify())
    html = list(soup.children)[3]
    # print(html)
    body = list(html.children)[3]
    # print(body)
    body_tags = list(body.children)[1]
    # print(body_tags)
    table = list(body_tags.children)[1]
    # print(table)
    table_body = list(table.children)[1]
    # print(table_body)
    table_row = list(table_body.children)[1]
    # print(table_row)
    table_d = list(table_row.children)[1]
    # print(table_d)
    div = list(table_d.children)[1]
    # print(div)
    p = list(div.children)[3]
    # print(p)
    a = list(p.children)[1]
    # print(a)

    del html
    del body
    del body_tags
    del table
    del table_body
    del table_row
    del table_d
    del div
    del p

    a = str(a)
    a = a.replace('<a href="',"")
    a = a.replace('" target="_blank">here</a>',"")
    print(a)
    
    print("="*50)
    return(a)

def dispatch_data():
    link = read_message(service, first_email_search_result_id)

    call_records = requests.get(link).content
    open('Data.csv', 'wb').write(call_records)

    # data = pd.read_excel(call_records)
    # data.to_excel("CallVolume.xlsx")

    # read_file = pd.read_excel('CallVolume.xlsx')
    # print(read_file)

    from revamp import clean_data
    clean_data()

    # Read the main file
    # df1 = pd.read_csv('Call_Volumes.csv', low_memory=False)
    # df2 = pd.read_csv('CallVolumes.csv', low_memory=False)
    # df1 = df1.append(df2)
    # print(df1)
    # df1.to_csv('Call_Volumes.csv', index=False)

    # create a json object to load into bigquery
    data = pd.read_csv('CallVolumes.csv', index_col=False)
    data = data.rename(columns={'Call Time': 'Call_Time', 'Caller ID': 'Caller_ID'})
    data_json = json.loads(data.to_json(orient='table',index=False))

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    table_id = 'businessintelligence-320707.Customer_Service.3cx'

    rows_iter = client.list_rows(table_id)

    rows_to_insert = data_json['data']

    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

# import schedule
# import time

# schedule.every().day.at("05:30").do(execute)

# while True:
#     print("Job in process...")
#     schedule.run_pending()
#     print("Job done!")
#     time.sleep(86400)

from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    last_run = datetime.datetime.now()
    return f'Last run at {last_run}'

@app.route('/execute', methods=["GET"])
def entry_point():
    dispatch_data()
    last_run = datetime.datetime.now()
    return f'Job executed last at {last_run}'

if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="0.0.0.0", debug=True)
