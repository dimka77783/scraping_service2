

import schedule
import time
 
def job():
    exec(open('run.py').read()) 

schedule.every(1).minutes.do(job)

 
