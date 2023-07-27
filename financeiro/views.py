# views.py

from datetime import date

from django.db.models import Sum
from django.shortcuts import render

from .models import Categoria, Subcategoria, Transacao


# views.py
def visao_geral(request):
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
            resumo[categoria.nome]['subcategorias'][subcategoria.nome] = [0]*6
            for transacao in transacoes:
                mes = transacao.data.month - current_month  # os índices em Python começam em 0
                resumo[categoria.nome]['subcategorias'][subcategoria.nome][mes] += transacao.montante
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
    return render(request, 'financeiro/visao_geral.html', {'resumo': resumo, 'meses': nomes_meses})







