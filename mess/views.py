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
    else: 
        return render(request, 'mess/index.html', {'error_msg': True}) 
        
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
    else: 
        return render(request, 'mess/index.html', {'error_msg': True})

def studentpage(request, id):
    if True:
        student = get_object_or_404(Student,student_id=id)
        t = timezone.now()
        date_today = t.strftime("%Y-%m-%d")
        try:
            dailybill = student.dailybill_set.get(date= date_today)
        except DailyBill.DoesNotExist:
            context = {
                'flag' : False,
                'total_bill': student.total_bill,
                'student_id': id,
            }
            return render(request, 'mess/studentpage.html', context) 

        bill = 0
        m = get_object_or_404(Mess, date= date_today,  mess_name = student.mess)
        if dailybill.breakfast is True: bill += m.breakfast_rate
        if dailybill.lunch is True: bill += m.lunch_rate
        if dailybill.dinner is True: bill += m.dinner_rate
        bill += (dailybill.extras_breakfast)*(m.extras_rate_breakfast)
        bill += (dailybill.extras_lunch)*(m.extras_rate_lunch)
        bill += (dailybill.extras_dinner)*(m.extras_rate_dinner)
        total_bill = student.total_bill
        context = {
            'flag': True,
            'dailybillset': dailybill,
            'mess_name': student.mess,
            'dailybill': bill,
            'student_id': id, 
            'total_bill': total_bill,   
        }
        return render(request, 'mess/studentpage.html', context)
    else:
        return HttpResponseRedirect(reverse('mess:index'))

def wardenpage(request, warden_id): 
    warden = get_object_or_404(Warden, warden_id= warden_id)
    mess = Mess.objects.filter(warden_id= warden.pk)
    context = {
        'warden': warden,
        'mess_list': mess,
    }
    return render(request, 'mess/wardenpage.html', context)

def mess(request, mess):
    mess_record = get_object_or_404(Mess, mess_name = mess)
    warden = get_object_or_404(Warden, name = mess_record.warden_id)
    context = {
        'mess_record': mess_record,
        'warden': warden
    }
    return render(request, 'mess/mess.html', context)

def update(request, mess):
    messx = get_object_or_404(Mess, mess_name = mess)
    warden = get_object_or_404(Warden, name = messx.warden_id)
    messx.breakfast_rate  = request.POST['bname']
    messx.lunch_rate = request.POST['lname']
    messx.dinner_rate = request.POST['dname']
    messx.extras_rate_breakfast = request.POST['bxname']
    messx.extras_rate_lunch = request.POST['exname']
    messx.extra_rate_dinner = request.POST['dxname'] 
    messx.date = date.today
    messx.save()
    return HttpResponseRedirect(reverse('mess:wardenpage', args=(warden.warden_id,)))

def logout_view(request, id):
    logout(request)
    return HttpResponseRedirect(reverse('mess:index'))

def logout_view1(request, warden_id):
    logout(request)
    return HttpResponseRedirect(reverse('mess:index'))
