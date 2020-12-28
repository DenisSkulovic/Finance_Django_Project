from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

class AnalysisTemplateView(TemplateView):
    template_name = 'analysis.html'