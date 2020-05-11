# -*- coding: utf-8 -*-
from datetime import datetime
from wallet.models import Transaction
from django_pandas.io import read_frame
from .report import Report
from .services import EmailService
from CurrencyXchange.settings import CURRENCIES_NAME_MAPPING

def MonthlyReport():
    month_start_date = datetime.today().replace(day=1)
    end_start_date = datetime.today()
    transactions = Transaction.objects.all()
    if not transactions:
        response = {"status" : False, "message" : "No transactions found"}
        return response
    transactions = transactions.filter(timestamp__gte=month_start_date)
    
    transactions_df = read_frame(transactions)   
    text = "Transaction Report (" + str(month_start_date.date()) + " - " + str(end_start_date.date()) + ")"      
    transactions_df["Debited Amount"] = transactions_df.apply(lambda t: str(t["sender_amount"]) + " " + CURRENCIES_NAME_MAPPING[t["sender_amount_currency"]], axis=1)
    transactions_df["Credited Amount"] = transactions_df.apply(lambda t: str(t["receiver_amount"]) + " " +CURRENCIES_NAME_MAPPING[t["receiver_amount_currency"]], axis=1)
    transactions_df["date"] = transactions_df.apply(lambda t: t["timestamp"].strftime('%Y-%m-%d'), axis=1)
    transactions_df = transactions_df[["sender", "Debited Amount", "receiver", "Credited Amount", "date"]]
    transactions_df = transactions_df.rename(columns={'receiver':'Credited Account', "date" : "Date"})
    sender_list = list(set(transactions_df["sender"]))
    for sender in sender_list:
        temp_transactiondf = transactions_df[transactions_df["sender"] == sender]
        temp_transactiondf = temp_transactiondf[["Date", "Credited Account", "Debited Amount", "Credited Amount" ]]
        file = Report.generate_report(sender, text, temp_transactiondf)
        EmailService.sendTransactionEmail(sender, "Email", file)
    
        