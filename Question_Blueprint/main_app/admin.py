from django.contrib import admin
from .models import Question, QuestionUpvote, Answer, AnswerUpvote

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionUpvote)
admin.site.register(Answer)
admin.site.register(AnswerUpvote)