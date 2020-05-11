# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Currency, Wallet, Transaction
from users.models import User
from .services import CurrencyServices

class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'code', 'country', "logo"]
        
        

class WalletSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='email')
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'amount', "amount_currency"]
        

class TransactionDetailsSerializers():
    
    def transaction_serializer(transaction_request):
        transaction_details = {}
        try:
            sender                   = transaction_request.user
            receiver_email           = transaction_request.data.get("receiver_email")
            sender_amount            = transaction_request.data.get("sender_amount")
            sender_amount_currency   = transaction_request.data.get("sender_amount_currency")
            receiver_amount_currency = transaction_request.data.get("receiver_amount_currency")
            receiver_amount          = CurrencyServices.convert_currency(sender_amount, sender_amount_currency, 
                                                                receiver_amount_currency, "latest")
            queryset                 = User.objects.all()
            receiver                 = queryset.filter(email=receiver_email).first()
            
            transaction              = Transaction(sender = sender,
                                            receiver = receiver,
                                            sender_amount = sender_amount,
                                            sender_amount_currency = sender_amount_currency,
                                            receiver_amount = receiver_amount,
                                            receiver_amount_currency = receiver_amount_currency)

            transaction_details = {"is_valid" : True, "transaction" : transaction}
            print(transaction_details)
        except Exception as error:
            transaction_details = {"is_valid" : False, "errors" : str(error), 
                                   "transaction_request" : str(transaction_request.data.get("amount"))}
            print(transaction_details)
        return transaction_details
        
class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    sender = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='email')
    receiver = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='email')
    """
    sender = UserSerializer()
    receiver = UserSerializer()
    """
    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'sender_amount', "sender_amount_currency", "receiver", 
                                      "receiver_amount", "receiver_amount_currency","timestamp"]
        