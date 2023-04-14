from django.urls import path
from . import views
app_name='main_app'


urlpatterns = [
    path('', views.home, name='home'),
    path('question/', views.QuestionListView.as_view(), name='question_view'),
    path('question/ask/', views.QuestionCreateView.as_view(), name='question_ask_view'),

]