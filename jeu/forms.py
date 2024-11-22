from django import forms
from .models import Personnage, Lieu

class DeplacementForm(forms.ModelForm):
    class Meta:
        model = Personnage
        fields = ['lieu']

class ActionForm(forms.Form):
    cible = forms.ModelChoiceField(queryset=Personnage.objects.all(), required=False)
    action = forms.ChoiceField(choices=[
        ('tuer', 'Tuer'),
        ('proteger', 'Protéger'),
        ('soigner', 'Soigner'),
    ], required=False)
