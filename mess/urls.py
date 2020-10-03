from django.urls import path
from . import views

app_name = 'mess'

urlpatterns = [
    path('', views.index, name='index'),
    path('wardenpageauthenticate/', views.wardenpageauthenticate, name='wardenpageauthenticate'),
    path('studentpageauthenticate/', views.studentpageauthenticate, name='studentpageauthenticate'),
    path('studentpage/<str:id>/', views.studentpage, name='studentpage'),
    path('wardenpage/<str:warden_id>/', views.wardenpage, name='wardenpage'),
    path('studentpage/<str:id>/logout/', views.logout_view, name='logout'),
    path('wardenpage/<str:warden_id>/logout/', views.logout_view1, name='logout1'),
    path('mess/<str:mess>/', views.mess, name='mess'),
    path('mess/<str:mess>/update', views.update, name='update')
]