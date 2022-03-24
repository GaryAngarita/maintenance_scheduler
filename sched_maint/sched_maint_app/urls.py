from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('setup', views.setup),
    path('add_maint/<int:instance_id>', views.add_maint),
    path('next_page/<int:instance_id>', views.next_page),
    path('logout', views.logout),
]