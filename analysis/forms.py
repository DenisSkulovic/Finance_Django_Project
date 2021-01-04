from django import forms
from scraper.models import Request
from datetime import date, timedelta


class DateInput(forms.DateInput):
    input_type='date'

class RequestCreateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['keyword', 'search_start_date', 'periods', 'periodicity', 'google_results_pages', 'accessibility']
        today = date.today()
        ten_days_ago = today - timedelta(days=10)
        widgets = {
                'search_start_date': DateInput(attrs={'min': '2010-01-01', 'max': f'{ten_days_ago.strftime("%Y-%m-%d")}'}), # google results sometimes show dates as '3 Days Ago', which breaks the date-link collection (not necessarily breaks but simply collects nothing for such an article), so I pushed back the last available date a little. Probably easily fixable with some extra care for entries like '6 Days Ago'
             }