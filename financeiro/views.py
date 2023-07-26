# views.py

from datetime import date

from django.db.models import Sum
from django.shortcuts import render

from .models import Categoria, Subcategoria, Transacao

# views.py


# views.py


def visao_geral(request):
    year = date.today().year
    transacoes = Transacao.objects.filter(data__year=year)
    resumo = {}
    for categoria in Categoria.objects.all():
        subcategorias = Subcategoria.objects.filter(categoria=categoria)
        resumo[categoria.nome] = {'subcategorias': subcategorias, 'meses': {}}
        for mes in range(1, 13):
            resumo[categoria.nome]['meses'][mes] = {
                'total': transacoes.filter(subcategoria__categoria=categoria, data__month=mes).aggregate(Sum('montante'))['montante__sum'] or 0,
                'subcategorias': {},
            }
            for transacao in transacoes.filter(subcategoria__categoria=categoria, data__month=mes):
                if transacao.subcategoria.nome not in resumo[categoria.nome]['meses'][mes]['subcategorias']:
                    resumo[categoria.nome]['meses'][mes]['subcategorias'][transacao.subcategoria.nome] = 0
                resumo[categoria.nome]['meses'][mes]['subcategorias'][transacao.subcategoria.nome] += transacao.montante
    meses = list(range(1, 13))
    return render(request, 'financeiro/visao_geral.html', {'resumo': resumo, 'meses': meses})
