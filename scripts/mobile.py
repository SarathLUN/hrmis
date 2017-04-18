__author__ = 'Tusfiqur'
from account.models import EmployeeUser

def hello():
    return "Hello, World"


def run():
    print(hello())
    emp = EmployeeUser.objects.all()
    for list in emp:
        print(list.employee)