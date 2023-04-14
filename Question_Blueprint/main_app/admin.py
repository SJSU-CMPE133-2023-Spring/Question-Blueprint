from django.contrib import admin
from .models import Question, QuestionUpvote

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionUpvote)