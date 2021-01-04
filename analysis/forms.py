from django import forms
from scraper.models import Request
from datetime import date, timedelta


class DateInput(forms.DateInput):
    input_type='date'

class RequestCreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['keyword', 'search_start_date', 'periods', 'periodicity', 'google_results_pages']
        today = date.today()
        ten_days_ago = today - timedelta(days=10)
        widgets = {
                'search_start_date': DateInput(attrs={'min': '2010-01-01', 'max': f'{ten_days_ago.strftime("%Y-%m-%d")}'}),
             }