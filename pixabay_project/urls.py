from django.urls import path
from base import views

urlpatterns = [
    path('', views.image_gallery, name='image_gallery'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
    path('download/<int:image_id>/', views.download_image, name='download_image'),
]
