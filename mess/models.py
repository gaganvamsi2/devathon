from django.db import models
from django.shortcuts import get_object_or_404
from datetime import date

class Mess(models.Model):
    mess_name = models.CharField(max_length=4096, default="Ganga")
    breakfast_rate = models.IntegerField(default=0)
    lunch_rate = models.IntegerField(default=0)
    dinner_rate = models.IntegerField(default=0)
    extras_rate_breakfast = models.IntegerField(default=0)
    extras_rate_lunch = models.IntegerField(default=0)
    extras_rate_dinner = models.IntegerField(default=0)
    date = models.DateField(default=date.today)
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
    extras_breakfast = models.IntegerField(default=0)
    extras_lunch = models.IntegerField(default=0)
    extras_dinner = models.IntegerField(default=0)
    date = models.DateField(default=date.today)


    def checkDate(self, mess_name):
        if self.date == get_object_or_404(Mess, date=self.date, name=mess_name):
            return True
        else:
            return False

    def __str__(self):
        return str(self.student)