from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .job import let_scrape
from frontpage.models import DoneSummary
import random


# def myjob():
# 	ApaAja.objects.create(name=f'jaran{random.randint(1, 100000)}')

# 	print(ApaAja.objects.all())
# 	print(f'hello {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')

def start():
  scheduler = BackgroundScheduler(timezone="Asia/Jakarta")
  scheduler.add_job(let_scrape, 'cron', minute='*/2')
  # scheduler.add_job(let_scrape, 'cron', minute='*/5', hour="9-14")
  scheduler.start()



# scheduler.add_job(
#    myjob,
#    'date',
#    id=id_value,
#    jobstore="default",
#    run_date=scheduler_date,
#    replace_existing=True
# )