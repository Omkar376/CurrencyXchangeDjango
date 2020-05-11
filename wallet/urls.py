# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'currencys', views.CurrencyList)
router.register(r'transactions', views.AllTransactionView)

router.register(r'walletlist', views.WalletList)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('createtransactions/', views.TransactionDetails.as_view()),
    path('wallets', views.WalletDetails.as_view()),
    path('convert_currency', views.WalletDetails.as_view())
]
