#-*-coding:utf-8 -*-
from django.shortcuts  import render,HttpResponseRedirect,render_to_response,HttpResponse,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth,messages # 別忘了import auth
from django.contrib.auth.models import User
from django.template.context import RequestContext


from django.forms.formsets import formset_factory
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib.auth.decorators import login_required

from .forms import loginForm,ChangepwdForm

from profiles.models import attendance_data,attendance_standards,attendances

import datetime

def login(request):

    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/index/')
    else:
        form = loginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            user = auth.authenticate(username = username, password = password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return render_to_response('index.html',RequestContext(request))
            else:
                return render_to_response('login.html',RequestContext(request,{ 'form':form,
                                                                                'password_is_wrong':True
                                                                              })
                                                                            )
        else:
            return render_to_response('login.html',RequestContext(request,{'form':form,}))



@login_required(login_url = '/login/')  
def changepwd(request):  
    if request.method == 'GET':  
        form = ChangepwdForm()  
        return render_to_response('changepwd.html', RequestContext(request, {'form': form,}))  
    else:  
        form = ChangepwdForm(request.POST)  
        if form.is_valid():  
            username = request.user.username  
            oldpassword = request.POST.get('oldpassword', '')  
            user = auth.authenticate(username=username, password=oldpassword)  
            if user is not None and user.is_active:  
                newpassword = request.POST.get('newpassword1', '')  
                user.set_password(newpassword)  
                user.save()  
                return render_to_response('index.html', RequestContext(request,{'changepwd_success':True}))  
            else:  
                return render_to_response('changepwd.html', RequestContext(request, {'form': form,'oldpassword_is_wrong':True}))  
        else:  
            return render_to_response('changepwd.html', RequestContext(request, {'form': form,}))  




def base(request):
    return render_to_response('base.html',locals())


def index(request):
    return render_to_response('index.html',locals())

def test(req):

    return render_to_response('test.html',locals())

@login_required(login_url = '/login/')  
def profiles(request):
    #  users = user_setobjects.get(name = request.user)
  #    username = user.name
 #      user1 = user.objects.get(name = request.user )
       user1 = User.objects.get( id = request.user.id)
       user = user1.profile
       return render_to_response('profiles.html',locals())

@login_required(login_url = '/login/')  
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

#@login_required(login_url = '/login/')  
     # 给更新后的考勤表记录补全数据
def update_attend_rela(request):
    #  attendances_all2 = attendance_data.objects.filter(user_id = request.user.id)
    a_log = attendance_data.objects.filter(user_id = request.user.id)
    user = User.objects.get(id = request.user.id).profile
    attendance_rela2 = attendances.objects.filter(user_id = request.user.id)
    try:
      a_s = attendance_standards.objects.get(company_id = user.company)
    except attendance_standards.DoesNotExist:   #DoesNotExist是attendance_standards的一个属性，用于判断是否有数据存在
      print "此用户并没有分配公司"
    else:
      pass

    for r1 in attendance_rela2:
      if r1.attendance_day.sign_in is not None and  a_s.regular_sign_in_min <=  r1.attendance_day.sign_in <=  a_s.regular_sign_in_max :
         r1.in_condition_status = 'late'
      elif r1.attendance_day.sign_in is not None and r1.attendance_day.sign_in > a_s.regular_sign_in_max:
         r1.in_condition_status = None
      else:
         r1.in_condition_status = 'in_attend'
      if r1.attendance_day.sign_out is not None and a_s.regular_sign_out_min <= r1.attendance_day.sign_out <= a_s.regular_sign_out_max:
         r1.out_condition_status = 'earlyout'
      else:
         r1.in_condition_status = 'out_attend'
      
      #设定临时的日期变量，time类不能相减

      tem_date = datetime.datetime.date(datetime.datetime.now())
      if r1.attendance_day.sign_in is not None:
          r1_a_in = datetime.datetime.combine(tem_date,r1.attendance_day.sign_in)
      a_s_in_min = datetime.datetime.combine(tem_date,a_s.regular_sign_in_min)
      if r1.attendance_day.sign_out is not None:
          r1_a_out = datetime.datetime.combine(tem_date,r1.attendance_day.sign_out)
      
      a_s_out_max = datetime.datetime.combine(tem_date,a_s.regular_sign_out_max)


      #该天实际未上班的总时间,返回一个timedelta对象
      missed_time_total = ( r1_a_in - a_s_in_min ) + (r1_a_out - a_s_out_max)
      
      #timedelta的原型
      #class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
      #该天迟到并早退，或者实际未上班总时间超过规定小时，则记为旷工
      if (r1.in_condition_status == 'late' and r1.out_condition_status == 'true') or (missed_time_total > datetime.timedelta( hours =a_s.missed_time_total_max)):
        r1.not_attend = True 
      # 写入数据库
      r1.save() 


@login_required(login_url = '/login/')  
def attendance_log(request):                  #考勤记录

     update_attend_rela(request)
     a_log = attendance_data.objects.filter(user_id = request.user.id)
     user = User.objects.get(id = request.user.id).profile
     attendance_rela2 = attendances.objects.filter(user_id = request.user.id)
     try:
      a_s = attendance_standards.objects.get(company_id = user.company)
     except attendance_standards.DoesNotExist:   #DoesNotExist是attendance_standards的一个属性，用于判断是否有数据存在
      print "此用户并没有分配公司"
     else:
      pass

     for r1 in attendance_rela2:
      if r1.attendance_day.sign_in is  None or a_s.regular_sign_in_min <=  r1.attendance_day.sign_in <=  a_s.regular_sign_in_max  or r1.attendance_day.sign_in > a_s.regular_sign_in_max:
         r1.in_condition_status = 'late'
      else:
         r1.in_condition_status = 'in_attend'
      if r1.attendance_day.sign_out is  None or a_s.regular_sign_out_min <=  r1.attendance_day.sign_out <= a_s.regular_sign_out_max:
         r1.out_condition_status = 'earlyout'
      else:
         r1.out_condition_status = 'out_attend' 
      
    #设定临时的日期变量，time类不能相减
      tem_date = datetime.datetime.date(datetime.datetime.now())
      if r1.attendance_day.sign_in is not None :
       r1_a_in = datetime.datetime.combine(tem_date,r1.attendance_day.sign_in)
      a_s_in_min = datetime.datetime.combine(tem_date,a_s.regular_sign_in_min)
      if r1.attendance_day.sign_out is not None :
       r1_a_out = datetime.datetime.combine(tem_date,r1.attendance_day.sign_out)
      a_s_out_max = datetime.datetime.combine(tem_date,a_s.regular_sign_out_max)


      #该天实际未上班的总时间,返回一个timedelta对象
      missed_time_total = ( r1_a_in - a_s_in_min ) + (r1_a_out - a_s_out_max)
      
      #timedelta的原型
      #class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
      #该天迟到并早退，或者实际未上班总时间超过规定小时，则记为旷工
      if (r1.in_condition_status == 'late' and r1.out_condition_status == 'true') or ( missed_time_total > datetime.timedelta( hours =a_s.missed_time_total_max)):
        r1.not_attend = True 
      # 写入数据库
      r1.save() 
      
      #重新读取考勤表数据
      aa = attendances.objects.filter(user_id = request.user.id)

     return render_to_response('attendance_log.html',locals())

 



''' 考勤界面        
           如果时间在   00：00：00 ~ regular_sign_in_max  显示 签到按钮
           如果时间在   regular_sign_out_min ~ 23:59:59   显示 签退按钮

           每天都自动插入对应的 ID+日期的一条记录  u+d
           用户只允许签到一次，使用更新操作，将对应记录中的签到时间更新上
           用户允许签退多次，使用更新操作，将对应记录中的签退时间更新上
           att

'''
@login_required(login_url = '/login/')
def get_attendance(request):
  
    attendances_all = attendance_data.objects.filter(user_id = request.user.id)
    attendance_rela = attendances.objects.filter(user_id = request.user.id)
    user = User.objects.get(id = request.user.id).profile
    try:
      a_s = attendance_standards.objects.get(company_id = user.company)
    except attendance_standards.DoesNotExist:   #DoesNotExist是attendance_standards的一个属性，用于判断是否有数据存在
      print "此用户并没有分配公司"
    else:
      pass
    for a in attendances_all:
      for r in attendance_rela:     
        if a.attendance_day == r.attendance_day.attendance_day:      
           break
      else:    #没有查到记录则创建相应记录
          p = attendances.objects.create(user_id = request.user.id, 
                                   attendance_day_id = a_id,
                                            )
            
 

    # 给更新后的考勤表记录补全数据

  #  attendances_all2 = attendance_data.objects.filter(user_id = request.user.id)
    attendance_rela2 = attendances.objects.filter(user_id = request.user.id)
    try:
      a_s = attendance_standards.objects.get(company_id = user.company)
    except attendance_standards.DoesNotExist:   #DoesNotExist是attendance_standards的一个属性，用于判断是否有数据存在
      print "此用户并没有分配公司"
    else:
      pass

    for r1 in attendance_rela2:
      if r1.attendance_day.sign_in is not None and a_s.regular_sign_in_min <=  r1.attendance_day.sign_in <=  a_s.regular_sign_in_max:
         r1.in_condition_status = 'late'
      else:
         r1.in_condition_status = 'in_attend'
      if r1.attendance_day.sign_out is not None and a_s.regular_sign_out_min <=  r1.attendance_day.sign_out <= a_s.regular_sign_out_max:
         r1.out_condition_status = 'earlyout'
      else:
         r1.out_condition_status = 'out_attend'
      
    #设定临时的日期变量，time类不能相减
      tem_date = datetime.datetime.date(datetime.datetime.now())
      if r1.attendance_day.sign_in is not None :
       r1_a_in = datetime.datetime.combine(tem_date,r1.attendance_day.sign_in)
      a_s_in_min = datetime.datetime.combine(tem_date,a_s.regular_sign_in_min)
      if r1.attendance_day.sign_out is not None :
       r1_a_out = datetime.datetime.combine(tem_date,r1.attendance_day.sign_out)
      a_s_out_max = datetime.datetime.combine(tem_date,a_s.regular_sign_out_max)


      #该天实际未上班的总时间,返回一个timedelta对象
      missed_time_total = ( r1_a_in - a_s_in_min ) + (r1_a_out - a_s_out_max)
      
      #timedelta的原型
      #class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
      #该天迟到并早退，或者实际未上班总时间超过规定小时，则记为旷工
      if (r1.in_condition_status == 'late' and r1.out_condition_status == 'true') or ( missed_time_total > datetime.timedelta( hours =a_s.missed_time_total_max)):
        r1.not_attend = True 
      # 写入数据库
      r1.save() 
      


      


       # b.attendance_day = today
   # if a_attendance
   
    return render_to_response('get_attendance.html',locals())         


'''这里用于根据现有的data数据，判断是否需要创建当天的attendance_data表记录'''

'''

    today = datetime.datetime.date(datetime.datetime.today())
    for aa in attendances_all:
      if aa.attendance_day == today:
          pass
      else:   #自动创建的今天的data实例
         pp = attendance_data.objects.create(user_id = request.user.id,
                                        attendance_day = today
              )
                     '''


                 

#这里用于生成一个打卡状态选项


'''

    now = datetime.datetime.time(datetime.datetime.now())
    earliest_in = datetime.time(00,05,00)
    if   earliest_in   <  now  < a_s.regular_sign_in_max : 
      attend_state = 'in'
    elif a_s.regular_sign_out_min < now < a_s.regular_sign_out_max : 
      attend_state = 'out'
    else :
      attend_state = 'none'
    
'''



   
'''这里用于根据现有的data数据和标准，自动生成该用户对应的考勤表(可能有多个记录未自动生成)，并将数据填入考勤表中'''
  
  

    
      # 查询并创建所有缺失的考勤表记录
    
    



def time(request):
    now = datetime.datetime.now()
    return render_to_response('time.html',locals())
     

