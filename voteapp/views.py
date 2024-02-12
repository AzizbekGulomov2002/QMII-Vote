from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

def index(request):
    vote = Vote.objects.all()
    contex = {
        'Vote':vote,
    }
    return render(request, ['index.html'] , contex)

                  
def professor_list(request, kafedra_id):
    professors = Professor.objects.filter(kafedra_id=kafedra_id)
    return render(request, 'professors.html', {'professors': professors})

@login_required(login_url="signin")
def vote_detail(request, vote_id):
    vote = Vote.objects.get(pk=vote_id)
    faculties = Faculty.objects.filter(vote=vote)
    for faculty in faculties:
        professors_count = Professor.objects.filter(kafedra__faculty=faculty).count()
        setattr(faculty, 'professors_count', professors_count)
    return render(request, 'vote_details.html', {'vote': vote, 'faculties': faculties})


def vote(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    
    # Foydalanuvchining ovoz berish ma'lumotini tekshiramiz
    user = request.user
    if Result.objects.filter(professor=professor, user=user).exists():
        messages.error(request, "Siz allaqachon ro'yxatdan o'tgan ekansiz.")
        return redirect('index')
    
    # Professor ma'lumotlarini olish
    vote_items = VoteItems.objects.filter(professor=professor)
    
    context = {
        'professor': professor,
        'vote_items': vote_items,
    }
    return render(request, 'vote.html', context)


def vote_item(request, professor_id):
    if request.method == 'POST':
        professor = Professor.objects.get(pk=professor_id)
        selected_options = request.POST.dict()
        user = request.user
        if Result.objects.filter(professor=professor, user=user).exists():
            messages.error(request, "You have already voted for this professor.")
            return redirect('index')
        for item_id, option_id in selected_options.items():
            if item_id.startswith('selected_option_'):
                item_id = int(item_id.split('_')[-1])
                option_id = int(option_id)
                item = professor.voteitems_set.get(pk=item_id)
                selected_option = item.options.get(pk=option_id)
                Result.objects.create(professor=professor, user=user, selected_option=selected_option)
        return redirect('index')
    professor = Professor.objects.get(pk=professor_id)
    return render(request, 'vote_item.html', {'professor': professor})


# def vote_item(request, professor_id):
#     professor = get_object_or_404(Professor, pk=professor_id)
#     return render(request, 'vote_item.html', {'professor': professor})


@staff_member_required
def statistics(request):
    user_results = Statistics.objects.all()
    print(user_results)
    return render(request, 'statistics.html', {'user_results': user_results})
    



@login_required(login_url="signin")
def detail(request, slug):
    category = Category.objects.get(slug=slug)
    categories = CategoryItem.objects.filter(category=category)
    msg = None
    if request.user.is_authenticated:
        if category.voters.filter(id=request.user.id).exists():
            msg = "voted"
            
    if request.method == 'POST':
        selected_id = request.POST.get("category_item")
        print(selected_id)
        item = CategoryItem.objects.get(id=selected_id)
        item.total_vote += 1
        
        item_category = item.category 
        item_category.total_vote += 1
        
        item.voters.add(request.user)
        item_category.voters.add(request.user)
        
        item.save()
        item_category.save()
        
        return redirect("result", slug=category.slug)
        
    
    context = {"category": category, "categories": categories, "msg": msg}
    return render(request, "detail.html", context)










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

