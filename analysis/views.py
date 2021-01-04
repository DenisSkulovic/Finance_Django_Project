from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from scraper.models import Request, Article, Text, ProcessingStatus
from analysis.forms import RequestCreateForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from finance_proj.settings import TEXT_CLEANER, MODEL
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from nltk import tokenize



class PlaygroundTemplateView(TemplateView):
    template_name = 'playground.html'



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



@login_required
def request_detail_view(request, pk):
    req = Request.objects.get(pk=pk)
    print('req: ', req)
    context = {
        'req':req,
        'range':range(50),
        }
    return render(request, 'request_detail.html', context=context)

@login_required
def article_detail_view(request, pk):
    article = Article.objects.get(pk=pk)
    texts = article.text_set.all()
    context = {
        'article':article,
        'texts':texts,
        'range':range(200)
    }
    return render(request, 'article_detail.html', context=context)


def get_sentence_html(sentence, prediction):
    if prediction > 0.85:
        return f'<span style="background-color:#03DF04">{sentence}</span>'
    elif prediction > 0.60:
        return f'<span style="background-color:#2AED2D">{sentence}</span>'
    elif prediction > 0.45:
        return f'<span style="background-color:#62F163">{sentence}</span>'
    elif prediction > 0.30:
        return f'<span style="background-color:#A0F9A0">{sentence}</span>'
    elif prediction > 0.15:
        return f'<span style="background-color:#D8FCD8">{sentence}</span>'
    elif prediction > 0.00:
        return f'<span style="background-color:#FFFFFE">{sentence}</span>'
    elif prediction > -0.15:
        return f'<span style="background-color:#FFDBDD">{sentence}</span>'
    elif prediction > -0.30:
        return f'<span style="background-color:#F6BDC0">{sentence}</span>'
    elif prediction > -0.45:
        return f'<span style="background-color:#F1959B">{sentence}</span>'
    elif prediction > -0.60:
        return f'<span style="background-color:#F07470">{sentence}</span>'
    elif prediction > -0.85:
        return f'<span style="background-color:#EA4C46">{sentence}</span>'
    else:
        return f'<span style="background-color:#DC1C13">{sentence}</span>'



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
def refresh_request_status(request):
    if request.method == 'POST':
        try: scraper_status = ProcessingStatus.objects.get(name='SCRAPER').status
        except: scraper_status = 'FREE'
        try: model_status = ProcessingStatus.objects.get(name='MODEL').status
        except: model_status = 'FREE'

        request_pk = request.POST.get('request_pk')
        req = Request.objects.get(pk=request_pk)
        articles = req.article_set.all()
        statuses = [article.status for article in articles]
        data = {'statuses':statuses, 
                'scraper_status':scraper_status, 
                'model_status':model_status}
        return JsonResponse(data, status=201, safe=False)

@csrf_exempt
def refresh_article_status(request):
    if request.method == 'POST':
        try: scraper_status = ProcessingStatus.objects.get(name='SCRAPER').status
        except: scraper_status = 'FREE'
        try: model_status = ProcessingStatus.objects.get(name='MODEL').status
        except: model_status = 'FREE'

        article_pk = request.POST['article_pk']
        article = Article.objects.get(pk=article_pk)
        texts = article.text_set.all()
        statuses = [text.status for text in texts]
        data = {'statuses':statuses, 
                'scraper_status':scraper_status, 
                'model_status':model_status}
        return JsonResponse(data, status=201, safe=False)




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
        model_status = ProcessingStatus.objects.get(name='MODEL')
        model_status.status = status
        model_status.save()
        data = {
            'status':model_status.status,
        }
        return JsonResponse(data, status=201, safe=False)
        