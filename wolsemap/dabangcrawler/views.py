from django.shortcuts import render, get_object_or_404
# Create your views here.

def wolsemap(request):
    return render(request, 'wolsemap.html')