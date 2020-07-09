import schedule
import time
import datetime
import threading
import spider

def job_spider():
    print('spider working')
    spider.main_spider_schedule(bool_add=True)

# def job2():
# 	print('i am working for job2')
# 	time.sleep(2)
# 	print('job2:', datetime.datetime.now())


def job_spider_task():
    threading.Thread(target=job_spider).start()

# def job2_task():
# 	threading.Thread(target=job2).start()


def run():
    schedule.every().day.at("16:30").do(job_spider_task)
    schedule.every().day.at("06:00").do(job_spider_task)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run()