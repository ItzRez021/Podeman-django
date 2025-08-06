from django.db import models

class Blog(models.Model):
    creator = models.ForeignKey('accounts.User', on_delete=models.PROTECT, editable=False)
    icon = models.ImageField(upload_to='blogs/')
    title = models.CharField(max_length=40)
    info = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    info = models.TextField(max_length=500)

    def __str__(self):
        return self.title
    
class Productsimage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='image')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.title
    
class ProductSizes(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='size')
    size = models.CharField(max_length=50)

class ProductColors(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='color')
    color = models.CharField(max_length=50)

class Likes(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='like')
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='like')
    like = models.BooleanField(default=False)
    quantity = models.IntegerField()


