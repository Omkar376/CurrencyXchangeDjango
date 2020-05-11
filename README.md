# CurrencyXchangeDjango
A Django Project for Currency Exchange, Wallet and much more... 


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
