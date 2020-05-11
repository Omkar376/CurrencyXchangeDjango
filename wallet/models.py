from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
#Currency Database Model 
class Currency(models.Model):
    name    = models.CharField(max_length=60)
    code    = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    logo    = models.ImageField(upload_to='images/currency', default ='')
    
    def __str__(self):
        return self.name
    
#Wallet Database Model    
class Wallet(models.Model):
    
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency="INR")
    
#Transaction Database Model    
class Transaction(models.Model):
    
    sender          = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sender')
    sender_amount   = MoneyField(max_digits=14, decimal_places=2, default_currency="INR") 
    receiver        = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='receiver')
    receiver_amount = MoneyField(max_digits=14, decimal_places=2, default_currency="INR")
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
