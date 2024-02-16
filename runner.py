
import schedule
import time
 
def job():
    exec(open('run.py').read()) 

schedule.every(1).minutes.do(job) 
 
while True:
    schedule.run_pending()
    time.sleep(2) 