from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from portfolio.models import Ticker
from yfinance_functions import store_ticker_info
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



class TickerDetailView(View):
    def get(self, request, symbol):
        data = Ticker.objects.get(symbol=symbol)

        context = {
            "data": data,
        }
        return render(request, 'ticker_detail.html', context)


    
class PortfolioTemplateView(TemplateView):
    template_name = 'portfolio.html'



@csrf_exempt
def get_updated_ticker_data(request):
    symbol = request.POST.get('symbol')
    store_ticker_info([symbol])
    ticker = Ticker.objects.get(symbol=symbol)
    data = model_to_dict(ticker)
    return JsonResponse(data)
    

# @csrf_exempt
# def run_task(request):
#     if request.POST:
#         task_symbol = request.POST.get("symbol")
#         return JsonResponse({"task_symbol": task_symbol}, status=202)

# def get_status(request, task_id):
#     return JsonResponse({"task_id": task_id}, status=200)