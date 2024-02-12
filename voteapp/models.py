from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    total_vote = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, blank=True)
    
    def __str__(self):
        return self.title
    

class CategoryItem(models.Model):
    title = models.CharField(max_length=200)
    total_vote = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    voters = models.ManyToManyField(User, blank=True)
    
    @property
    def percentage_vote(self):
        category_votes = self.category.total_vote 
        item_votes = self.total_vote
        
        if category_votes == 0:
            vote_in_percentage = 0
        
        else:
            vote_in_percentage = (item_votes/category_votes) * 100
            
        return vote_in_percentage
    
    
    def __str__(self):
        return self.title


class Vote(models.Model):
    name = models.CharField(max_length=200)
    start = models.DateField()
    finish = models.DateField()
    
    # def is_active(self):
    #     return self.finish >= timezone.now().date()
    
    def __str__(self):
        return self.name
    

class Faculty(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
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
      


class Option(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class VoteItems(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    options = models.ManyToManyField(Option)  # Changed to ManyToManyField

    def __str__(self):
        return self.professor.name
    


class Statistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s result"