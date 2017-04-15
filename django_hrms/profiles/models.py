#-*-coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

sex_choices = (
		('F','Female'),
		('M','Male'),
	)

status_choices = (
		('Z','在职'),
		('L','离职'),
		('O','停职'),
		('T','退休'),

	)

assignment_status_choices = (
		('A','已外派'),
		('B','未外派'),

	)

in_condition_choices = (
		('in_attend','正常上班'),
		('late','迟到'),
	)
out_condition_choices = (
		('out_attend','正常下班'),
		('earlyout','早退'),
	)



#人员基本信息表
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	name = models.CharField('name',max_length = 30,)
	sex = models.CharField(max_length = 1,choices = sex_choices )
	birth = models.DateField('birth',help_text = '输入格式为 YYYY-MM-DD',null = True)
	birth_place = models.CharField('birth_place',max_length = 50)
	nation = models.CharField('nation',max_length=20)
	identification_num = models.CharField('identification_num',max_length = 18)
	political = models.CharField(null = True,max_length = 50)
	duty = models.ForeignKey('duties',null=True)
	company = models.ForeignKey('company',null=True)
	department = models.ForeignKey('department',null=True)
	graduation_school = models.CharField(null = True,max_length = 30)
	graduation_date = models.DateField(null = True,help_text = '输入格式为 YYYY-MM-DD')
	education = models.CharField(max_length = 10)
	address = models.CharField(max_length = 50)
	telephone = models.CharField(max_length = 11)
	email = models.EmailField(null = True)
	status = models.CharField(choices = status_choices,max_length = 1)

	def __unicode__(self):
		return self.name

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
 #       Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
 #   instance.profile.save()



#部门信息表
class department(models.Model):
	department_name = models.CharField(max_length = 30)
	department_comment = models.CharField(max_length = 500)

	def __unicode__(self):
		return self.department_name


#职务信息表 
class duties(models.Model):
	duty_id = models.CharField(max_length = 4 ,primary_key=True)
	duty_name = models.CharField(max_length = 30 )
	department = models.ForeignKey('department',null=True)
	salary_lev_id = models.ForeignKey('salary_standard',null=True)

	def __unicode__(self):
		return self.duty_name




#外派单位信息表
class company(models.Model):
	company_name = models.CharField(max_length = 30,unique=True)
	company_loca = models.CharField(max_length = 50)

	def __unicode__(self):
		return  self.company_name






#考勤数据表   通过日期区间跟ID确定一个员工的考勤情况      员工只能通过 now 按钮输入，并且可以输入多次，不过选最早的当签到，最晚的当签退
class attendance_data(models.Model):                 
	user = models.ForeignKey(User)       #employee_id作为一个对象，拥有对应Profile的所有属性且能对其进行访问
	attendance_day = models.DateField()
	sign_in = models.TimeField(blank = True , null = True)
	sign_out = models.TimeField(blank = True , null =True)
	

	def __unicode__(self):
		return u'%s %s '  % (self.attendance_day,self.user.profile.name)     #可以进行多个参数的显示设置
	class Meta:
		unique_together = ("user","attendance_day")		
  		ordering = ['attendance_day']
#各公司考勤规则表       
class attendance_standards(models.Model):
	company = models.ForeignKey('company')
	regular_sign_in_min = models.TimeField(help_text='早上迟到时间起点   ---- **签到最早时间比这项早，为正常上班')
	regular_sign_in_max = models.TimeField(help_text='早上迟到时间终点   ---- **限制签到的时间段 即min_max') 
	regular_sign_out_min = models.TimeField(help_text='下午早退时间起点  ---- **限制签退的时间段 即min_max') 
	regular_sign_out_max = models.TimeField(help_text='下午早退时间终点  ----**签退最晚时间比这项晚，为正常下班')
	missed_time_total_max = models.IntegerField(default = 3 , help_text='早上迟到的时间加上下午早退时间的总和。超过这个时间则算旷工')
	def __unicode__(self):
		return u'%s' % self.company


#

#考勤表       这个表建立了考勤原数据跟考勤标准的联系与对比，同时能够将结果存在condition_status中，condition_status也就是我们要进行考核的内容
class attendances(models.Model):
	user = models.ForeignKey(User)      
	attendance_day =  models.ForeignKey('attendance_data')
	in_condition_status = models.CharField(choices = in_condition_choices,max_length=10,default='in_attend')	
	out_condition_status = models.CharField(choices = out_condition_choices,max_length=10,default='out_attend')
	not_attend = models.BooleanField(default=False)
	def __unicode__(self):
		return u'%s _ %s ' % (self.user.profile.name,self.attendance_day)
		ordering = ['attendance_day'] 

#工资标准信息表
class salary_standard(models.Model):
	salary_lev_id = models.CharField(max_length = 4, primary_key=True)
	salary_lev_name = models.CharField(max_length = 10)
	basic_salary = models.DecimalField(max_digits = 11 , decimal_places = 2 )
	subsidy = models.DecimalField(max_digits = 11 , decimal_places = 2 )
	housing_fund = models.DecimalField(max_digits = 11 , decimal_places = 2 )
	social_security = models.DecimalField(max_digits = 11 , decimal_places = 2 )
	bonus = models.DecimalField(max_digits = 11 , decimal_places = 2 )
    
    	def __unicode__(self):
    		return self.salary_lev_name

#工资记发信息表
class salary_cs(models.Model):
	attendance = models.ForeignKey('attendances',null=True)
	user = models.ForeignKey(User,null=True)
	salary_should_sent_time = models.CharField(max_length=30)
	salary_standard = models.ForeignKey('salary_standard',null=True)
	salary_total = models.DecimalField(max_digits = 11 , decimal_places = 2 )
	salary_actual = models.DecimalField(max_digits = 11 , decimal_places = 2 )
	sent_salary_status = models.BooleanField("工资是否已发放？", default=False)