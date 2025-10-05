from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from transaction.models import Transaction
from invoice.models import Invoice
from .serializers import TransactionSerializer

class TransactionListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        transactions = Transaction.objects.all().order_by("-created_at")
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionByInvoiceApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, reference):
        try:
            invoice = Invoice.objects.get(reference=reference)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

        transactions = invoice.transactions.all().order_by("-created_at")
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
