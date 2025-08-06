from django.contrib import admin
from .models import User,Profile,Adresse,Wishlist,Cart,CartItem
from .forms import ChangeUser,CreateUser
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    form = ChangeUser
    add_form = CreateUser
    list_display = ['email','username']
    list_filter = ['email']
    fieldsets = (
        ('User Info',{'fields':('email','username')}),
        ('User Status',{'fields':('is_active','is_admin')}),
    )
    
    add_fieldsets = (
        ('Add User',{'fields',('email','username','password_1','password_2')}),
    )
    search_fields = ('email',)
    filter_horizontal = ()
    
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email','username','icon','bio']
    list_filter = ['email']
    fieldsets = (
        ('User Info',{'fields':('email','username','icon','bio')}),
    )
    
    add_fieldsets = (
        ('Add User',{'fields',('email','username','password_1','password_2')}),
    )
    
    search_fields = ('email',)
    filter_horizontal = ()
    
class AdressAdmin(admin.ModelAdmin):
    list_display = ('user_name','loc','number')  # Show title in the admin list view
    search_fields = ('user_name',) 

class wishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Show title in the admin list view
    search_fields = ('user',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    autocomplete_fields = ['product', 'size', 'color']

class CartAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'size', 'color', 'quantity')
    list_filter = ('product', 'size', 'color')
    search_fields = ('product__title',)
    autocomplete_fields = ['cart', 'product', 'size', 'color']

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.unregister(Group)
admin.site.register(Adresse,AdressAdmin)
admin.site.register(Wishlist,wishlistAdmin)