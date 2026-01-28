from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('<uuid:public_id>/', views.landing_page, name='landing_page'),
]
