from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student, Warden, DailyBill, Mess
from django.utils import timezone
from datetime import date

def index(request):
    return render(request, 'mess/index.html', {'error_msg': False})

def wardenpageauthenticate(request):
    warden_id = request.POST['warden_username']
    warden_password = request.POST['warden_password']
    warden_present = authenticate(username = warden_id, password = warden_password)
    if warden_present is None:
        a = get_object_or_404(Warden, warden_id= warden_id)
        if a is not None:
            user = User.objects.create_user(warden_id, 'default@email.com', warden_password)
            user.save()
            warden_present = authenticate(username = warden_id, password = warden_password)

    if warden_present is not None and get_object_or_404(Warden, warden_id=warden_id):
        return HttpResponseRedirect(reverse('mess:wardenpage', args=(warden_id,)))
    else : return render(request, 'mess/index.html', {'error_msg': True}) 
        
def studentpageauthenticate(request):
    student_id = request.POST['student_username']
    student_password = request.POST['student_password']
    student_present = authenticate(username = student_id, password = student_password)
    if student_present is None:
        a = get_object_or_404(Student, student_id = student_id)
        if a is not None:
            user = User.objects.create_user(student_id, 'default@email.com', student_password)
            user.save()
            student_present = authenticate(username = student_id, password = student_password)

    if student_present is not None and get_object_or_404(Student, student_id=student_id):
        return HttpResponseRedirect(reverse('mess:studentpage', args=(student_id,)))
    else : return render(request, 'mess/index.html', {'error_msg': True})

def studentpage(request, id):
    student = get_object_or_404(Student,student_id=id)
    t = timezone.now()
    date_today = t.strftime("%Y-%m-%d")
    dailybill = student.dailybill_set.get(date= date_today)
    bill = 0
    m = get_object_or_404(Mess, date= date_today,  mess_name = student.mess)
    if dailybill.breakfast is True: bill += m.breakfast_rate
    if dailybill.lunch is True: bill += m.lunch_rate
    if dailybill.dinner is True: bill += m.dinner_rate
    bill += (dailybill.extras_breakfast)*(m.extras_rate_breakfast)
    bill += (dailybill.extras_lunch)*(m.extras_rate_lunch)
    bill += (dailybill.extras_dinner)*(m.extras_rate_dinner)
    total_bill = student.total_bill + bill
    student.total_bill = total_bill
    student.save()
    print(dailybill)
    context = {
        'mess_name': student.mess,
        'dailybill': bill,
        'student_id': id, 
        'total_bill': total_bill,   
    }
    return render(request, 'mess/studentpage.html', context)

def wardenpage(request, id):
    return render(request, 'mess/wardenpage.html', {'warden_id': id})

def logout_view(request, id):
    logout(request)
    return HttpResponseRedirect(reverse('mess:index'))

def logout_view1(request, id):
    logout(request)
    return HttpResponseRedirect(reverse('mess:index'))
