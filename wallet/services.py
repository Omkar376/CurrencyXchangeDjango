# -*- coding: utf-8 -*-
from CurrencyXchange import settings
from .models import Wallet
import requests
import pandas as pd
from django_pandas.io import read_frame
from CurrencyXchange.settings import CURRENCIES_NAME_MAPPING
from analytics.report import Report
from analytics.services import EmailService

class CurrencyServices:
    
    def convert_currency(amount, from_currency_code, to_currency_code, date):
        try:
            exchange_url      = settings.CURRENCY_EXCHANGE_API_URL
            exchange_url      = exchange_url + date
            
            params            = {}
            params["base"]    = from_currency_code
            params["symbols"] = to_currency_code
            
            response          = requests.get(exchange_url, params = params)
            conversion_rate   = response.json().get("rates", {}).get(to_currency_code)
            
            if conversion_rate:
                converted_amount  = amount * conversion_rate
                
                return converted_amount
            else:
                return 0
            
        except Exception as error:
            error = str(error)
            return error

class EmailTransactionDetails:
    
    def send_transaction_email(transaction):
        transactions_df = pd.DataFrame(columns=["sender", "receiver", "sender_amount", "sender_amount_currency",
                                               "receiver_amount_currency", "receiver_amount", "timestamp"])
        transactions_df.loc[0] = [transaction.sender, transaction.receiver, transaction.sender_amount, transaction.sender_amount_currency,
                                  transaction.receiver_amount_currency, transaction.receiver_amount, transaction.timestamp ]
        text = "Transaction Report"    
        transactions_df["Debited Amount"] = transactions_df.apply(lambda t: str(t["sender_amount"]) + " " + t["sender_amount_currency"], axis=1)
        transactions_df["Credited Amount"] = transactions_df.apply(lambda t: str(t["receiver_amount"]) + " " + t["receiver_amount_currency"], axis=1)
        transactions_df["date"] = transactions_df.apply(lambda t: t["timestamp"].strftime('%Y-%m-%d'), axis=1)
        transactions_df = transactions_df[["sender", "Debited Amount", "receiver", "Credited Amount", "date"]]
        transactions_df = transactions_df.rename(columns={'receiver':'Credited Account', "date" : "Date", "sender" : "Sender Account"})
        file = Report.generate_report("", text, transactions_df)
        EmailService.sendTransactionEmail(transaction.sender, "Email", file)
        EmailService.sendTransactionEmail(transaction.receiver, "Email", file)
        
class WalletServices:
    
    def get_wallet(user, currency):
        queryset = Wallet.objects.all()
        if currency:
            wallet = queryset.filter(user__email=user.email, amount_currency=currency)
        else:
            wallet = queryset.filter(user__email=user.email)

        return wallet
    
    def create_wallet(user, amount, currency):
        wallet = Wallet(user=user, amount=amount, amount_currency=currency)
        wallet.save()
        return True
    
    def update_wallet(user, amount, currency):
        wallet_not_available = {"status": False, "error" : "Wallet not available"}
        queryset = Wallet.objects.all()
        wallet   = queryset.filter(user__email=user.email, amount_currency=currency)
        success_status = {"status" : True}
        if wallet:
            wallet = wallet.first() 
            wallet.amount = amount
            wallet.save()
            success_status["amount"] = amount
            return success_status
        else:
            return wallet_not_available
    
    def credit_wallet(user, amount, currency):
        
        wallet = WalletServices.get_wallet(user, currency)
        success_status = {"status" : True}
        if wallet:
            wallet = wallet.first()
            wallet.amount += amount
            wallet.save()
            success_status["amount"] = wallet.amount
        else:
            WalletServices.create_wallet(user, amount, currency)
            success_status["amount"] = amount
        return success_status
    
    def debit_wallet(user, amount, currency):
        wallet = WalletServices.get_wallet(user, currency)
        insufficent_balance_status = {"status": False, "error": "Insufficent Balance"}
        success_status = {"status" : True}
        if wallet:
            wallet = wallet.first()
            if wallet.amount > amount:
                wallet.amount -= amount
                wallet.save()
                success_status["wallet"] = wallet.amount
                return success_status
            else:
                return insufficent_balance_status
        else:
            return insufficent_balance_status
            
            
    
            