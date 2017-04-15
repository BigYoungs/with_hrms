from django.contrib import admin
from profiles.models import Profile,department,duties,company,attendances,attendance_data,attendance_standards,salary_standard,salary_cs


class CompanytAdmin(admin.ModelAdmin):
    list_display = ('company_name',  'company_loca')
    search_fields = ('company_name',)

class Salary_standardAdmin(admin.ModelAdmin):
    list_display = ('salary_lev_name',  'basic_salary')
    search_fields = ('salary_lev_name',)

#class Attendance_dataAdmin(admin.ModelAdmin):
#	list_display = ('attendance_day','employee_id')
#	search_fields = ('attendance_day',)

# Register your models here.
admin.site.register(department)
admin.site.register(company,CompanytAdmin)
admin.site.register(Profile)
admin.site.register(duties)
admin.site.register(attendances)
admin.site.register(attendance_data)
admin.site.register(attendance_standards)
admin.site.register(salary_standard,Salary_standardAdmin)
admin.site.register(salary_cs)