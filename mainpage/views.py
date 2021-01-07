from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View, CreateView, DeleteView, UpdateView

# Create your views here.
class MainpageTemplateView(TemplateView):
    template_name = 'mainpage.html'

class ContactTemplateView(TemplateView):
    template_name = 'contact.html'