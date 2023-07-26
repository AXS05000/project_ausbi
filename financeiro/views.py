# views.py

from datetime import date

from django.db.models import Sum
from django.shortcuts import render

from .models import Categoria, Subcategoria, Transacao

# views.py

def visao_geral(request):
    year = date.today().year
    meses = list(range(1, 13))
    ordem_categorias = {'RC': 1, 'I': 2, 'GF': 3, 'GV': 4}  # ordem das categorias
    categorias = sorted(Categoria.objects.all(), key=lambda x: ordem_categorias[x.nome])
    resumo = {}
    for categoria in categorias:
        resumo[categoria.nome] = {'subcategorias': {}, 'total': [None]*12}
        for subcategoria in Subcategoria.objects.filter(categoria=categoria):
            transacoes = Transacao.objects.filter(subcategoria=subcategoria, data__year=year)
            resumo[categoria.nome]['subcategorias'][subcategoria.nome] = [None]*12
            for transacao in transacoes:
                mes = transacao.data.month - 1 # os índices em Python começam em 0
                if resumo[categoria.nome]['subcategorias'][subcategoria.nome][mes] is None:
                    resumo[categoria.nome]['subcategorias'][subcategoria.nome][mes] = 0
                resumo[categoria.nome]['subcategorias'][subcategoria.nome][mes] += transacao.montante
                if resumo[categoria.nome]['total'][mes] is None:
                    resumo[categoria.nome]['total'][mes] = 0
                resumo[categoria.nome]['total'][mes] += transacao.montante
    nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    return render(request, 'financeiro/visao_geral.html', {'resumo': resumo, 'meses': nomes_meses})


