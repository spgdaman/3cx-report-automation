from read_email_schedule_task import execute
import schedule
import time

schedule.every().day.at("05:30").do(execute)

while True:
    print("Job in process...")
    schedule.run_pending()
    print("Job done!")
    time.sleep(86400)


# if __name__ == "__main__":
#     exec()