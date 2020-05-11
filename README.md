# CurrencyXchangeDjango
A Django Project for Currency Exchange, Wallet and Analytics..

## Getting Started


```
git clone https://github.com/Omkar376/CurrencyXchangeDjango.git
```

API List
Register User 
    method : POST
    url : http://localhost:8000/rest-auth/registration/
      {
        "email" : "user0376@gmail.com",
        "password1" : "user0376",
        "password2" : "user0376",
        "first_name" : "User0376",
        "last_name" : "UserLastName0376"

      }
Login User
    method : POST
    url : http://localhost:8000/rest-auth/login/
    {
      "email" : "user0376@gmail.com",
      "password" : "user0376"
    }
    
Create Wallet:
    url : http://localhost:8000/wallets
        {
          "amount" : 10000,
          "amount_currency" : "INR"
        }
        
Update Wallet:
    url : http://localhost:8000/wallets
        {
          "amount" : 10000,
          "amount_currency" : "INR"
        }
Get Wallet Balance:
  url : http://localhost:8000/wallets
[
    {
        "id": 7,
        "user": "user0376@gmail.com",
        "amount": "20000.00",
        "amount_currency": "INR"
    },
    {
        "id": 8,
        "user": "user0376@gmail.com",
        "amount": "2000.00",
        "amount_currency": "USD"
    },
    {
        "id": 9,
        "user": "user0376@gmail.com",
        "amount": "2000.00",
        "amount_currency": "EUR"
    }
]

Convert Currency:
url : http://localhost:8000/convert_currency
body: {
	"amount": 20000,
	"from_currency" :"INR",
	"to_currency" : "USD"
}
response : {
    "converted_amount": 263.691288,
    "converted_currency": "USD"
}

Create transaction:
http://127.0.0.1:8000/createtransactions/
{		
	"receiver_email": "omkar.gulave123@gmail.com",
        "sender_amount": 3000,
        "sender_amount_currency": "INR",
        "receiver_amount_currency": "USD"
}

Weekly Report:
http://127.0.0.1:8000/analytics/weekly?year=2020&week_number=20
{
    "analysis_list": [
        {
            "currency": "Indian Rupee",
            "date": "2020-05-11",
            "average_amount": 3000
        }
    ]
}

Profit/Loss Report 
http://127.0.0.1:8000/analytics/analytics?start_date=2020-05-01
{
    "status": "Profit",
    "amount": 100
}
