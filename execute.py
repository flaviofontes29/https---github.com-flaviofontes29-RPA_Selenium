import time
import schedule
from main import main

schedule.every(1).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)