from rest_framework import serializers
from transaction.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    invoice_reference = serializers.CharField(source="invoice.reference", read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "invoice_reference", "type", "amount", "created_at"]
