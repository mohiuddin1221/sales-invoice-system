from django.urls import path
from .transaction import TransactionListApiView, TransactionByInvoiceApiView

urlpatterns = [
    path('transactions_list', TransactionListApiView.as_view(), name='transaction-list'),
    path('transactions/<str:reference>', TransactionByInvoiceApiView.as_view(), name='transaction-by-invoice'),
]
