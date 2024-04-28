from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, purchaseOrder, historicalPerformance
from .serializers import *

class vendorViewset(viewsets.ViewSet):
    def create(self,request):
        serialized=vendorSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)