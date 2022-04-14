from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logreg', views.logreg),
    path('register', views.register),
    path('login', views.login),
    path('instance/<int:user_id>', views.instance),
    path('delete/<int:instance_id>', views.delete),
    path('edit_page/<int:instance_id>', views.edit_page),
    path('update/<int:instance_id>', views.update),
    path('start_maint/<int:user_id>', views.start_maint),
    path('next_page/<int:user_id>', views.next_page),
    path('logout', views.logout),
]