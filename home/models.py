from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator , MinValueValidator

class Cinfo(models.Model):
    Name = models.CharField(max_length=255)
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=20)
    Confirm = models.CharField(max_length=20)
    Email = models.EmailField()
    Code=models.IntegerField()
    PhoneNo= models.CharField(max_length=12)
    Address=models.CharField(max_length=1000)
    Image = models.ImageField(upload_to="images/customer/profile/", null=True, blank=True,default="images/customer/profile/default-customer.png")


class Vinfo(models.Model):
    Name = models.CharField(max_length=255)
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=20)
    Confirm = models.CharField(max_length=20)
    Email = models.EmailField()
    Aadhar = models.CharField(max_length=255)
    Code=models.IntegerField(null=True)
    PhoneNo = models.CharField(max_length=12)
    Kitchen = models.CharField(max_length=255)
    Address=models.CharField(max_length=1000)
    Image=models.ImageField(upload_to="images/vendor/profile/",null=True,blank=True,default="images/vendor/profile/default-vendor.PNG")


class Vendoradd(models.Model):
    Username = models.TextField()
    name = models.CharField(max_length=255)
    price=models.IntegerField()
    quantity=models.IntegerField()

class Feedbacks(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    phoneNo= models.CharField(max_length=12)
    feedback=models.TextField()
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])


ORDER_STATUS = ( 
    ("placed", "placed"), 
    ("accepted", "accepted"), 
    ("rejected", "rejected"), 
    ("delivering", "delivering"), 
    ("delivered", "delivered"),  
) 

class Order(models.Model):
    orderId=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Cinfo,on_delete=models.CASCADE,related_name="customer")
    vendor=models.ForeignKey(Vinfo,on_delete=models.CASCADE,related_name="vendor")
    orderDate=models.DateTimeField(auto_now_add=True)
    customer_username=models.CharField(max_length=255)
    vendor_username=models.CharField(max_length=255)
    ordered_items=models.CharField(max_length=5000)
    grandTotal=models.DecimalField(max_digits=6,decimal_places=2)
    email=models.EmailField()
    address=models.CharField(max_length=255)
    zipCode=models.CharField(max_length=10)
    phoneNo= models.CharField(max_length=12)
    paymentMode=models.CharField(max_length=10)
    status=models.CharField( 
        max_length = 10, 
        choices = ORDER_STATUS, 
        default = 'placed'
        ) 
