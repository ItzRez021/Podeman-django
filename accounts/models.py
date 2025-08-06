from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email,username,password):
        if not email:
            raise ValueError('email field is empty')
        if not username:
            raise ValueError('username field is empty')
        user = self.model(email=self.normalize_email(email),username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password):
        user = self.create_user(email,username,password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True)
    bio = models.TextField(max_length=200,blank=True,null=True)
    icon = models.ImageField(default='profiles/def.png',upload_to='profiles/',blank=True,null=True)
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.user.username != self.username:
            self.user.username = self.username
            self.user.save(update_fields=['username'])
        super().save(*args, **kwargs)    

class Adresse(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='adress')
    user_name = models.CharField(max_length=100,null=True)
    loc = models.CharField(max_length=400,null=True)
    number = models.PositiveIntegerField(null=True)

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField('home.Product', related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField('home.Product', through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('home.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey('home.ProductSizes', null=True, blank=True, on_delete=models.SET_NULL)
    color = models.ForeignKey('home.ProductColors', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        unique_together = ('cart', 'product', 'size', 'color')

    def __str__(self):
        return f"{self.product.title} - {self.size.size if self.size else 'No Size'} - {self.color.color if self.color else 'No Color'} (x{self.quantity})"

    @property
    def total_price(self):
        return self.quantity * self.product.price