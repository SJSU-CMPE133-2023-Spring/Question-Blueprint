from django.urls import path
from .views import home
app_name = 'question_blueprint'


urlpatterns = [
    path('', home, name='home'),
]