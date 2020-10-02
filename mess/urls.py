from django.urls import path
from . import views

app_name = 'mess'

urlpatterns = [
    path('', views.index, name='index'),
    path('wardenpageauthenticate/', views.wardenpageauthenticate, name='wardenpageauthenticate'),
    path('studentpageauthenticate/', views.studentpageauthenticate, name='studentpageauthenticate'),
    path('studentpage/<int:id>', views.studentpage, name='studentpage'),
    path('wardenpage/<int:id>', views.wardenpage, name='wardenpage'),
    path('studentpage/<int:id>/logout/', views.logout_view, name='logout'),
    path('wardenpage/<int:id>/logout/', views.logout_view, name='logout')
]