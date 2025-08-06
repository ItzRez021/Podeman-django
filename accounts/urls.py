from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('registercode/',views.UserRegisterCodeView.as_view(),name='registercode'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('profile/<int:pk>/',views.UserProfileView.as_view(),name='profile'),
    path('changeprofile/',views.ProfileUpdateView.as_view(),name='changeprofile'),
    path('changepass/',views.UserChangePassView.as_view(),name='changepass'),
    path('logout/',views.logoutt,name='logout'),
    path('useradress/',views.UserAdressesView.as_view(),name='adress'),
    path('addadress/',views.UserAddAdressView.as_view(),name='addadres'),
    path('deleteadress/<int:id>/',views.UserDeleteAdressView.as_view(),name='deladress'),
    path('Wishlist/<int:id>/',views.UserWishlistView.as_view(),name='wishlist'),
    path('addTowish/<int:id>/',views.UserAddToWishlistView.as_view(),name='addtowish'),
    path('deletewishlist/<int:id>/',views.UserRemoveWishlistView.as_view(),name='delwishlist'),
    path('ChangeEmail/',views.UserChangeEmail.as_view(),name='changeemail'),
    path('ChangeEmailCode/',views.UserChangeEmailCodeView.as_view(),name='changeemailcode'),
    path('cart/add/<int:product_id>/',views.AddToCartView.as_view(), name='addtocart'),
    path('Cart/',views.UserCartView.as_view(),name='cart'),
    path('cart/remove/<int:item_id>/',views.RemoveFromCartView.as_view(),name='remove_from_cart'),
]