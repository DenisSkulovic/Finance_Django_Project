from finance_proj.settings import TEXT_CLEANER, MODEL
from scraper.models import Request, Article, Text
import time

def process_text(work_time_sec=120):
    start = time.time()
    try:
        while True:
            print('started')
            text = Text.objects.filter(status='Unprocessed').first()
            sentences, sequences = TEXT_CLEANER.get_cleaned_element(text.text)
            print('cleaned')
            sentiments = list(map(lambda x: MODEL.predict(x), sequences))
            print('predicted')
            sentiment_scores = [str(sent[0][0]-sent[0][2]) for sent in sentiments]
            sentiment_string = ','.join(sentiment_scores)
            text.text = ' '.join(sentences) # replacing text with processed version to avoid text & sentiment length mismatch
            text.sentiment = sentiment_string
            text.status='Processed'
            text.save()
            print('saved')
            if time.time() - start > work_time_sec:
                break
    except: print('text_processor exited')



if __name__ == "__main__":
    process_text()
