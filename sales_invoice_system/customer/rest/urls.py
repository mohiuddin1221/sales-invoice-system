from django.urls import path
from customer.rest.customer import (
    CustomerCreateView,
    CustomerListView
    )

urlpatterns = [
    path("customers_create/", CustomerCreateView.as_view(), name="customer-create"),
    path("customers_list/", CustomerListView.as_view(), name="customer-create"),
]
