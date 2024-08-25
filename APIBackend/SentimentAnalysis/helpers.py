from .models import Departments

def check_existing_department_name(department_name):
    try:
        print(department_name)
        department = Departments.objects.filter(DepartmentName=department_name).exists()
        print(department)
        if department:
            return True
        else:
            return False
    except Departments.DoesNotExist:
        return False
    
def check_existing_department_by_id(dept_id):
    try:
        department = Departments.objects.filter(DepartmentId=dept_id).first()
        return  department
    except Departments.DoesNotExist:
        return  None 