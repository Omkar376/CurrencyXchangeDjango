# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)

# jobs
from . import monthly_report

#scheduler.add_job(monthly_report.MonthlyReport, 'interval', seconds=10)
scheduler.add_job(monthly_report.MonthlyReport, 'cron', day='last fri')
scheduler.start()

