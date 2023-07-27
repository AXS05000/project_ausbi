# urls.py
from django.urls import path

from .views import (TransacaoCreate, TransacaoDelete, TransacaoUpdate,
                    TransacoesMes, VisaoGeral)

# urls.py

urlpatterns = [
    path('visao/', VisaoGeral.as_view(), name='visao-geral'),
    path('transacao/nova/', TransacaoCreate.as_view(), name='transacao-nova'),
    path('transacao/<int:pk>/editar/', TransacaoUpdate.as_view(), name='transacao-editar'),
    path('transacao/<int:pk>/deletar/', TransacaoDelete.as_view(), name='transacao-deletar'),
    path('transacao/mes/<int:mes>/', TransacoesMes.as_view(), name='transacoes-mes'),  # nova linha
]

