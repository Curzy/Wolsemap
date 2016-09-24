from django.shortcuts import render
from django.views import generic


# Create your views here.


class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html')


class WolseMapView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='wolsemap.html')
