from read_email_schedule_task import execute
import schedule
import time
import streamlit as st

st.set_page_config(layout='wide')
schedule.every().day.at("05:30").do(execute)

while True:
    st.markdown("Job in process...")
    schedule.run_pending()
    st.markdown("Job done!")
    time.sleep(86400)


# if __name__ == "__main__":
#     exec()