from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


@login_required(login_url="signin")
def index(request):
    user = request.user
    tag_questions = TagQuestions.objects.filter(is_active=True)
    participated_votes = Vote.objects.filter(user=user, tag_question__in=tag_questions).values_list('tag_question_id', flat=True)
    remaining_tag_questions = tag_questions.exclude(id__in=participated_votes)
    return render(request, 'index.html', {'tag_questions': remaining_tag_questions})


@login_required(login_url="signin")
def vote_detail(request, tag_question_id):
    tag_question = get_object_or_404(TagQuestions, pk=tag_question_id)
    faculties = Faculty.objects.all()
    return render(request, 'vote_detail.html', {'faculties': faculties,
                                                "tag_question": tag_question})


@login_required(login_url="signin")
def vote(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    faculties = Faculty.objects.all()
    context = {
        'professor': professor,
        'faculties': faculties,
    }
    return render(request, 'vote.html', context)



def result(request, slug):
    category = Category.objects.get(slug=slug)
    items = CategoryItem.objects.filter(category=category)
    context = {"category": category, "items": items}
    return render(request, "result.html", context)


def signin(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("index")
        else:
            msg = "Invalid Credentials"

    context = {"msg": msg}
    return render(request, "signin.html", context)


def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # login starts here
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    context = {"form": form}
    return render(request, "signup.html", context)


def signout(request):
    logout(request)
    return redirect("index")


def professor_list(request, kafedra_id, tag_question_id):
    tag_question = get_object_or_404(TagQuestions, pk=tag_question_id)
    professors = Professor.objects.filter(kafedra_id=kafedra_id)
    return render(request, 'professors.html', {'professors': professors,
                                               'tag_question': tag_question})


def vote_item(request, professor_id, tag_question_id):
    professor = get_object_or_404(Professor, id=professor_id)
    tag_question = get_object_or_404(TagQuestions, pk=tag_question_id)
    return render(request, 'vote_item.html', {'professor': professor,
                                              'tag_question': tag_question})



def submit_vote(request):
    if request.method == 'POST':
        print(request.POST)
        return redirect('index')
    else:
        pass

@staff_member_required
def statistics(request):
    professors = Professor.objects.all()
    tag_questions = TagQuestions.objects.filter(is_active=True)
    vote_data = []
    for professor in professors:
        professor_votes = Vote.objects.filter(professor=professor)
        for tag_question in tag_questions:
            vote_count = professor_votes.filter(tag_question=tag_question).count()
            vote_data.append({
                'professor': professor.name,
                'tag_question': tag_question.name,
                'vote_count': vote_count
            })
    return render(request, 'statistics.html', {'vote_data': vote_data})