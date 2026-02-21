from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('quiz/<uuid:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<uuid:quiz_id>/preview/', views.preview_quiz, name='preview_quiz'),
    path('quiz/<uuid:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/<uuid:quiz_id>/nudge/', views.nudge_quiz, name='nudge_quiz'),
    path('result/<uuid:result_id>/', views.view_result, name='view_result'),
]
