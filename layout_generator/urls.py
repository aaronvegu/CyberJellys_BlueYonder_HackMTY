from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='layout-home'),
    path('generate_layout',  views.generate_initial_grid, name='layout-generate'),
    path('calculated_layout', views.generated_layout, name='layout-calculated'),
]