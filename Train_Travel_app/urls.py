from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('PrecticeWebsiteAbout',views.about,name='about'),
    path('PrecticeWebsitePNRStatus',views.PNR,name='PNR-Status'),
    path('PrecticeWebsiteContects',views.contects,name='contects'),
    path('PrecticeWebsiteRegister',views.register, name="register"),
    path('success', views.success, name='success'),
    path('PrecticeWebsitePNRStatus1',views.PNR1,name='PNR-Status1'),
    path('PrecticeWebsiteHome1',views.HomeFindTrain,name='HomeFindTrain'),
    path('fetch-pnr-status/', views.fetch_pnr_status, name='fetch_pnr_status'),
    path('live-train-status', views.live_train_status, name='live_train_status'),
    path('train-info/', views.fetch_train_info, name='fetch_train_info'),
    path('train-details/', views.train_details, name='train_details'),
    path('register/', views.register, name='register'),
    path('register/success/', views.success, name='success'),
    path('find-trains/', views.find_trains, name='HomeFindTrain'),
    path('train-details/<str:train_number>/', views.train_details, name='train_details'),
]