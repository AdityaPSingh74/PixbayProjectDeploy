from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
API_KEY = '46078793-e7d124ea44e3dd5e5cfb5a827'

def fetch_images(query=None):
    url = 'https://pixabay.com/api/'
    
        
    params = {
        'key': API_KEY,
        'q': query if query else 'nature',  
        'image_type': 'photo',
        'per_page': 12,     
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get('hits', [])
    return []


def image_gallery(request):
    query = request.GET.get('q')
    images = fetch_images(query=query)
    return render(request, 'base/gallery.html', {'images': images})

def image_detail(request, image_id):
    url = f'https://pixabay.com/api/?key={API_KEY}&id={image_id}'
    response = requests.get(url)
    if response.status_code == 200:
        image = response.json().get('hits', [])[0]  
        return render(request, 'base/image_detail.html', {'image': image})
    return render(request, 'base/image_detail.html', {'error': 'Image not found'})

import requests
from django.http import HttpResponse

def download_image(request, image_id):
    url = f'https://pixabay.com/api/?key={API_KEY}&id={image_id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        image = response.json().get('hits', [])[0]
        image_url = image['largeImageURL']
        
        image_response = requests.get(image_url)
        
        content_type = image_response.headers['Content-Type']
        
        response = HttpResponse(image_response.content, content_type=content_type)
        
        response['Content-Disposition'] = f'attachment; filename="{image["user"]}_{image_id}.jpg"'
        
        return response
    else:
        return HttpResponse("Error: Unable to download image.", status=404)
