from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


# Create your models here.

class Faculty(models.Model):
    # vote = models.ForeignKey("Vote", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Kafedra(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.faculty.name} | {self.name}"


class Professor(models.Model):
    photo = models.ImageField(upload_to='images')
    name = models.CharField(max_length=200)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE)
    work_year = models.DateField()
    stuff = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=200)
    choices = models.ManyToManyField("Choices", related_name='question')

    def __str__(self):
        return self.name


class Choices(models.Model):
    item = models.CharField(max_length=200)

    def __str__(self):
        return self.item


class TagQuestions(models.Model):
    name = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question, related_name='tag_questions')
    start = models.DateField()
    finish = models.DateField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if isinstance(self.finish, str):
            self.finish = datetime.date.fromisoformat(self.finish)

        if self.finish and self.finish <= datetime.now().date():
            self.is_active = False
        super(TagQuestions, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Choices, on_delete=models.CASCADE)


class Vote(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    tag_question = models.ForeignKey(TagQuestions, on_delete=models.CASCADE, related_name='votes')
    answers = models.ManyToManyField(Answers, related_name='votes')

    def __str__(self):
        return f"Vote for {self.professor.name}"
