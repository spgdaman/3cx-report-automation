import pandas as pd
import csv
from datetime import datetime
import time 

read_file = pd.read_csv('Data.csv')
read_file.to_csv('CallVolume.csv', index=None, header=True)

def clean_data():
    with open("CallVolumes.csv","w+", newline='') as cdr2: # Final file with cleaned data
        collection = []
        data2 = csv.writer(cdr2, delimiter=',')

        with open('CallVolume.csv') as cdr: # Raw file with uncleaned data
            data = csv.reader(cdr)
            line_count = 0
            for row in data:
                if line_count <5:
                    line_count += 1
                else:
                    collection.append(row)
                    line_count += 1

        counter = 0

        for items in collection:
            if items[0] != '':
                data2.writerow(items)
                counter += 1
            elif items[0] == '': # Fills in the gaps with dates from row above it
                item = items
                item[0] = collection[counter-1][0]
                data2.writerow(item)
                counter += 1
        # print(collection[1])

        counts = len(collection[1:])

        print(f"Your data contains {counts} rows")

    df = pd.read_csv('CallVolumes.csv')
    df2 = pd.DataFrame(df)
    del df2['Unnamed: 2']
    del df2['Totals']
    del df2['Cost']
    df2 = df2.drop(df2.index[[len(df2)-1,len(df2)-2]])
    df2.rename(columns = {'Play':'Totals'}, inplace=True)
    # df2['Call Time'] = df2['Call Time'].astype('datetime64[ns]')
    # df2['Call Time'] = pd.to_datetime(df2['Call Time'], infer_datetime_format=True)
    df2['Caller ID'] = df2['Caller ID'].apply(str)

    # print(df2)
    # print(df2.dtypes)

    # numbers = ["0","1","2","3","4","5","6","7","8","9"]
    num_count = 0
    index = list(df2.index.values.tolist()) 

    x = 0
    df_items = [x for x in df2['Caller ID']]
    df_items_2 = [x for x in df2['Destination']]
    new_df_items = list()
    new_df_items_2 = list()

    for items in df_items:
        if items[0] == '2' or items[0] == 2:
            items = '+' + items
            new_df_items.append(items)
        elif items[0] == '7' or items[0] == 7:
            items = '+254' + items
            new_df_items.append(items)
        else:
            new_df_items.append(items)

    for items in df_items_2:
        if items[0] == '2' or items[0] == 2:
            items = '+' + items
            new_df_items_2.append(items)
        elif items[0] == '7' or items[0] == 7:
            items = '+254' + items
            new_df_items_2.append(items)
        else:
            new_df_items_2.append(items)

    df2['Caller ID'] = new_df_items
    df2['Destination'] = new_df_items_2
    # print(x[0][0])

    df3 = df2

    df3['CallTime'] = df3['Call Time']
    
    df3['CallTime'] = df3['CallTime'].to_string()

    print(len(df3['CallTime']))


    """
        This section formats the date and time correctly, and does error handling.
    """

    try: 
        df3[['Date','Time','AM/PM']] = df3['Call Time'].str.split(' ', expand=True)

        standard_dates = []

        for dates in df3['Date']:
            if dates[4:5] == "-":
                new_dates = f"{dates[9:10]}/{dates[5:7]}/{dates[:4]}"
                standard_dates.append(new_dates)
            else:
                new_dates = f"{dates}"
                standard_dates.append(new_dates)
        
        df3['Date'] = standard_dates

        standard_time = []
        
        zipped = zip(df3['Time'],df3["AM/PM"])

        for times, meridiem in zipped:
            suffixes = datetime.strptime(times,"%H:%M:%S").strftime("%I:%M:%S %p")[-2:]
            if meridiem == None:
                new_time = datetime.strptime(times,"%H:%M:%S").strftime("%I:%M:%S %p")
                standard_time.append(new_time)
            else:
                new_time = times + " " + meridiem
                standard_time.append(new_time)

        df3['Time'] = standard_time
        
        del df3['CallTime']
        del df3['AM/PM']
        del standard_dates
        del standard_time

    # The except clause does the same as above, without splitting the column into 3

    except:
        df3[['Date','Time']] = df3['Call Time'].str.split(' ', expand=True)
        standard_dates = []

        for dates in df3['Date']:
            if dates[4:5] == "-":
                new_dates = f"{dates[9:10]}/{dates[5:7]}/{dates[:4]}"
                standard_dates.append(new_dates)
            else:
                new_dates = f"{dates}"
                standard_dates.append(new_dates)
        
        df3['Date'] = standard_dates
        # df3['Date'] = pd.to_datetime(df3['Date'], format='%m/%d/%Y')

        standard_time = []
        
        zipped = zip(df3['Time'],df3["Time"])

        for times, meridiem in zipped:
            suffixes = datetime.strptime(times,"%H:%M:%S").strftime("%I:%M:%S %p")[-2:]
            if meridiem == None:
                new_time = datetime.strptime(times,"%H:%M:%S").strftime("%I:%M:%S %p")
                standard_time.append(new_time)
            else:
                new_time = times + " " + meridiem
                standard_time.append(new_time)

        df3['Time'] = standard_time
        
        del df3['CallTime']
        del standard_dates
        del standard_time

    """
        The end of the date formatting section and error handling
    """  

    df3['Call Time'] = pd.to_datetime(df3.Date.astype(str)+' '+df3.Time.astype(str))

    # datetime.strptime(df3['Call Time'], "%Y/%m/%d %H:%M:%S %p")

    del df3['Date']
    del df3['Time']
    

    df3[['Call Time','Caller ID','Destination','Status','Ringing','Talking','Reason','Totals']].to_csv("CallVolumes.csv", index=False)
    del df2
    print(df3)
    del df3

    

    #df3['Date'] = pd.to_datetime(pd.to_datetime(df3['Date'], format='%m/%d/%Y'), format='%d/%m/%Y')
    # df3['Time'] = pd.to_datetime(df3['Time'], format='%H:%M:%S') - pd.to_datetime('1900-01-01 00:00:00', format = '%Y/%m/%d %H:%M:%S' )
    
    # pd.to_datetime(df3['Date'], format='%d/%m/%Y')
    #pd.to_datetime(df3['Time'], format = '%H:%M:%S')
    # df3['Time'].to_string()
    #print(df3[['Date','Time','AMPM']])
    # df3[['Date','Time','AMPM']]

    # time = df3['Time'][0]
    # print(datetime.strptime(time,"%H:%M:%S").strftime("%I:%M:%S %P"))

if __name__ == "__main__":
    clean_data()
