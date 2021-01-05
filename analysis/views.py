from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView, 
    ListView, 
    DetailView, 
    CreateView, 
    View,
    DeleteView,
    )
from scraper.models import Request, Article, Text, ProcessingStatus
from analysis.forms import RequestCreateForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from finance_proj.settings import TEXT_CLEANER, MODEL
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from nltk import tokenize
from django.contrib.auth.mixins import UserPassesTestMixin




class PlaygroundTemplateView(View):
    def get(self, request):
        model_status = ProcessingStatus.objects.get(name="MODEL").status
        if model_status == "BUSY":
            return redirect(reverse_lazy('mainpage'))
        context = {}
        return render(request, 'playground.html', context)




class RequestsView(View):
    def get(self, request, mode):
        context = {
            'range': range(50),
            'mode': mode,
        }
        return render(request, 'requests.html', context)



def change_accessibility(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            mode = request.GET['mode']
            request_index = int(request.GET['request_index'])
            new_privacy = request.GET['new_privacy']
            requests = get_requests(mode, user)

            req = requests[request_index]

            if req.user != user:
                return redirect(reverse_lazy('account_login'))
            req.accessibility = new_privacy
            req.save()
            return redirect(f'/analysis/requests/{mode}')
        else:
            return redirect(reverse_lazy('account_login'))



class RequestDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'request_confirm_delete.html'
    model = Request
    success_url = reverse_lazy('requests')
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    def handle_no_permission(self):
        return redirect(reverse_lazy('account_login'))




class RequestCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        form = RequestCreateForm()
        context = {'form': form}
        return render(request, 'request_create.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = RequestCreateForm(request.POST)
        if form.is_valid():
            req = form.save()
            req.user = user
            req.save()
            return HttpResponseRedirect(reverse_lazy('request_detail', args=[req.id]))
        return render(request, 'request_create.html', {'form': form})





def request_detail_view(request, pk):
    req = Request.objects.get(pk=pk)
    context = {
        'req':req,
        'range':range(50),
        }
    return render(request, 'request_detail.html', context=context)

def article_detail_view(request, pk):
    article = Article.objects.get(pk=pk)
    texts = article.text_set.all()
    context = {
        'article':article,
        'texts':texts,
        'range':range(200)
    }
    return render(request, 'article_detail.html', context=context)



# various Python functions

def get_sentence_html(sentence, prediction):
    if prediction > 0.85:
        return f'<span class="mr-1" style="background-color:#03DF04">{sentence}</span>'
    elif prediction > 0.60:
        return f'<span class="mr-1" style="background-color:#2AED2D">{sentence}</span>'
    elif prediction > 0.45:
        return f'<span class="mr-1" style="background-color:#62F163">{sentence}</span>'
    elif prediction > 0.30:
        return f'<span class="mr-1" style="background-color:#A0F9A0">{sentence}</span>'
    elif prediction > 0.15:
        return f'<span class="mr-1" style="background-color:#D8FCD8">{sentence}</span>'
    elif prediction > 0.00:
        return f'<span class="mr-1" style="background-color:#FFFFFE">{sentence}</span>'
    elif prediction > -0.15:
        return f'<span class="mr-1" style="background-color:#FFDBDD">{sentence}</span>'
    elif prediction > -0.30:
        return f'<span class="mr-1" style="background-color:#F6BDC0">{sentence}</span>'
    elif prediction > -0.45:
        return f'<span class="mr-1" style="background-color:#F1959B">{sentence}</span>'
    elif prediction > -0.60:
        return f'<span class="mr-1" style="background-color:#F07470">{sentence}</span>'
    elif prediction > -0.85:
        return f'<span class="mr-1" style="background-color:#EA4C46">{sentence}</span>'
    else:
        return f'<span class="mr-1" style="background-color:#DC1C13">{sentence}</span>'



def get_playground_html(data):
    html = '<p>'
    end_p = '</p>'
    try:
        sentences, sequences = TEXT_CLEANER.get_cleaned_element(data)
        predictions = list(map(lambda x: MODEL.predict(x), sequences))
        for sentence, prediction in zip(sentences, predictions):
            prediction = prediction[0][0] - prediction[0][2]
            sentence_html = get_sentence_html(sentence, prediction)
            html += sentence_html
    except: pass


    html += end_p
    return html



def get_requests(mode, user):
        if mode == "PRIVATE":
            return Request.objects.filter(user=user, accessibility='Private')
        elif mode == "PUBLIC":
            return Request.objects.filter(accessibility='Public')
        elif mode == "PUBLICOWN":
            return Request.objects.filter(user=user, accessibility='Public')
        elif mode == "OWN":
            return Request.objects.filter(user=user)



# Javascript related functions


@csrf_exempt
def refresh_processor_status(request):
    if request.method == "POST":
        try: scraper_status = ProcessingStatus.objects.get(name='SCRAPER').status
        except: scraper_status = 'FREE'
        try: model_status = ProcessingStatus.objects.get(name='MODEL').status
        except: model_status = 'FREE'  
        data = {'scraper_status':scraper_status, 
                'model_status':model_status,
                }
        return JsonResponse(data, status=201, safe=False)      



@csrf_exempt
def article_detail_html(request):
    if request.method == 'POST':
        tag = request.POST['tag']
        text = request.POST['text']
        position = request.POST['position']
        text_html = get_playground_html(text)
        final_text_html = f'<{tag}>{text_html}</{tag}>'
        return JsonResponse({'final_text_html':final_text_html,'position':position}, status=201, safe=False)





@csrf_exempt
def playground(request):
    if request.method == 'POST':
        data = request.POST['text']
        html = get_playground_html(data)
        print(html)
        return JsonResponse({'html':html}, status=201, safe=False)





@csrf_exempt
def refresh_requests_status(request):
    if request.method == 'POST':
        mode = request.POST['mode']
        user = request.user
        requests = get_requests(mode, user)
        statuses = [req.status for req in requests]
        data = {'statuses':statuses}
        return JsonResponse(data, status=201, safe=False)

@csrf_exempt
def refresh_request_status(request):
    if request.method == 'POST':

        request_pk = request.POST.get('request_pk')
        req = Request.objects.get(pk=request_pk)
        articles = req.article_set.all()
        statuses = [article.status for article in articles]
        data = {'statuses':statuses}
        return JsonResponse(data, status=201, safe=False)

@csrf_exempt
def refresh_article_status(request):
    if request.method == 'POST':

        article_pk = request.POST['article_pk']
        article = Article.objects.get(pk=article_pk)
        texts = article.text_set.all()
        statuses = [text.status for text in texts]
        data = {'statuses':statuses,}
        return JsonResponse(data, status=201, safe=False)




@csrf_exempt
def requests_load_initial_content(request):
    if request.method == 'POST':
        mode = request.POST['mode']
        user = request.user
        requests = get_requests(mode, user)
        requests_len = len(requests)
        return JsonResponse({'requests_len':requests_len}, status=201, safe=False)

@csrf_exempt
def request_load_initial_content(request):
    if request.method == 'POST':
        articles_len = len(Request.objects.get(pk=request.POST['request_pk']).article_set.all())
        return JsonResponse({'articles_len':articles_len}, status=201, safe=False)

@csrf_exempt
def article_load_initial_content(request):
    if request.method == 'POST':
        texts_len = len(Article.objects.get(pk=request.POST['article_pk']).text_set.all())
        return JsonResponse({'texts_len':texts_len}, status=201, safe=False)       




@csrf_exempt
def load_requests_request_content(request):
    mode = request.POST['mode']
    user = request.user
    request_index = int(request.POST['request_index'])
    requests = get_requests(mode, user)
    req = model_to_dict(requests[request_index])
    return JsonResponse({'req':req, 'request_index':request_index}, status=201, safe=False)

@csrf_exempt
def load_request_article_content(request):
    if request.method == 'POST':
        article_index = int(request.POST['article_index'])
        request_pk = request.POST['request_pk']
        req_articles = Request.objects.get(pk=request_pk).article_set.all()
        article = model_to_dict(req_articles[article_index])
        return JsonResponse({'article':article, 'article_index':article_index}, status=201, safe=False)

@csrf_exempt
def load_article_text_content(request):
    if request.method == 'POST':
        text_index = int(request.POST['text_index'])
        article_pk = request.POST['article_pk']
        article_texts = Article.objects.get(pk=article_pk).text_set.all()
        text = model_to_dict(article_texts[text_index])
        sentences = tokenize.sent_tokenize(text['text'])
        if text['sentiment']:
            predictions = text['sentiment'].split(',')
            predictions = list(map(lambda x: float(x), predictions))
            text['text'] = ' '.join([get_sentence_html(sentence, prediction) for sentence, prediction in zip(sentences, predictions)])
        return JsonResponse({'text':text, 'text_index':text_index}, status=201, safe=False)




@csrf_exempt
def change_model_status_js(request):
    if request.method == 'POST':
        status = request.POST['status']
        print(status)
        model_status = ProcessingStatus.objects.get(name='MODEL')
        model_status.status = status
        model_status.save()
        data = {
            'status':model_status.status,
        }
        return JsonResponse(data, status=201, safe=False)
        

@csrf_exempt
def text_example_js(request):
    if request.method == 'POST':
        print('Im here')
        example_id = request.POST['button_id']
        print(example_id)

        if example_id == 'example-1':
            example_text = '''\
Alas, the COVID-19 pandemic has threatened to undermine the good work the industry did. Airline revenue fell 90% year over year during the second quarter of 2020 as the pandemic dried up travel demand. Few businesses can survive that sort of revenue drop, and most airline stocks lost 50% or more of their value as the pandemic spread globally.

The good news is that no U.S. airline has had to declare bankruptcy to date. The industry in the first half of 2020 raised more than $50 billion in private funding, alongside a similar amount of government assistance, to help weather the storm. But with travel volumes expected to take years to return to pre-pandemic levels, investors buying in now will be waiting on a multiyear turnaround even in the best-case scenario.
'''
        elif example_id == 'example-2':
            example_text = '''\
It was a rocky first trading day of the year for Wall Street as stocks fell sharply and investors grew worried about the the pandemic and the economic recovery in 2021.

Investors took profits off the market's record highs set last week, and they took a more cautious position ahead of the high-stakes runoff election in Georgia Tuesday, which will decide the balance in the Senate, analysts said.

Wall Street had started the day in the green, putting stocks on track to start the New Year off with a bang. The Dow (INDU) and the S&P 500 (SPX) finished at record highs on the last trading day of 2020. But trading quickly turned south Monday.
'''
        elif example_id == 'example-3':
            example_text = '''\
Less than three weeks ago, a new variant of the SARS-CoV-2 virus, which causes COVID-19, was identified in the United Kingdom. The mutability of the virus has the potential to cause serious problems. For example, differences in transmission or mortality rate could induce strict lockdowns that further ravage the economy. It's also possible that emergency use-approved and experimental vaccines may prove ineffective or less effective against new variants of the virus. 
'''
        print(example_text)
        data = {"example_text": example_text}
        return JsonResponse(data, status=201, safe=False)