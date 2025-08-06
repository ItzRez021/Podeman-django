from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.HomePage.as_view(),name='home'),
    path('blog/',views.BlogView.as_view(),name='blog'),
    path('blog-post/<int:pk>/',views.BlogPostView.as_view(),name='blogpost'),
    path('store/',views.StoreView.as_view(),name='store'),
    path('detail/<int:pk>/',views.productdetailView.as_view(),name='detail'),
    path('search/', views.product_search, name='product-search'),
    
    

]