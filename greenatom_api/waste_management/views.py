from django.template.context_processors import request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Factory, Storage
from .serializers import WasteDistributionSerializer, StorageSerializer


class StorageAPIView(APIView):
    def get(self, request):
        storages = Storage.objects.all()
        serializer = StorageSerializer(storages, many=True)
        return Response(serializer.data)



class WasteDistributionView(APIView):

    def patch(self, request, factory_id):
        try:
            factory = Factory.objects.get(id=factory_id)
        except Factory.DoesNotExist:
            return Response({"error": "Завод не найден."}, status=status.HTTP_404_NOT_FOUND)

        serializer = WasteDistributionSerializer(data=request.data, context={'factory': factory})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)