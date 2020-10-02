from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student, Warden, DailyBill, Mess
from django.utils import timezone

def index(request):
    return render(request, 'mess/index.html', {'error_msg': False})

def wardenpageauthenticate(request):
    warden_id = request.POST['warden_username']
    warden_password = request.POST['warden_password']
    warden_present = authenticate(username = warden_id, password = warden_password)
    if warden_present is None:
        a = Warden.objects.get(warden_id= warden_id)
        if a is not None:
            user = User.objects.create_user(warden_id, 'default@email.com', warden_password)
            user.save()
            warden_present = authenticate(username = warden_id, password = warden_password)

    if warden_present is not None and Warden.objects.get(warden_id=warden_id):
        return HttpResponseRedirect(reverse('mess:wardenpage', args=(warden_id,)))
    else : return render(request, 'mess/index.html', {'error_msg': True}) 
        
def studentpageauthenticate(request):
    student_id = request.POST['student_username']
    student_password = request.POST['student_password']
    student_present = authenticate(username = student_id, password = student_password)
    if student_present is None:
        a = Student.objects.get(student_id = student_id)
        if a is not None:
            user = User.objects.create_user(student_id, 'default@email.com', student_password)
            user.save()
            student_present = authenticate(username = student_id, password = student_password)

    if student_present is not None and Student.objects.get(student_id=student_id):
        return HttpResponseRedirect(reverse('mess:studentpage', args=(student_id,)))
    else : return render(request, 'mess/index.html', {'error_msg': True})

def studentpage(request, id):
    dailybill = DailyBill.objects.get(student=id)
    bill = dailybill.get_todays_bill()
    student = Student.objects.filter(student_id=id)
    total_bill = student.total_bill
    total_bill += bill
    student.total_bill += bill
    student.save()
    context = {'student_id': id, 
    'todays_bill': bill, 
    'total_bill': total_bill, 
    'daily_bill': dailybill,
    }
    return render(request, 'mess/studentpage.html', context)

def wardenpage(request, id):
    return render(request, 'mess/wardenpage.html', {'warden_id': id})

def logout_view(request, id):
    logout(request)
    return HttpResponseRedirect(reverse('mess:index'))
