from rest_framework import serializers
from invoice.models import Invoice, InvoiceItem
from customer.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone", "address"]


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ["id", "description", "quantity", "unit_price", "line_total"]
        read_only_fields = ["line_total"]


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    customer = CustomerSerializer(read_only=True)  # nested customer

    class Meta:
        model = Invoice
        fields = ["id", "reference", "customer", "status", "total_amount", "items", "created_at"]
        read_only_fields = ["total_amount", "status", "created_at"]
