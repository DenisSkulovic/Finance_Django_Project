from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from scraper.models import Request, Article, Text
from analysis.forms import RequestCreateForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from finance_proj.settings import TEXT_CLEANER, MODEL
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


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
    }
    return render(request, 'article_detail.html', context=context)




def get_html(data):
    html = '<p>'
    end_p = '</p>'
    try:
        sentences, sequences = TEXT_CLEANER.get_cleaned_element(data)
        outputs = list(map(lambda x: MODEL.predict(x), sequences))
        for sentence, output in zip(sentences, outputs):
            output = output[0][0] - output[0][2]
            print(output)
            if output > 0.85:
                html += f'<span style="background-color:#03DF04">{sentence}</span>'
            elif output > 0.60:
                html += f'<span style="background-color:#2AED2D">{sentence}</span>'
            elif output > 0.45:
                html += f'<span style="background-color:#62F163">{sentence}</span>'
            elif output > 0.30:
                html += f'<span style="background-color:#A0F9A0">{sentence}</span>'
            elif output > 0.15:
                html += f'<span style="background-color:#D8FCD8">{sentence}</span>'
            elif output > 0.00:
                html += f'<span style="background-color:#FFFFFE">{sentence}</span>'
            elif output > -0.15:
                html += f'<span style="background-color:#FFDBDD">{sentence}</span>'
            elif output > -0.30:
                html += f'<span style="background-color:#F6BDC0">{sentence}</span>'
            elif output > -0.45:
                html += f'<span style="background-color:#F1959B">{sentence}</span>'
            elif output > -0.60:
                html += f'<span style="background-color:#F07470">{sentence}</span>'
            elif output > -0.85:
                html += f'<span style="background-color:#EA4C46">{sentence}</span>'
            else:
                html += f'<span style="background-color:#DC1C13">{sentence}</span>'
    except: pass

    html += end_p
    return html



@csrf_exempt
def evaluate(request):
    if request.method == 'POST':
        data = request.POST['text']
        html = get_html(data)
        return JsonResponse({'html':html}, status=201, safe=False)


@csrf_exempt
def refresh_request_status(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        req = Request.objects.get(pk=pk)
        articles = req.article_set.all()
        statuses = [article.status for article in articles]
        return JsonResponse({'statuses':statuses}, status=201, safe=False)


@csrf_exempt
def load_initial_content(request):
    if request.method == 'POST':
        articles_len = len(Request.objects.get(pk=request.POST['pk']).article_set.all())
        return JsonResponse({'articles_len':articles_len}, status=201, safe=False)


@csrf_exempt
def load_article_content(request):
    if request.method == 'POST':
        article_index = int(request.POST['article_index'])
        request_pk = request.POST['request_pk']
        req_articles = Request.objects.get(pk=request_pk).article_set.all()
        article = model_to_dict(req_articles[article_index])
        return JsonResponse({'article':article, 'article_index':article_index}, status=201, safe=False)


