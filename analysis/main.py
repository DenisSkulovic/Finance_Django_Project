from finance_proj.settings import TEXT_CLEANER, MODEL
from scraper.models import Request, Article, Text, ProcessingStatus
import time

def process_text(work_time_sec=120):
    if Text.objects.filter(status='Unprocessed').first() == None:
        print('text_processor exited')
        return

    start = time.time()
    try:
        while True:
            text = Text.objects.filter(status='Unprocessed').first()
            sentences, sequences = TEXT_CLEANER.get_cleaned_element(text.text)
            model_status = ProcessingStatus.objects.get_or_create(name='MODEL')[0]
            if model_status.status == 'FREE':
                model_status.status='BUSY'
                model_status.save()
                try:
                    sentiments = list(map(lambda x: MODEL.predict(x), sequences))
                except: pass
                finally: 
                    model_status.status='FREE'
                    model_status.save()
                model_status.status='FREE'
                model_status.save()
            sentiment_scores = [str(sent[0][0]-sent[0][2]) for sent in sentiments]
            sentiment_string = ','.join(sentiment_scores)
            text.text = ' '.join(sentences) # replacing text with processed version to avoid text & sentiment length mismatch
            text.sentiment = sentiment_string
            text.status='Processed'
            text.save()

            update_db_status()

            if time.time() - start > work_time_sec:
                break

    except: print('text_processor exited')




def update_db_status():
    processing_status_articles = Article.objects.exclude(status='Processed').exclude(status='Unprocessed')
    for article in processing_status_articles:
        text_set = article.text_set.filter(status='Unprocessed')
        if len(text_set) == 0:
            article.status = 'Processed'
            article.save()
    processing_status_requests = Request.objects.exclude(status='Processed').exclude(status='Unprocessed')
    for request in processing_status_requests:
        article_set = request.article_set.filter(status='Unprocessed')
        if len(article_set) == 0:
            request.status = 'Processed'
            request.save()   



if __name__ == "__main__":
    process_text()
