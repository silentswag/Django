from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import vendor, purchaseOrder, historicalPerformance
from .serializers import vendorSerializer, purchaseOrderSerializer,historicalPerformanceSerializer

from django.shortcuts import render
from django.http import HttpResponse

class vendorViewset(viewsets.ViewSet):
    def createVendor(self, request):
        serialized = vendorSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)

    def listVendors(self, request):
        queryset=vendor.objects.all()
        serialized=vendorSerializer(queryset,many=True)
        return Response(serialized.data)
    
    def retrieve(self, request,pk=None):
        try:
            vendorInst=vendor.objects.get(pk=pk)
            serialized=vendorSerializer(vendorInst)
            return Response(serialized.data)
        except vendor.DoesNotExist:
            return Response({"message":"This vendor doesnt exist in the database"},status=status.HTTP_404_NOT_FOUND)
        

    def UpdateVdetails(self,request,pk):
        try:
            vendorUpdates= vendor.objects.get(pk=pk)
            serialized=vendorSerializer(vendorUpdates,data=request.data)
            if serialized.is_valid:
                serialized.save()
                return Response(serialized.data,{"message":"data updated"})
            return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)  
        except vendor.DoesNotExist:
            return Response({"message":"This vendor doesnt exist in the database"},status=status.HTTP_404_NOT_FOUND) 

    def deleteVendor(self,request,pk):
        try:
            delVendor=vendor.objects.get(pk=pk)
            delVendor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except vendor.DoesNotExist:
            return Response({"message":"vendor not available to delete"},status=status.HTTP_404_NOT_FOUND)
       
       

class poViewset(viewsets.ViewSet):
    def createPO(self, request):
        serializer = purchaseOrderSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def listPO(self, request):
        queryset = purchaseOrder.objects.all()
        serializer = purchaseOrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrievePOinstance(self, request, pk=None):
        try:
            purchase_order = purchaseOrder.objects.get(pk=pk)
            serializer = purchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        except purchaseOrder.DoesNotExist:
            return Response({"message": "Purchase order not found in database"}, status=status.HTTP_404_NOT_FOUND)

    def updatePO(self, request, pk=None):
        try:
            purchase_order = purchaseOrder.objects.get(pk=pk)
            serializer = purchaseOrderSerializer(purchase_order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except purchaseOrder.DoesNotExist:
            return Response({"message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

    def delPO(self, request, pk=None):
        try:
            purchase_order = purchaseOrder.objects.get(pk=pk)
            purchase_order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except purchaseOrder.DoesNotExist:
            return Response({"message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
        
#class HperformanceViewset(viewsets.ViewSet):
    