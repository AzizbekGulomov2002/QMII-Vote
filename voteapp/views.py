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
    tag_questions = TagQuestions.objects.all()
    return render(request, 'index.html', {'tag_questions': tag_questions})

@login_required(login_url="signin")
def vote_detail(request, tag_question_id):
    # Assuming tag_question_id is used to retrieve faculties, update it if necessary
    faculties = Faculty.objects.all()
    return render(request, 'vote_detail.html', {'faculties': faculties})
    

@login_required(login_url="signin")
def vote(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    faculties = Faculty.objects.all()
    context = {
        'professor': professor,
        'faculties': faculties,
    }
    return render(request, 'vote.html', context)

# def vote_item(request, professor_id):
#     if request.method == 'POST':
#         professor = Professor.objects.get(pk=professor_id)
#         selected_options = request.POST.dict()
#         user = request.user
#         if Result.objects.filter(professor=professor, user=user).exists():
#             messages.error(request, "You have already voted for this professor.")
#             return redirect('index')
#         for item_id, option_id in selected_options.items():
#             if item_id.startswith('selected_option_'):
#                 item_id = int(item_id.split('_')[-1])
#                 option_id = int(option_id)
#                 item = professor.voteitems_set.get(pk=item_id)
#                 selected_option = item.options.get(pk=option_id)
#                 Result.objects.create(professor=professor, user=user, selected_option=selected_option)
#         return redirect('index')
#     professor = Professor.objects.get(pk=professor_id)
#     return render(request, 'vote_item.html', {'professor': professor})

@staff_member_required
def statistics(request):
    user_results = Statistics.objects.all()
    print(user_results)
    return render(request, 'statistics.html', {'user_results': user_results})

# def professor_list(request, kafedra_id):
#     professors = Professor.objects.filter(kafedra_id=kafedra_id)
#     return render(request, 'professors.html', {'professors': professors})

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
            
    context = {"msg":msg}
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
    context = {"form":form}
    return render(request, "signup.html", context)

def signout(request):
    logout(request)
    return redirect("index")



def professor_list(request, kafedra_id):
    professors = Professor.objects.filter(kafedra_id=kafedra_id)
    return render(request, 'professors.html', {'professors': professors})

def vote_item(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    vote = professor.votes.first()
    if vote:
        tag_question = vote.tag_question
        return render(request, 'vote_item.html', {'professor': professor, 'tag_question': tag_question})
    else:
        return render(request, 'vote_item.html', {'professor': professor})


def submit_vote(request, professor_id):
    if request.method == 'POST':
        professor = get_object_or_404(Professor, id=professor_id)
        # Here you can process the form submission, save the vote, etc.
        # For now, let's just redirect to the index page after voting
        return redirect('index')
    else:
        # Handle GET request appropriately, maybe render an error page
        pass