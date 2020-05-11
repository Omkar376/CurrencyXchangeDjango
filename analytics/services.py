# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django_pandas.io import read_frame
from wallet.models import Transaction
from CurrencyXchange.settings import CURRENCIES_NAME_MAPPING
from django.core.mail import EmailMessage

class AnalyticsServices:
    def week_date_range(year, week_num):
    
        start_date = datetime.strptime(f'{year}-W{int(week_num )- 1}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(days=6.9)
        return start_date, end_date

    def get_weekly_analytics(user, year, week_number):
        transactions = Transaction.objects.all()
        transactions = transactions.filter(sender__email=user.email)
        if not transactions:
            response = {"status" : False, "message" : "No transactions found"}
            return response
        start_date, end_date = AnalyticsServices.week_date_range(year, week_number)       
        transactions = transactions.filter(timestamp__gte=start_date).filter( timestamp__lte=end_date)
        if not len(transactions)>0:
            return {}
        transactions_df = read_frame(transactions)

        transactions_df["date"] = transactions_df.apply(lambda t: t["timestamp"].strftime('%Y-%m-%d'), axis=1)
        transactions_df["sender_amount"] = transactions_df.apply(lambda t: int(t["sender_amount"]), axis=1)
        transactions_df = transactions_df[["sender_amount_currency","sender_amount" , "date"]]
        print(transactions_df)
        transactions_df = transactions_df.groupby(["sender_amount_currency", "date"]).mean().reset_index()
        transactions_df = transactions_df.rename(columns={'sender_amount_currency':'currency', 
                                        "sender_amount" : "average_amount"}) 
        transactions_df["average_amount"] = transactions_df.apply(lambda t: int(t["average_amount"]), axis=1)

        analysis = {"analysis_list": transactions_df.to_dict("records")}
        return analysis
    
    def get_transaction_analysis(user, start_date):
        analysis = {}
        transactions = Transaction.objects.all()
        transactions = transactions.filter(sender__email=user.email)
        if not transactions:
            response = {"status" : False, "message" : "No transactions found"}
            return response
        transactions = transactions.filter(timestamp__gte=start_date)
        if not len(transactions)>0:
            return {}
        transactions_df = read_frame(transactions)

        transactions_df["date"] = transactions_df.apply(lambda t: t["timestamp"].strftime('%Y-%m-%d'), axis=1)
        transactions_df["sender_amount"] = transactions_df.apply(lambda t: int(t["sender_amount"]), axis=1)
        transactions_df["receiver_amount"] = transactions_df.apply(lambda t: int(t["receiver_amount"]), axis=1)
        from wallet.services import CurrencyServices

        def convert(t):
            print(t)
            amount = CurrencyServices.convert_currency(t["sender_amount"], CURRENCIES_NAME_MAPPING.get(t["sender_amount_currency"]), 
                                                      CURRENCIES_NAME_MAPPING.get( t["receiver_amount_currency"]), "latest")
            print(amount)
            return amount
        
        transactions_df["current_amount"] = transactions_df.apply(lambda t:convert(t), axis =1)
        transactions_df["diff"] = transactions_df.apply(lambda t: t["receiver_amount"] - t["current_amount"], axis =1)
        total = sum(transactions_df["diff"])
        if total > 0:
            analysis = {"status": "Profit", "amount":total}
        elif total == 0:
            analysis = {"status": "No Profit or Loss", "amount": 0}
        else:
            analysis = {"status": "Loss", "amount": abs(total)}
        return analysis
    
class EmailService:
    def sendTransactionEmail(to_email, message ,file):
        msg = EmailMessage('Transaction Report', message, "omkar.gulave123@gmail.com", [to_email])
        msg.content_subtype = "html"  
        msg.attach_file(file)
        msg.send() 


