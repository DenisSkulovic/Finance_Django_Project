from django.shortcuts import render
from django.views.generic import TemplateView


class PortfolioTemplateView(TemplateView):
    template_name = 'portfolio.html'
    