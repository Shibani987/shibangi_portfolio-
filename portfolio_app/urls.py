from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("highlights/", views.highlights, name="highlights"),
    path("highlights/<int:pk>/", views.highlight_detail, name="highlight_detail"),
    path("highlights/<int:pk>/like/", views.like_highlight, name="like_highlight"),
    path("products/<slug:slug>/", views.product_page, name="product_page"),
]
