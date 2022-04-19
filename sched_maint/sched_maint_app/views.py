from datetime import datetime
from datetime import timedelta
from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *

def index(request):
    return render(request, 'index.html')

def logreg(request):
    return render(request, 'logreg.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/logreg')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(password)
        print(pw_hash)
        user = User.objects.create(first_name = request.POST['first_name'], 
        last_name = request.POST['last_name'], 
        email = request.POST['email'], 
        password = pw_hash)
        messages.success(request, "Registration successful!")
        request.session['id'] = user.id
    return redirect(f'/start_maint/{user.id}')

def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.log_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/logreg')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(password)
        print(pw_hash)
        user = User.objects.get(email = request.POST['email'])
        request.session['id'] = user.id
        return redirect(f'/start_maint/{user.id}')

def start_maint(request, user_id):
    if 'id' in request.session:
        user = User.objects.get(id = user_id)
        context = {
            'user': user
        }
        return render(request, 'homepage.html', context)
    else:
        return redirect('/')

def instance(request, user_id):
    if 'id' in request.session:        
        user = User.objects.get(id = user_id)
        request.session['id'] = user.id
        errors = Instance.objects.inst_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/start_maint/{user.id}')
        else:
            print("passed validation")
            instance = Instance.objects.create(owner = request.POST['owner'], 
            maintenance = request.POST['maintenance'], 
            interval = request.POST['interval'],
            date_due = date.today() + timedelta(days=int(request.POST['interval'])), 
            status = "", 
            user = user)
            print(f"Today is {datetime.today()}")
            print(f"Due date is {instance.date_due}")
            request.session['instance'] = instance.id
            return redirect(f'/start_maint/{user.id}')
    else:
        return redirect('/logreg')

def delete(request, instance_id):
    user = User.objects.get(id = request.session['id'])
    indiv_inst = Instance.objects.get(id = instance_id)
    indiv_inst.delete()
    request.session['id'] = user.id
    return redirect(f'/start_maint/{user.id}')

def edit_page(request, instance_id):
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])
        instance = Instance.objects.get(id = instance_id)
        context = {
            "user": user,
            "instance": instance
        }
        return render(request, "update.html", context)
    else:
        return redirect('/logreg')

def update(request, instance_id):
    errors = Instance.objects.edit_validator(request.POST)
    if errors:
        instance = Instance.objects.get(id = instance_id)       
        request.session['instance'] = instance.id
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_page/{instance.id}')
    else:
        inst = Instance.objects.get(id = instance_id)
        user = User.objects.get(id = request.session['id'])
        inst.owner = request.POST['owner']
        inst.maintenance = request.POST['maintenance']
        inst.interval = request.POST['interval']
        inst.date_due = date.today() + timedelta(days=int(request.POST['interval']))
        inst.save()
        request.session['id'] = user.id
        return redirect(f'/start_maint/{user.id}')

# Need to fix activity.status update problem


def next_page(request, user_id):
    if 'id' in request.session:
        user = User.objects.get(id = user_id)
        today = date.today()
        for instance in user.user_insts.all():
            print(instance.id)
            new_date = (instance.date_due - today).days
            if new_date < 0:
                str = "It's past due. Get on it!"
            elif new_date == 0:
                str = "Today's the day. Make it happen"
            elif new_date <= 3:
                str = "The time is now"
            elif new_date <= 7:
                str = "Within a week"
            elif new_date <= 15:
                str = "Under two weeks left"
            elif new_date <= 30:
                str = "Just about a month. Getting close"
            else:
                str = "Plenty of time"
            print(new_date)
            print(instance.status)
            instance.status = str
            instance.save()
        context = {
            'user': user,
            "current": today,
            "new_date": new_date
        }
        return render(request, "calendar.html", context)
    else:
        return render('/')

def logout(request):
    request.session.flush()
    return redirect('/')
# Create your views here.





# NEED TO ADD INTERVAL PATH IN VIEWS