from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from django.db.models import Sum

class CustomUser(AbstractUser):

    USER = (
        ('1', 'HOD'),
        ('2', 'EMPLOYEE')
    )
    last_name = models.CharField(max_length=100, null=True)
 
    user_type = models.CharField(choices=USER, max_length=50, default=1)

    
class Employee(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=150, null=True)
    gender = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.admin.username    

class Collecteur(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    address = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Create your models here.
class Products(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    product_type = models.CharField(max_length=250)
    price = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Products"

    def __str__(self):
        return str(f"{self.product_type}")


class Invoice(models.Model):
    code = models.CharField(max_length=100)
    collecteur = models.ForeignKey(Collecteur, on_delete=models.CASCADE, null=True)
    total_amount = models.FloatField(max_length=15)
    amount_paid = models.FloatField(max_length=15)
    position = models.CharField(max_length=2, choices=(('0','Pending'), ('1', 'In-progress'), ('2', 'Done')), default = 0)
    payment = models.CharField(max_length=2, choices=(('0','Unpaid'), ('1', 'Paid')), default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Invoices"

    def __str__(self):
        return str(f"{self.code} - {self.collecteur}")

    def rest(self):
        rest = float(self.total_amount) - float(self.amount_paid)
        return rest

        
    def totalProducts(self):
        try:
            Products =  InvoiceProducts.objects.filter(invoice = self).aggregate(Sum('total_amount'))
            Products = Products['total_amount__sum']
        except:
            Products = 0
        return float(Products)

class InvoiceProducts(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,related_name="invoice_fk")
    product_type = models.ForeignKey(Products, on_delete=models.CASCADE,related_name="products_fk")
    price = models.FloatField(max_length=15, default=0)
    weight = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)
    date_added = models.DateTimeField(default = timezone.now)

    class Meta:
        verbose_name_plural = "List of Invoice Products"

    def __str__(self):
        return str(f"{self.invoice.code} - {self.product_type.product_type}")
#Employee Invoice
class Bill(models.Model):
    code = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    total_amount = models.FloatField(max_length=15)
    amount_paid = models.FloatField(max_length=15)
    status = models.CharField(max_length=2, choices=(('0','Pending'), ('1', 'In-progress'), ('2', 'Done')), default = 0)
    payment = models.CharField(max_length=2, choices=(('0','Unpaid'), ('1', 'Paid')), default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    class Meta:
        verbose_name_plural = "List of Employee Invoices"

    def __str__(self):
        return str(f"{self.code} - {self.employee.admin.username}")
    
    def rest(self):
        rest = float(self.total_amount) - float(self.amount_paid)
        return rest

    def totalProducts(self):
        try:
            Products = BillProducts.objects.filter(bill = self).aggregate(Sum('total_amount'))
            Products = Products['total_amount__sum']
        except:
            Products = 0
        return float(Products)    

class BillProducts(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE,related_name="bill_fk")
    product_type = models.ForeignKey(Products, on_delete=models.CASCADE,related_name="billproducts_fk")
    price = models.FloatField(max_length=15, default=0)
    weight = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)
    date_added = models.DateTimeField(default = timezone.now)

    class Meta:
        verbose_name_plural = "List of Invoice Products"

    def __str__(self):
        return str(f"{self.bill.code} - {self.product_type.product_type}")

#Employee
class Client(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    address = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class EmployeeProducts(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    product_type = models.CharField(max_length=250)
    price = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Products"

    def __str__(self):
        return str(f"{self.product_type}")

class Purchase(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_amount = models.FloatField(max_length=15)
    amount_paid = models.FloatField(max_length=15)
    regulation = models.CharField(max_length=2, choices=(('0','Pending'), ('1', 'In-progress'), ('2', 'Done')), default = 0)
    payment = models.CharField(max_length=2, choices=(('0','Unpaid'), ('1', 'Paid')), default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Purchases"

    def __str__(self):
        return str(f"{self.code} - {self.client}")

    def rest(self):
        rest = float(self.total_amount) - float(self.amount_paid)
        return rest
             
    def totalProducts(self):
        try:
            Products =  PurchaseProducts.objects.filter(purchase = self).aggregate(Sum('total_amount'))
            Products = Products['total_amount__sum']
        except:
            Products = 0
        return float(Products)

class PurchaseProducts(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_fk")
    product_type = models.ForeignKey(EmployeeProducts, on_delete=models.CASCADE, related_name="products_fk")
    price = models.FloatField(max_length=15, default=0)
    weight = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)
  
    class Meta:
        verbose_name_plural = "List of Purchase Products"

    def __str__(self):
        return str(f"{self.purchase.code} - {self.product_type.product_type}")

class Expenses(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(max_length=15, default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)    

    def __str__(sefl):
        return self.employee.admin.username

class Costs(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    amount = models.FloatField(max_length=15, default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

#Sales
class Sales(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=100, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_amount = models.FloatField(max_length=15)
    amount_paid = models.FloatField(max_length=15)
    condition = models.CharField(max_length=2, choices=(('0','Pending'), ('1', 'In-progress'), ('2', 'Done')), default = 0)
    payment = models.CharField(max_length=2, choices=(('0','Unpaid'), ('1', 'Paid')), default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Sales"

    def __str__(self):
        return str(f"{self.code} - {self.client}")

    def rest(self):
        rest = float(self.total_amount) - float(self.amount_paid)
        return rest
             
    def totalProducts(self):
        try:
            Products =  SalesProducts.objects.filter(sale = self).aggregate(Sum('total_amount'))
            Products = Products['total_amount__sum']
        except:
            Products = 0
        return float(Products)

class SalesProducts(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name="sale_fk")
    product_type = models.ForeignKey(EmployeeProducts, on_delete=models.CASCADE, related_name="saleproducts_fk")
    price = models.FloatField(max_length=15, default=0)
    weight = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)
  
    class Meta:
        verbose_name_plural = "List of Sales Products"

    def __str__(self):
        return str(f"{self.sale.code} - {self.product_type.product_type}")            
