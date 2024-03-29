from django.urls import path 
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from .views import professor_list, vote_item
from .views import statistics
urlpatterns = [
    path("", views.index, name="index"),
    # path('vote/<int:professor_id>/', views.vote_detail, name='vote_detail'),
    path('vote_detail/<int:tag_question_id>/', views.vote_detail, name='vote_detail'),

    path('submit_vote/', views.submit_vote, name='submit_vote'),

    path('professors/', professor_list, name='professor_list'),
    path('vote/<int:professor_id>/<int:tag_question_id>/', vote_item, name='vote_item'),

    path('statistics/', statistics, name='statistics'),
    path('professors/<int:kafedra_id>/<int:tag_question_id>/', views.professor_list, name='professors'),




    
    path("result/<str:slug>", views.result, name="result"),
    path("result", views.result, name="result"),
    path("signin", views.signin, name="signin"),
    path("signup", views.signup, name="signup"),
    path("logout", views.signout, name="logout")
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
