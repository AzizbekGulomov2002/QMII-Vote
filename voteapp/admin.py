from django.contrib import admin
from .models import *



@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Kafedra)
class KafedraAdmin(admin.ModelAdmin):
    list_display = ['name', 'faculty']

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['name', 'kafedra', 'work_year', 'stuff']
    list_filter = ['kafedra']
    search_fields = ['name', 'stuff']



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ['item']

@admin.register(TagQuestions)
class TagQuestionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'finish', 'is_active']
    filter_horizontal = ['questions']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'professor', 'user', 'tag_question']
