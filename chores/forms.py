from django import forms

from .models import Chore


class HouseholdForm(forms.Form):
    code = forms.CharField(max_length=8, label='Household code')
    name = forms.CharField(max_length=120, required=False, initial='Our home')


class PartnerForm(forms.Form):
    display_name = forms.CharField(max_length=80, label='Your name')
    avatar_color = forms.CharField(max_length=7, initial='#245c52', widget=forms.TextInput(attrs={'type': 'color'}))


class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['title', 'description', 'frequency', 'due_date', 'effort', 'is_shared', 'assigned_to']
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, household=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = household.partners.all() if household else self.fields['assigned_to'].queryset.none()