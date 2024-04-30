from django.db import models
from datetime import timedelta, datetime
from django.db.models import Avg, Count, F


class vendor(models.Model):
    name=models.CharField(max_length=200)
    contact_details=models.TextField(max_length=50)
    address=models.TextField(max_length=400)
    vendor_code=models.CharField(max_length=200)
    on_time_delivery_rate= models.FloatField(max_length=50)
    quality_rating_avg=models.FloatField(max_length=50)
    average_response_time=models.FloatField(max_length=50)
    fulfillment_rate=models.FloatField(max_length=50)

class purchaseOrder(models.Model):
    po_number=models.CharField(max_length=50)
    vendor=models.ForeignKey(to=vendor, on_delete=models.CASCADE,max_length=100)
    order_date=models.DateTimeField(max_length=10)
    delivery_date=models.DateTimeField(max_length=10)
    items=models.JSONField(max_length=200)
    quantity=models.IntegerField()
    status=models.CharField(max_length=10,choices=[("pending", "pending"), ("completed", "completed"), ("cancelled", "cancelled")], 
        default="pending",)
    quality_rating=models.FloatField(max_length=100)
    issue_date=models.DateTimeField(max_length=10)
    acknowledgment_date=models.DateTimeField(null=True,blank=True)

class historicalPerformance(models.Model):
    vendor=models.ForeignKey(to=vendor, on_delete=models.CASCADE,max_length=200)
    date=models.DateTimeField(max_length=20)
    on_time_delivery_rate=models.FloatField(max_length=50)
    quality_rating_avg=models.FloatField(max_length=50)
    average_response_time=models.FloatField(max_length=50)
    fulfilment_rate=models.FloatField(max_length=10)

     #calcPerformancemetrics
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

    #calls
    def calculate_performance_metrics(vendor):
        historicalPerformance.calc_onTimedeliveryRate(vendor)
        historicalPerformance.calcQualityRatingAvg(vendor)
        historicalPerformance.calcAvgRespTime(vendor)
        historicalPerformance.calcFulfillmentRate(vendor)
        vendor.save()