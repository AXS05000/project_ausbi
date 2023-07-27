from datetime import date

from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from .forms import TransacaoForm
from .models import Categoria, Subcategoria, Transacao


class VisaoGeral(TemplateView):
    template_name = 'financeiro/visao_geral.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        year, current_month = today.year, today.month
        meses = list(range(current_month, current_month + 6))
        ordem_categorias = {'Receitas': 1, 'Investimentos': 2, 'Gastos Fixos': 3, 'Gastos Variáveis': 4}  # ordem das categorias
        categorias = sorted(Categoria.objects.all(), key=lambda x: ordem_categorias[x.nome])
        resumo = {}
        for categoria in categorias:
            resumo[categoria.nome] = {'subcategorias': {}, 'total': [0]*6}
            for subcategoria in Subcategoria.objects.filter(categoria=categoria):
                transacoes = Transacao.objects.filter(subcategoria=subcategoria, data__year=year, data__month__in=meses)
                resumo[categoria.nome]['subcategorias'][subcategoria.nome] = {
                    'valores': [0]*6,
                    'ids': [None]*6,
                }
                for transacao in transacoes:
                    mes = transacao.data.month - current_month
                    resumo[categoria.nome]['subcategorias'][subcategoria.nome]['valores'][mes] += transacao.montante
                    resumo[categoria.nome]['subcategorias'][subcategoria.nome]['ids'][mes] = transacao.id
                    resumo[categoria.nome]['total'][mes] += transacao.montante

        # Cálculo do líquido movido para fora do loop
        resumo['Liquido'] = {'total': [0]*6}
        for mes in range(6):  # Calcula o líquido para cada mês
            receita = resumo.get('Receitas', {'total': [0]*6})['total'][mes] or 0
            gastos_fixos = resumo.get('Gastos Fixos', {'total': [0]*6})['total'][mes] or 0
            gastos_variaveis = resumo.get('Gastos Variáveis', {'total': [0]*6})['total'][mes] or 0
            investimentos = resumo.get('Investimentos', {'total': [0]*6})['total'][mes] or 0
            resumo['Liquido']['total'][mes] = receita - (gastos_fixos + gastos_variaveis + investimentos)

        nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        nomes_meses = nomes_meses[current_month-1:current_month+5]
        context['resumo'] = resumo
        context['meses'] = nomes_meses
        return context


class TransacoesMes(ListView):
    model = Transacao
    template_name = 'financeiro/transacoes_mes.html'

    def get_queryset(self):
        year = date.today().year
        mes = self.kwargs['mes']
        return Transacao.objects.filter(data__year=year, data__month=mes)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        context['month'] = nomes_meses[self.kwargs['mes'] - 1]
        return context



class TransacaoCreate(CreateView):
    model = Transacao
    form_class = TransacaoForm
    template_name = 'financeiro/transacao_form.html'

class TransacaoUpdate(UpdateView):
    model = Transacao
    form_class = TransacaoForm
    template_name = 'financeiro/transacao_form.html'

class TransacaoDelete(DeleteView):
    model = Transacao
    template_name = 'financeiro/transacao_confirm_delete.html'
    success_url = reverse_lazy('visao-geral')  # redireciona para a visão geral após a exclusão









