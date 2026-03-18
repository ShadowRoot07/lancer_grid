from django.urls import path
from .views import (
    JobListView, 
    JobDetailView, 
    JobCreateView, 
    BidCreateView, 
    AcceptBidView
)

urlpatterns = [
    path('', JobListView.as_view(), name='job_list'),
    path('job/new/', JobCreateView.as_view(), name='job_create'),
    path('job/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('job/<int:job_id>/bid/', BidCreateView.as_view(), name='bid_create'),
    path('bid/<int:bid_id>/accept/', AcceptBidView.as_view(), name='accept_bid'),
]
