from django.db import models
from django.utils import timezone
from invoice.models import Invoice  

class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ("Sale", "Sale"),
        ("Payment", "Payment"),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.type} - {self.invoice.reference} - {self.amount}"
