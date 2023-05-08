from django.urls import path
from . import views
app_name='main_app'


urlpatterns = [
    path('', views.home, name='home'),
    path('question/', views.QuestionListView.as_view(), name='question_view'),
    path('question/ask/', views.QuestionCreateView.as_view(), name='question_ask_view'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail_view'),
    path('question/<int:pk>/update', views.QuestionUpdateView.as_view(), name='question_update_view'),
    path('question/<int:pk>/delete', views.QuestionDeleteView.as_view(), name='question_delete_view'),
    path('question/<int:pk>/upvote', views.upvote, name='upvote'),

    path('question/<int:pk>/answer/', views.AnswerAddView.as_view(), name='answer_create_view'),
    path('search/', views.search, name='search'),

]