from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
   phone = models.CharField(max_length=15,null=True)
   block = models.CharField(max_length=15,default=False)
   address=models.CharField(max_length=250)
   address2=models.CharField(max_length=250,blank=True)
   address3=models.CharField(max_length=250,blank=True)
   address4=models.CharField(max_length=250,blank=True)


class Address(models.Model):
    username=models.CharField(max_length=50,null=True)
    building=models.CharField(max_length=250,blank=True)
    street=models.CharField(max_length=250,blank=True)
    area=models.CharField(max_length=250,blank=True)
    po=models.CharField(max_length=250,blank=True)
    district=models.CharField(max_length=250,blank=True)
    state=models.CharField(max_length=250,blank=True)
   

class Category(models.Model):
    category= models.CharField(max_length=15)
    def __str__(self):
        return self.category


class Products(models.Model):
    name = models.CharField(max_length=50)
    detail=models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    stock=models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_image1 = models.ImageField(upload_to='images')
    product_image2 = models.ImageField(upload_to='images')
    product_image3 = models.ImageField(upload_to='images')
    product_image4 = models.ImageField(upload_to='images')


class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    price=models.IntegerField(default=0)
    date_added=models.DateField(auto_now_add=True)


class Orders(models.Model):
    orderNumber= models.CharField(max_length=50)
    orderDate=models.DateField(auto_now_add=True)
    cartID=models.CharField(max_length=50)
    product=models.CharField(max_length=50)
    quantity=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    sale=models.IntegerField(blank=True)


class OrderNumber(models.Model):
    orderNumber=models.CharField(max_length=50)


class Coupon(models.Model):
    code=models.CharField(max_length=50)
    discount=models.IntegerField(default=0)
    status=models.CharField(max_length=50)


class Productoffer(models.Model):
    product=models.CharField(max_length=50)


    discount=models.IntegerField(default=0)
class Categoryoffer(models.Model):
    category=models.CharField(max_length=50)
    discount=models.IntegerField(default=0)


