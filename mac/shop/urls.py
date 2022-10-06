
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index,name="ShopHome"),
    path('about/', views.about,name="AboutUs"),
    path('contact/', views.contact,name="ContactUs"),
    path('track/', views.track,name="Tracking"),
    path('search/', views.search,name="Search"),
    path('checkout/', views.checkout,name="checkout"),
    path('products/<int:myid>', views.productView,name="productview"),
] 