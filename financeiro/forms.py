# forms.py

from django import forms

from .models import Transacao


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['subcategoria', 'data', 'montante', 'descricao']
