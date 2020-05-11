from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import CurrencySerializer, TransactionSerializer, TransactionDetailsSerializers, WalletSerializer
from .models import Currency, Transaction, Wallet
from .services import CurrencyServices, WalletServices, EmailTransactionDetails

# Create your views here.
class TransactionDetails(APIView):
    #Token Authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    #Post Request
    def post(self, request, format=None): 
        
        transaction_details = TransactionDetailsSerializers.transaction_serializer(request)
        transaction         = transaction_details.get("transaction")
        
        #Debit amount from Send
        sender_debit_status = WalletServices.debit_wallet(user=transaction.sender, amount=transaction.sender_amount, 
                                                          currency=transaction.sender_amount_currency)
        if not sender_debit_status.get("status"):
            debit_failed_status = {"status" : False, "error" : "Debit failed"}
            return Response(debit_failed_status, status=status.HTTP_501_NOT_IMPLEMENTED)
        
        #Credit amount to receiver
        receiver_credit_status = WalletServices.credit_wallet(user=transaction.receiver, amount=transaction.receiver_amount, 
                                                             currency=transaction.receiver_amount_currency)
        if not sender_debit_status.get("status"):
            WalletServices.credit_wallet(user=transaction.sender, amount=transaction.sender_amount, 
                                                             currency=transaction.sender_amount_currency)
            sender_debit_status = {"status" : False, "error" : "Credit failed"}
            return Response(receiver_credit_status, status=status.HTTP_501_NOT_IMPLEMENTED)
        
        #Save transaction
        transaction.save()
        EmailTransactionDetails.send_transaction_email(transaction)
        transaction_details.pop("transaction") if "transaction" in transaction_details else next
        
        return Response(transaction_details, status=status.HTTP_201_CREATED)
    
        
class WalletDetails(APIView):
    #Token Authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    #Get request
    def get(self, request, format=None):
        #Get Wallet
        currency = request.GET.get('currency')
        wallet = WalletServices.get_wallet(request.user, currency)
        wallet_response = WalletSerializer(wallet, many=True)
        
        return Response(wallet_response.data, status=status.HTTP_200_OK)
    
    #Put req
    def put(self, request, format=None):
        #Update Wallet
        amount = request.data.get("amount")
        currency =  request.data.get("amount_currency")
        if not amount and not amount > 0:
            response_status = {"status" : False, "error" : "Please enter a valid amount value"}
            return Response(response_status, status=status.HTTP_501_NOT_IMPLEMENTED)
        response_status = WalletServices.update_wallet(user=request.user, amount=amount, currency=currency)
        
        return Response(response_status, status=status.HTTP_200_OK)
    
    #Post req to create wallet
    def post(self, request, format=None):
        #Create Wallet
        currency =  request.data.get("amount_currency")
        wallet = WalletServices.get_wallet(request.user, currency)
        if wallet:
            response_status = {"status" : False, "error" : "Wallet already created, use update method."}
            return Response(response_status, status=status.HTTP_501_NOT_IMPLEMENTED)
        amount = request.data.get("amount")
        currency =  request.data.get("amount_currency")
        if not amount and not amount > 0:
            response_status = {"status" : False, "error" : "Please enter a valid amount value"}
            return Response(response_status, status=status.HTTP_501_NOT_IMPLEMENTED)
        response_status = WalletServices.create_wallet(user=request.user, amount=amount, currency=currency)
        
        return Response(response_status, status=status.HTTP_200_OK)
    
class CurrencyConversion(APIView):
    #Token Authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    #Post Request
    def post(self, request, format=None):
        amount =  request.data.get("amount")
        currency =  request.data.get("from_currency")
        convert_to_currency = request.data.get("to_currency")
        date =  request.data.get("date", "latest")
        converted_amount = CurrencyServices.convert_currency(amount, currency, convert_to_currency, date)
        response = {}
        response["converted_amount"] = converted_amount
        response["converted_currency"] = convert_to_currency
        return Response(response, status=status.HTTP_200_OK)
        
#Model Set View for Models Currency Wallet, Transaction     
class CurrencyList(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Currency.objects.all().order_by('name')
    serializer_class = CurrencySerializer
    
class AllTransactionView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
class TransactionList(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
class WalletList(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
