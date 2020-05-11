# -*- coding: utf-8 -*-
from django.urls import path
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('weekly', views.WeeklyAnalyticsView.as_view()),
    
    path('analytics', views.TransactionAnalytics.as_view())
]

from . import scheduler_execute