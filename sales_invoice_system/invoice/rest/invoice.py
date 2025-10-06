import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customer.models import Customer
from .serializers import InvoiceSerializer, InvoicePaymentSerializer
from invoice.models import Invoice, InvoiceItem
from rest_framework.permissions import AllowAny
from transaction.models import Transaction
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema





def generate_reference():
        return f"INV-{random.randint(10000, 99999)}"


class InvoiceCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InvoiceSerializer)
    def post(self, request):
        data = request.data
        items_data = data.get("items", [])

        if not items_data:
            return Response({"error": "Invoice must have at least one item."}, status=status.HTTP_400_BAD_REQUEST)

        # 🔹 Fetch customer
        try:
            customer = Customer.objects.get(pk=data.get("customer"))
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        reference = generate_reference()

        # Create invoice
        # Create invoice
        invoice = Invoice.objects.create(
            customer=customer,
            reference=reference,
            status="Pending"
        )

        total = 0
        for item in items_data:
            quantity = int(item.get("quantity", 0))
            unit_price = float(item.get("unit_price", 0))

            if quantity <= 0 or unit_price < 0:
                invoice.delete()
                return Response({"error": "Quantity must be > 0 and unit_price >= 0"}, status=status.HTTP_400_BAD_REQUEST)

            line_total = quantity * unit_price
            total += line_total

            InvoiceItem.objects.create(
                invoice=invoice,
                description=item.get("description"),
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total
            )

        invoice.total_amount = total
        invoice.save()

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class InvoiceListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        invoices = Invoice.objects.all().order_by("-created_at")  # latest first
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class InvoiceDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reference):
        try:
            invoice = Invoice.objects.get(reference=reference)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)



class InvoicePaymentApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InvoicePaymentSerializer)
    def post(self, request):
        serializer = InvoicePaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        reference = serializer.validated_data['reference']
        try:
            invoice = Invoice.objects.get(reference = reference)
        except Invoice.DoesNotExist:
            return Response({"Error":"Invoice are not available"}, status= status.HTTP_400_BAD_REQUEST)
        
        if invoice.status != "Pending":
            return Response({"Error":"Invoice already {invoice.status}"}, status= status.HTTP_400_BAD_REQUEST)
        
        invoice.status = "Paid"
        invoice.save(update_fields=["status"])

        Transaction.objects.create(
             invoice=invoice,
             type="Payment",
             amount=invoice.total_amount
         )
        return Response({"message": f"Invoice {invoice.reference} has been paid successfully"}, status=status.HTTP_200_OK)


