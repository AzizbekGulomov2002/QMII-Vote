from django.urls import path 
from . import views 
from voteapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path("", views.index, name="index"),
     path('vote/<int:vote_id>/', views.vote_detail, name='vote_detail'),
     path('vote_item/<int:professor_id>/', views.vote_item, name='vote_item'),

     path('statistics/', views.statistics, name='statistics'),

     path('professors/<int:kafedra_id>/', views.professor_list, name='professors'),
     path('vote/<int:professor_id>/', views.vote, name='vote'),
     path('vote/', views.vote, name='vote'),
     

     
     # path("vote/<str:slug>", views.detail, name="detail"),
     path("result/<str:slug>", views.result, name="result"),
     path("result", views.result, name="result"),
     path("signin", views.signin, name= "signin"),
     path("signup", views.signup, name="signup"),
     path("logout", views.signout, name="logout")
     
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)