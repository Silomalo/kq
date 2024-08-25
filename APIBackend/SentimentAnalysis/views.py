from django.shortcuts import render
from  django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from SentimentAnalysis.models import Departments, Employees
from SentimentAnalysis.serializers import DepartmentSerializer, EmployeeSerializer
from django.views.decorators.http import require_http_methods
# Create your views here.
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    GenericAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework import response, status
from .helpers import check_existing_department_name, check_existing_department_by_id
from .serializers import UpdateSingleDepartmentSerializer
from APIBackend.tasks import add_two_numbers,divide_two_numbers,scrap_data_with_beautifulsoup,scrap_data_from_site

class GetDepartment(GenericAPIView):
    serializer_class = DepartmentSerializer
    def get(self,request, department_id):
        numbers = add_two_numbers.delay(1, 2)
        # division = divide_two_numbers.delay(5, 0)
        
        # I have 10 pages in my website, I want to scrap all the pages
        # https://quotes.toscrape.com/page/10/
        
        # for i in range(1, 11):
        #     web_url = f"https://quotes.toscrape.com/page/{i}/"
        #     print(web_url)
        #     scrapping = scrap_data_with_beautifulsoup.delay(web_url)
        #     print("scrapped page", i)
            
        scrapping = scrap_data_with_beautifulsoup.delay("https://quotes.toscrape.com")
            
        
        # scrapping = scrap_data_from_site.delay("https://www.tripadvisor.com/Airline_Review-d8729102-Reviews-or5-Kenya-Airways.html#REVIEWS")
        # print(scrapping)
        try:
            department = Departments.objects.get(DepartmentId=department_id)
            department_serializer = self.serializer_class(department)
            return response.Response(department_serializer.data, status=status.HTTP_200_OK)
        except Departments.DoesNotExist:
            return response.Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllDepartments(ListAPIView):
    serializer_class = DepartmentSerializer
    def get(self, request):
        departments = Departments.objects.all()
        department_serializer = self.serializer_class(departments, many=True)
        return response.Response(department_serializer.data, status=status.HTTP_200_OK)
    
class CreateDepartment(CreateAPIView):
    serializer_class = DepartmentSerializer
    def post(self, request):
        department_data = request.data
        # print(department_data)
        department_exits = check_existing_department_name(department_data.get('DepartmentName'))
        # print(department_exits)
        if department_exits:
            return response.Response({"error": "Department already exists"}, status=status.HTTP_409_CONFLICT)
        department_serializer = self.serializer_class(data=department_data)
        if department_serializer.is_valid():
            department_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
class UpdateDepartment(UpdateAPIView):
    serializer_class = UpdateSingleDepartmentSerializer
    def put(self, request, department_id):
        department_data = request.data
        try:
            department = Departments.objects.get(DepartmentId=department_id)
            department_exits = check_existing_department_by_id(department_id)
            print(department_exits)
            if not department_exits:
                return response.Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(department_exits, data=department_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Departments.DoesNotExist:
            return response.Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteDepartment(DestroyAPIView):
    def delete(self, request, department_id):
        try:
            department = Departments.objects.get(DepartmentId=department_id)
            department.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except Departments.DoesNotExist:
            return JsonResponse({"error": "Department not found"}, status=404)
        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
            
            
    


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def departmentApi(request, department_id=0):
    if request.method == 'GET':
        if department_id == 0:
            departments = Departments.objects.all()
            department_serializer = DepartmentSerializer(departments, many=True)
            return JsonResponse(department_serializer.data, safe=False)
        else:
            try:
                department = Departments.objects.get(DepartmentId=department_id)
                department_serializer = DepartmentSerializer(department)
                return JsonResponse(department_serializer.data, safe=False)
            except Departments.DoesNotExist:
                return JsonResponse({"error": "Department not found"}, status=404)
    elif request.method == 'POST':
        department_data = JSONParser().parse(request)
        department_serializer = DepartmentSerializer(data=department_data)
        if department_serializer.is_valid():
            department_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        department_data = JSONParser().parse(request)
        print(department_data.get('DepartmentId'))
        dept_id = department_data.get('DepartmentId')
        try:
            department = Departments.objects.get(DepartmentId=dept_id)
            department_serializer = DepartmentSerializer(department, data=department_data)
            if department_serializer.is_valid():
                department_serializer.save()
                return JsonResponse("Updated Successfully", safe=False)
            return JsonResponse("Failed to Update", safe=False)
        except Departments.DoesNotExist as e:
            print(e)
            return JsonResponse({"error": "Department not found"}, status=404)
    elif request.method == 'DELETE':
        try:
            department = Departments.objects.get(DepartmentId=department_id)
            department.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except Departments.DoesNotExist:
            return JsonResponse({"error": "Department not found"}, status=404)