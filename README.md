# CurrencyXchangeDjango
A Django Project for Currency Exchange, Wallet and Analytics. The Project has three Apps as below
```
1. users
	Models : Users
	Functionality : A custom user model to store data of the logged in user.
	
2. wallet
	Models : Wallet, Currency, Transaction
	Functionality : Create, Update Wallet, Transfer Money from one wallet to another.
	
3. analytics
	Models : None
	Functionality:  Monthly Scheduler, Weekly Report generation and Email Services.
```		

## Getting Started
Follow below instructions to run the django app.
### Clone Repository
```
git clone https://github.com/Omkar376/CurrencyXchangeDjango.git
```
### Installing

Use AnacondaPrompt any other commandline control with python installed. Create a virtual env for ou project.

```
pip install virtualenv
virtualenv env
env\Scripts\activate
```

Open the project directory and install the required library from requirments.txt

```
cd {ProjectDirectory}
pip install requirements.txt
```

## Start Django REST framework project server

Start django rest framework project using below command:
```
python manage.py runserver
```

## Test using Postman

Find the Collection of Postman requests "CurrencyXchangeTesting.postman_collection.json" in Code repository 

## Assumption

Below are some assumptions and settings implemented in this project:

### Background Scheduler

A Monthly Transaction Report is generated and an Email is sent for the same to all users on last Friday of the month

### Currencies Configured

This project is configured for 10 Currencies around the world. Currency can be added as below in setting.py file.


For converison of currency {CURRENCY_EXCHANGE_API_URL} end point is used.

```
/settings.py
.

#Currency Conversion API
CURRENCY_EXCHANGE_API_URL = "https://api.exchangeratesapi.io/"

#Add the currency code in {CURRENCIES}
CURRENCIES = ('USD', 'INR', "EUR" ,"JPY", "GBP", "AUD", "CAD", "CHF", "SEK", "NZD")

#Add the corresponding currency name with code in {CURRENCIES_NAME_MAPPING} (NAME : CODE)
CURRENCIES_NAME_MAPPING = {  'US Dollar': 'USD',
                             'Indian Rupee': 'INR',
                             'EURO': 'EUR',
                             'Yen': 'JPY',
                             'Pound Sterling': 'GBP',
                             'Australian Dollar': 'AUD',
                             'Canadian Dollar': 'CAD',
                             'Swiss Franc': 'CHF',
                             'New Zealand Dollar': 'NZD',
                             'Chinese renminbi': 'CNH',
                             'Swedish Krona': 'SEK' }

....
```
### Analytics

1. Weekly Average Amount transferred is the mean of all transaction of each currency of the logged in user.
2. Profit/Loss is for every sender and receiver currency type pair, for a particular pair it is the mean of the diff of the recevier amount at time of transaction and amount that would be current amount if the transaction occurs now for all transactions.
 ```
 {
        "sender_amount_currency": "Indian Rupee",
        "receiver_amount_currency": "US Dollar",
        "diff": -0.5536931999999979,
        "status": "Loss"
 }
```

## Reports and Emails

Monthly report of all transactions and after every successfull transaction an email received by Sender and Receiver of the transaction.

Format of Report:

![alt text](https://github.com/Omkar376/CurrencyXchangeDjango/blob/master/images/SampleReport.JPG)

## API List
```
# Currency Conversion API

CURRENCY_EXCHANGE_API_URL = "https://api.exchangeratesapi.io/"

1. Register User 
	    Method : POST
	    URL : http://localhost:8000/rest-auth/registration/
	    Request Body :    {
				"email" : "user0376@gmail.com",
				"password1" : "user0376",
				"password2" : "user0376",
				"first_name" : "User0376",
				"last_name" : "UserLastName0376"
			      }

2. Login User
	    Method : POST
	    URL : http://localhost:8000/rest-auth/login/
	    Request Body : {
			      "email" : "user0376@gmail.com",
			      "password" : "user0376"
			    }
    
3. Create Wallet:
	    Method : POST
	    URL : http://localhost:8000/wallets
	    Request Body : {
			  "amount" : 10000,
			  "amount_currency" : "INR"
			   }
        
4. Update Wallet:
	    Method : PUT
	    URL : http://localhost:8000/wallets
	    Request Body :    {
		  "amount" : 10000,
		  "amount_currency" : "INR"
		}
	
5. Get Wallet Balance:
	  Method : GET
	  URL : http://localhost:8000/wallets
	  Response:
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

6. Convert Currency:
	Method : POST
	URL : http://localhost:8000/convert_currency
	Request Body: {
			"amount": 20000,
			"from_currency" :"INR",
			"to_currency" : "USD"
		      }
	Response : {
	    "converted_amount": 263.691288,
	    "converted_currency": "USD"
	}

7. Create transaction:
	Method : POST
	URL: http://127.0.0.1:8000/createtransactions/
	Request Body:{		
		"receiver_email": "omkar.gulave123@gmail.com",
		"sender_amount": 3000,
		"sender_amount_currency": "INR",
		"receiver_amount_currency": "USD"
	}

8. Weekly Report:
	Method : GET
	URL: http://127.0.0.1:8000/analytics/weekly?year=2020&week_number=20
	Query Params : week_number is nth week of year for example year=2020&week_number=20 
				start date: 5/11/2020 12:00 AM and end date 5/17/2020 9:36 PM
	Response:  {
		    "analysis_list": [
					{
					    "currency": "Indian Rupee",
					    "date": "2020-05-11",
					    "average_amount": 3000
					}
				     ]
		   }

9. Profit/Loss Report 
	Method : GET
	URL: http://127.0.0.1:8000/analytics/analytics?start_date=2020-05-01
	Response: {
			"sender_amount_currency": "Indian Rupee",
			"receiver_amount_currency": "US Dollar",
			"diff": -0.55,
			"status": "Loss"
		 }
		
10. Upload User profile image:
	Method : POST
	URL : http://localhost:8000/rest-auth/user/
	Request Body:{		
		"profile_image": Profile File
		}
