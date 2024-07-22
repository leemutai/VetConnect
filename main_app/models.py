from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ''
)


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=300)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    products_image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.title


class Farmer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    appointment_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    vet_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    def __str__(self):
        return self.appointment_id


class Purchase(models.Model):
    purchase_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return self.purchase_id
