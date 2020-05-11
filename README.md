# CurrencyXchangeDjango
A Django Project for Currency Exchange, Wallet and Analytics..

## Getting Started
Follow below instructions to run the django app. Also see deployment for notes
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

## Deployment

Start django rest framework project using below command:
```
python manage.py runserver
```

## Test using Postman

Find the Collection of Postman requests "CurrencyXchangeTesting.postman_collection.json" in Code repository 

## API List
```
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
	Response:{
		    "status": "Profit",
		    "amount": 100
		}
		
10. Upload User profile image:
	Method : POST
	URL : http://localhost:8000/rest-auth/user/
	Request Body:{		
		"profile_image": Profile File
		}
