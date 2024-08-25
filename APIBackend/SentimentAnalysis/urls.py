from django.urls import path
from SentimentAnalysis import views

urlpatterns = [
    path('department', views.GetAllDepartments.as_view(), name='get-all-department'),
    path('department/<int:department_id>', views.GetDepartment.as_view(), name='get-single-department'),
    path('department/add', views.CreateDepartment.as_view(), name='create-department'),
    path('department/update/<int:department_id>', views.UpdateDepartment.as_view(), name='update-department'),
    path('department/delete/<int:department_id>', views.DeleteDepartment.as_view(), name='delete-department'),
    
]

