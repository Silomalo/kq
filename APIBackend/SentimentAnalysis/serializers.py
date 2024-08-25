from rest_framework import serializers
from SentimentAnalysis.models import Departments, Employees, Addition


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'
        
class UpdateSingleDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Departments
        fields =("DepartmentName",)
        
        
class AdditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addition
        fields = '__all__'
        