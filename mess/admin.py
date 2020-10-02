from django.contrib import admin

from .models import Warden, Mess, Student, DailyBill

admin.site.register(Warden)
admin.site.register(Mess)
admin.site.register(Student)
admin.site.register(DailyBill)