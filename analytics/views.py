from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import AnalyticsServices
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class WeeklyAnalyticsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request): 
        try:
            year = int(request.GET.get('year'))
            week_number = int(request.GET.get('week_number'))            
            analysis = AnalyticsServices.get_weekly_analytics(request.user, year, week_number)
            return Response(analysis, status=status.HTTP_200_OK)
        except Exception as error:
            response = {"error": str(error) }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class TransactionAnalytics(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            start_date = request.GET.get('start_date')
            if not start_date:
                response = {"error": "Start date not provided"}
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            analysis = AnalyticsServices.get_transaction_analysis(request.user, start_date)
            return Response(analysis, status=status.HTTP_200_OK)
            
        except Exception as error:
            response = {"error": str(error) }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)