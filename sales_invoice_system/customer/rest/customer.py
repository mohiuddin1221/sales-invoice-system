from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customer.models import Customer
from .serializers import CustomerSerializer
from rest_framework.permissions import AllowAny

class CustomerCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Customer created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomerListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
