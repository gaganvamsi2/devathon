from django.db import models
from django.utils import timezone
import datetime

class Mess(models.Model):
    mess_name = models.CharField(max_length=4096, default="Ganga")
    breakfast_rate = models.IntegerField(default=0)
    lunch_rate = models.IntegerField(default=0)
    dinner_rate = models.IntegerField(default=0)
    extras_rate = models.IntegerField(default=0)
    date = models.DateField()
    def __str__(self):
        return self.mess_name

class Warden(models.Model):
    name = models.CharField(max_length=4096)
    warden_id = models.CharField(max_length=20) 
    mess = models.ForeignKey(Mess, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=4096)
    student_id = models.CharField(max_length=20)
    year = models.IntegerField(default=1)
    mess = models.ForeignKey(Mess, on_delete=models.CASCADE)
    total_bill = models.IntegerField(default=0)

    def __str__(self):
        return self.student_id

class DailyBill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    extras = models.IntegerField(default=0)
    date = models.DateField()

    def get_todays_bill(self):
        bill = 0
        m = Mess.objects.get(date= self)
        if self.breakfast is not None: bill += m.breakfast_rate
        if self.lunch is not None: bill += m.lunch_rate
        if self.dinner is not None: bill += m.dinner_rate
        if self.extras != 0:
            bill += (self.extras)*m.extras_rate
        return bill