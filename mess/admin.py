from django.contrib import admin
from .models import Mess, Warden, Student, DailyBill

admin.site.register(Warden)
admin.site.register(Student)
admin.site.register(Mess)
admin.site.register(DailyBill)