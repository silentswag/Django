from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import vendor, purchaseOrder, historicalPerformance
from .serializers import *

from django.shortcuts import render
from django.http import HttpResponse

def vendor(request):
    return HttpResponse("Hello world!")


class vendorViewset(viewsets.ViewSet):
    def create(self,request):
        serialized=vendorSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = vendor.objects.all()
        serialized = vendorSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = vendor.objects.all()
        vendor = queryset.filter(pk=pk).first()
        if vendor:
            serialized = vendorSerializer(vendor)
            return Response(serialized.data)
        return Response({"message": "vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            vendor = vendor.objects.get(pk=pk)
        except vendor.DoesNotExist:
            return Response({"message": "vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serialized = vendorSerializer(vendor, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            vendor = vendor.objects.get(pk=pk)
        except vendor.DoesNotExist:
            return Response({"message": "vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)