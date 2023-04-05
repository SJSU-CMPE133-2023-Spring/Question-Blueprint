from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.TextField(max_length=20000, blank=False, null=False)
    tag = TaggableManager(blank=True)
    upvote_num = models.IntegerField(default=0)

    def __str__(self):
        return f'Question of {self.user.username}'
    
    #  to get the URL of the object's detail view.
    def get_absolute_url(self):
        pass

    def update_vote_num(self):
        pass


"""
class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_vote')
    is_upvote = models.BooleanField(default=True)

    class Meta:
        abstract = True

class QuestionUpvote(Upvote):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_vote')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.question.update_upvote_num()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.question.update_upvote_num()

class AnswerUpvote(Upvote):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_vote')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.answer.update_upvote_num()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.answer.update_upvote_num()


"""