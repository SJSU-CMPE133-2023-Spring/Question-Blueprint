from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils import timezone
from django.urls import reverse



# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.TextField(max_length=20000, blank=False, null=False)
    tag = TaggableManager(blank=True)
    upvote_num = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)


    def __str__(self):
        return f'Question of {self.user.username}'
    
    #  to get the URL of the object's detail view.
    def get_absolute_url(self):
        return reverse('main_app:question_detail_view', kwargs={'pk':self.pk})

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    def update_upvote_num(self):
        self.upvote_num = self.question_vote.filter(is_upvote=True).count() - self.question_vote.filter(is_upvote=False).count()
        self.save()



class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answer", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    upvote_num = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.question.title}-{self.question.user}"
    
    def get_absolute_url(self):
        return reverse('question_blueprint:question_detail_view', kwargs={'pk':self.pk})
    

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    def update_upvote_num(self):
        self.upvote_num = self.answer_vote.filter(is_upvote=True).count() - self.answer_vote.filter(is_upvote=False).count()
        self.save()


class Upvote(models.Model):
    is_upvote = models.BooleanField(default=True)

    class Meta:
        abstract = True

class QuestionUpvote(Upvote):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_vote')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_vote')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.question.update_upvote_num()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.question.update_upvote_num()


class AnswerUpvote(Upvote):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_vote')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_vote')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.answer.update_upvote_num()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.answer.update_upvote_num()
