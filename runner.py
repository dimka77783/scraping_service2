
import schedule
import time
 
def job():
    exec(open('send.py').read()) 

schedule.every(1).minutes.do(job) 
 
while True:
    schedule.run_pending()
    time.slep(1) 