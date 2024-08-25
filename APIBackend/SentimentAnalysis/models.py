from django.db import models
# Create your models here.

class Departments(models.Model):
        DepartmentId = models.AutoField(primary_key=True)
        DepartmentName = models.CharField(max_length=100)
        # first_name=models.CharField(max_length=100)
        
class Employees(models.Model):
        EmployeeId = models.AutoField(primary_key=True)
        EmployeeName = models.CharField(max_length=100)
        Department = models.ForeignKey(Departments, on_delete=models.CASCADE)
        DateOfJoining = models.DateField()
        PhotoFileName = models.CharField(max_length=100)
        

class Addition(models.Model):
        id = models.AutoField(primary_key=True)
        num_1 = models.IntegerField()
        num_2 = models.IntegerField()
        result = models.IntegerField()
        # date = models.DateField()
        
class Reviews(models.Model):
        id = models.AutoField(primary_key=True)
        source = models.CharField(max_length=100)
        source_link = models.CharField(max_length=100, null=True)
        title = models.CharField(max_length=100, null=True)
        description = models.TextField()
        # sentiment can be positive, negative or neutral
        sentiment = models.CharField(max_length=100)
        


# from mongoengine import Document, StringField, IntField
# class Departments(Document):
#         DepartmentId = IntField(primary_key=True)
#         DepartmentName = StringField(max_length=100)
        
# class Employees(Document):
#         EmployeeId = IntField(primary_key=True)
#         EmployeeName = StringField(max_length=100)
#         Department = StringField(max_length=100)
#         DateOfJoining = StringField(max_length=100)
        # PhotoFileName = StringField(max_length=100)