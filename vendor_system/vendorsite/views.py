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
        
class HperformanceViewset(viewsets.ViewSet):
    def get(self, request, pk=None):
        try:
            vendor_inst = vendor.objects.get(pk=pk)
            res = self.calculate_performance_metrics(vendor_inst)
            quality_rating_avg = vendor_inst.quality_rating_avg
            average_response_time = vendor_inst.average_response_time
            fulfillment_rate = vendor_inst.fulfillment_rate
            on_time_delivery_rate = vendor_inst.on_time_delivery_rate
        except vendor.DoesNotExist:
            return JsonResponse({"message": "vendor doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
            'on_time_delivery_rate': on_time_delivery_rate,
        })
    
    def calculate_performance_metrics(self,vendor_inst):
        self.calc_onTimedeliveryRate(vendor_inst)
        self.calcQualityRatingAvg(vendor_inst)
        self.calcAvgRespTime(vendor_inst)
        self.calcFulfillmentRate(vendor_inst)

    def calc_onTimedeliveryRate(self,vendor_inst):
        total = purchaseOrder.objects.filter(vendor=vendor_inst, status="completed").count()
        if total == 0:
            vendor.on_time_delivery_rate = 0
        else:
            on_time_count = 0
            orders = purchaseOrder.objects.filter(vendor=vendor_inst, status="completed")
            for order in orders:
                on_time_delivery_orders = order.order_date + timedelta(days=5)
                if order.delivery_date <= on_time_delivery_orders:
                    on_time_count += 1

            on_time_delivery_rate = (on_time_count / total) * 100 
            vendor.on_time_delivery_rate = on_time_delivery_rate

        return vendor.on_time_delivery_rate


    from django.db.models import Avg, F

    def calcQualityRatingAvg(self, vendor_inst):
        # quality ratings= avg of all quality ratings
        quality_rating_avg = purchaseOrder.objects.filter(vendor=vendor_inst, status='completed').aggregate(avg_rating=Avg('quality_rating'))
        vendor_inst.quality_rating_avg = quality_rating_avg['avg_rating'] if quality_rating_avg['avg_rating'] is not None else 0
        return vendor_inst.quality_rating_avg

    def calcAvgRespTime(self, vendor_inst):
        order = purchaseOrder.objects.filter(vendor=vendor_inst, acknowledgment_date__isnull=False)
        inter = order.aggregate(avg_resp=Avg(F('acknowledgment_date') - F('issue_date')))
        average_response_time = inter['avg_resp'].total_seconds() / order.count() if inter['avg_resp'] else 0
        vendor_inst.average_response_time = average_response_time
        return average_response_time

    def calcFulfillmentRate(self, vendor_inst):
        totalOrders = purchaseOrder.objects.filter(vendor=vendor_inst).count()
        if totalOrders == 0:
            vendor_inst.fulfillment_rate = 0
        else:
            fulfilled_orders = purchaseOrder.objects.filter(vendor=vendor_inst, status='completed', issue_date__isnull=True).count()
            vendor_inst.fulfillment_rate = (fulfilled_orders / totalOrders) * 100
        return vendor_inst.fulfillment_rate

            
        
                
    """def getVendor(self,pk=None):
        try:
            vendorInst= vendor.objects.get(pk=pk)
            hpVendor= purchaseOrder.objects.filter(vendor=vendorInst)
            res=hpVendor.calculate_performance_metrics()
            serialized=historicalPerformanceSerializer(res,many=True)
            return JsonResponse(serialized.data,safe=False)
        except vendor.DoesNotExist:
            return JsonResponse({"message":"vendor doesnt exist"},status=status.HTTP_404_NOT_FOUND)"""


        # Calculate performance metrics for the vendor
        #historicalPerformance.calc_onTimedeliveryRate(vendorInst)
        #historicalPerformance.calcQualityRatingAvg(vendorInst)
        #historicalPerformance.calcAvgRespTime(vendorInst)
        #historicalPerformance.calcFulfillmentRate(vendorInst)
    

    


class AckPurchaseOrderViewSet(viewsets.ViewSet):
    def put(self, request, pk=None):
        if purchaseOrder.objects.get(pk=pk).acknowledgment_date:
                    return Response({"error": "this order has already been acknowledged"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            
            order = purchaseOrder.objects.get(pk=pk)
            # Check if the purchase order is associated with a vendor instance
            if not isinstance(order.vendor, vendor):
                return Response({"message": "Invalid vendor associated with the purchase order"}, status=status.HTTP_400_BAD_REQUEST)
            if order.acknowledgment_date:
                    return Response({"error": "this order has already been acknowledged"}, status=status.HTTP_400_BAD_REQUEST)
            # Update acknowledgment_date to today's date
            order.acknowledgment_date = datetime.now()
            order.save()
            
            # Trigger recalculation of average_response_time
            self.calcAvgRespTime(order)
            
            return Response({"message": "Purchase order acknowledged successfully"}, status=status.HTTP_200_OK)
        except purchaseOrder.DoesNotExist:
            return Response({"message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)


    #def calculate_performance_metrics(sender, instance, **kwargs):
        #historicalPerformance.calculate_performance_metrics(instance)



        #calc perf metrics defined two times
        #ack view
        #admin auth in views of vkay