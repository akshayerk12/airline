from django.urls import path
from . import views
from django.contrib import admin

urlpatterns=[
    path('',views.Welcome,name='Welcome'),
    path('review',views.Review,name='review'),
    path('suggest',views.Suggest,name='suggest'),
    path('recommend',views.Recommend,name='recommend'),
    path("reviewadder",views.ReviewAdder,name='reviewadder'),
    path('admin/',admin.site.urls)
]