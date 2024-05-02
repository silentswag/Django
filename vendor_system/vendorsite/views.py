from django.shortcuts import render
from rest_framework import viewsets
import datetime
from rest_framework.response import Response
from rest_framework import status
from .models import vendor, purchaseOrder, historicalPerformance
from .serializers import vendorSerializer, purchaseOrderSerializer,historicalPerformanceSerializer
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import render
from datetime import timedelta, datetime
from django.db.models import Avg, Count, F
from django.http import HttpResponse, JsonResponse

def calc_onTimedeliveryRate(vendor):
        # on-time delivery rate=(Number of Deliveries Made on Time / Total Number of Deliveries) * 100
        total=purchaseOrder.objects.filter(vendor=vendor).filter(status="completed").count()
        if total==0:
            vendor.on_time_delivery_rate=0
        else: #check
            on_time_delivery_orders=purchaseOrder.objects.filter(vendor=vendor).filter(status="completed").order_date.date()+ timedelta(days=5)
            if purchaseOrder.objects.filter(vendor=vendor).filter(status="completed").delivery_date.date()<= on_time_delivery_orders:
                on_time_delivery_rate = (on_time_delivery_orders / total) * 100 
            vendor.on_time_delivery_rate = on_time_delivery_rate


def calcQualityRatingAvg(vendor):
# quality ratings= avg of all quality ratings
    quality_rating_avg = purchaseOrder.objects.filter(vendor=vendor, status='completed').aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
    vendor.quality_rating_avg = quality_rating_avg

def calcAvgRespTime(vendor):
    order=purchaseOrder.objects.filter(vendor=vendor).filter(acknowledgement_date__isnull=False)
    inter=order.aggregate(avg_resp=Avg(F('acknowledgment_date') - F('issue_date'))['avg_response'])
    vendor.average_response_time=inter.total_seconds() / purchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).count() if inter else 0

def calcFulfillmentRate(vendor):
    totalOrders = purchaseOrder.objects.filter(vendor=vendor).count()
    if totalOrders == 0:
        vendor.fulfillment_rate = 0
    else:
        fulfilled_orders = purchaseOrder.objects.filter(vendor=vendor, status='completed', issues__isnull=True).count()
        vendor.fulfillment_rate = (fulfilled_orders / totalOrders) * 100

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
            if serialized.is_valid():
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
    def createPO(self, request,pk=None):
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
            purchase_order = purchaseOrder.objects.get(id=pk)
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
        
class HperformanceViewset(viewsets.ViewSet):
    def getVendor(self,request,pid):
        try:
            vendorInst= vendor.objects.get(pid)
            hpVendor= historicalPerformance.objects.filter(vendor=vendorInst)
            serialized=historicalPerformanceSerializer(hpVendor,many=True)
            return JsonResponse(serialized.data)
        except vendor.DoesNotExist:
            return JsonResponse({"message":"vendor doesnt exist"},status=status.HTTP_404_NOT_FOUND)


    def calculate_performance_metrics(self, request, id=None):
        try:
            vendorInst = vendor.objects.get(pk=id)
            calc_onTimedeliveryRate(vendorInst)
            calcAvgRespTime(vendorInst)
            calcFulfillmentRate(vendorInst)
            calcQualityRatingAvg(vendorInst)
        except vendor.DoesNotExist:
            return JsonResponse({"message": "vendor doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        # Calculate performance metrics for the vendor
        #historicalPerformance.calc_onTimedeliveryRate(vendorInst)
        #historicalPerformance.calcQualityRatingAvg(vendorInst)
        #historicalPerformance.calcAvgRespTime(vendorInst)
        #historicalPerformance.calcFulfillmentRate(vendorInst)
    
        return JsonResponse({"message": "Performance metrics calculated and updated for vendor {}".format(id)})
    


class AckPurchaseOrderViewSet(viewsets.ViewSet):
    def put(self, request, pk=None):
        try:
            order = purchaseOrder.objects.get(pk=pk)
            if order.acknowledgment_date:
                    return Response({"error": "this order has already been acknowledged"}, status=status.HTTP_400_BAD_REQUEST)
            serialized = historicalPerformanceSerializer(order, data={"acknowledgment_date": datetime.now()}, partial=True)
            if serialized.is_valid():
                order.save()
                calcAvgRespTime(order)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
        except purchaseOrder.DoesNotExist:
            return Response({"message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        """if order.acknowledgment_date is None:
            order.acknowledgment_date = datetime().now()

        serialized = historicalPerformanceSerializer(order, data={"acknowledgment_date": order.acknowledgment_date}, partial=True)
        if serialized.is_valid():
            order.save()
            historicalPerformance.calculate_performance_metrics(order)
            return Response({"message": "Purchase order acknowledged successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)"""


    #def calculate_performance_metrics(sender, instance, **kwargs):
        #historicalPerformance.calculate_performance_metrics(instance)



        #calc perf metrics defined two times
        #ack view
        #admin auth in views of vkay