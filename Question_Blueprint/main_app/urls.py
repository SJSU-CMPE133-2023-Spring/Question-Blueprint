from django.urls import path
from .views import home
app_name='main_app'


urlpatterns = [
    path('', home, name='home'),
]