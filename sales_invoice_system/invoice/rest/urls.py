from django.urls import path
from .invoice import (
    InvoiceCreateApiView,
    InvoiceDetailApiView,
    InvoiceListApiView,
    InvoicePaymentApiView
)

urlpatterns = [
    path("invoices_create/", InvoiceCreateApiView.as_view(), name="invoice-create"),
    path("invoices_list", InvoiceListApiView.as_view(), name="invoice-create"),
    path('invoice/<str:reference>', InvoiceDetailApiView.as_view(), name='invoice-detail'),
    path('pay_invoice/', InvoicePaymentApiView.as_view(), name='invoice-pay'),

]
