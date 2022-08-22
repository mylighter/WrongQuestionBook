from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Folder(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ChoiceQuestion(models.Model):
    stem = models.CharField(max_length=150)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    multiple = models.BooleanField(default=False)


class Choice(models.Model):
    content = models.CharField(max_length=40)
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    correct = models.BooleanField()


class Completion(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    stem = models.CharField(max_length=200)


class Answer(models.Model):
    question = models.ForeignKey(Completion, on_delete=models.CASCADE)
    content = models.CharField(max_length=40)


class AnswerSheet(models.Model):
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    used_time = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)


class UserChoiceQuestionAnswer(models.Model):
    sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE)
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)


class UserChoiceAnswer(models.Model):
    question = models.ForeignKey(UserChoiceQuestionAnswer, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


class UserCompletionQAnswer(models.Model):
    sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE)
    question = models.ForeignKey(Completion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=40)
    correct = models.BooleanField(default=False)


class Log(models.Model):
    date_updated = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=10)
    content = models.CharField(max_length=80)


class Image(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=50)
    image = models.ImageField(upload_to='upload')
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
