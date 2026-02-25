"""Puutarhapäiväkirjan URL-reitit."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.EtusivuView.as_view(), name='etusivu'),
    path('kasvit/', views.KasvilistaView.as_view(), name='kasvilista'),
    path('kasvit/lisaa/', views.LisaaKasvilajiView.as_view(), name='lisaa_kasvilaji'),
    path('puutarha/lisaa/', views.LisaaViljelyView.as_view(), name='lisaa_viljely'),
    path('puutarha/<int:pk>/', views.ViljelyDetailView.as_view(), name='viljely_detail'),
    path('puutarha/<int:pk>/tila/', views.VaihdaTilaView.as_view(), name='vaihda_tila'),
]
