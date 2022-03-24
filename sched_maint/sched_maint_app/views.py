import datetime
from django.shortcuts import render, redirect
from .models import *

def index(request):
    return render(request, 'homepage.html')

def setup(request):
    instance = Instance.objects.create(maintenance = request.POST['maintenance']) 
    timing = Timing.objects.create(interval = request.POST['interval'], instance = instance)
    request.session['instance'] = instance.id
    print(instance)
    print(timing)
    return redirect(f'/add_maint/{instance.id}')

def add_maint(request, instance_id):
    if 'instance' in request.session:
        instance = Instance.objects.get(id = instance_id)
        timing = Timing.objects.get(instance = instance)
        context = {
            'instances': Instance.objects.all(),
            # 'timing': timing,
            'timings': Timing.objects.all()
        }
        return render(request, 'homepage.html', context)

def next_page(request, instance_id):
    if 'instance' in request.session:
        activity = ""

        instances = Instance.objects.get(id = instance_id)
        single_interval = instances.interval
        single_instance = request.session['instance']
        # each_int = Instance.objects.get(id = single_instance)

        curr_date_temp = datetime.datetime(2022, 3, 22)
        full_date = curr_date_temp.strftime("%b %d %Y")
        # today = datetime.today()
        for single_interval in instances:
            print(single_interval)
            new_date = full_date - datetime.timedelta(days=single_interval)
            if new_date <= 3:
                str = "The time is now"
            elif new_date <= 7:
                str = "Within a week"
            elif new_date <= 15:
                str = "About two weeks left"
            elif new_date <= 30:
                str = "Just about a month. Getting close"
            else:
                str = "Plenty of time"

        activity.append(0, str)
        context = {
            "current": full_date,
            "instances": instances,
            # "today": today,
            "activity": activity
        }
        return render(request, "calendar.html", context)
    else:
        return render('/')

def logout(request):
    request.session.flush()
    return redirect('/')
# Create your views here.





# NEED TO ADD INTERVAL PATH IN VIEWS