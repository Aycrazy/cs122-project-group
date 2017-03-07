from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

class UserInput(forms.Form):
    start_date = forms.DateField(help_text="Enter a start date after 04/01/2008")
    end_date = forms.DateField(help_text="Enter an end date before 04/01/2013")
    keyword = forms.CharField(help_text="Enter a keyword or phrase in English or Spanish")
    stock_or_currency = forms.ChoiceField(choices=['stocks','currency'])
    home = forms.ChoiceField(choices=['United States','Mexico'])
    other = forms.ChoiceField(choices=['United States','Mexico'])

    def stock_choice(self):
        if self.stock_or_currency == 'stock':
            chosen_stock = forms.ChoiceField(choices=['NASDAQ','Crude Oil Future','Ford','Boeing','Chrysler','West Texas Intermediate'])
            return chosen_stock

    def clean_start_date(self):
        start_data = self.cleaned_data['start_date']
        
        if start_data < datetime.date(2008,4,1):
            raise ValidationError(_('Invalid date - start in past'))
        return start_data

    def clean_end_date(self):
        end_data = self.cleaned_data['end_date']

        if end_data < datetime.date(2013,4,1):
            raise ValidationError(_('Invalid date - beyond current dataset'))
        return end_data