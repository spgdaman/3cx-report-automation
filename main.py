import flask

from read_email_schedule_task import execute
import schedule
import time

app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def hello():

    schedule.every().day.at("05:30").do(execute)

    while True:
        print("Job in process...")
        schedule.run_pending()
        print("Job done!")
        time.sleep(86400)


if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8001, debug=True)