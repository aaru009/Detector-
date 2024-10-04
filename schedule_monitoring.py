# scripts/schedule_monitoring.py

import schedule
import time
from run_real_time_monitoring import monitor_youtube

def job():
    print("Running scheduled monitoring...")
    # Here, you can call your monitoring functions or any other tasks
    monitor_youtube()

# Schedule the job every 1 minute
schedule.every(10).minutes.do(job)

if __name__ == "__main__":
    print("Starting scheduled monitoring...")

    while True:
        schedule.run_pending()
        time.sleep(1)