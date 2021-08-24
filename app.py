from read_email_schedule_task import execute
import schedule
import time

schedule.every().day.at("05:30").do(execute)

while True:
    schedule.run_pending()
    time.sleep(86400)
    print("Job done!")


# if __name__ == "__main__":
#     exec()