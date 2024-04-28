from django.db import models
class vendor(models.Model):
    name=models.CharField(max_length=200)
    contact_details=models.TextField(max_length=10)
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
    status=models.CharField(max_length=100)
    quality_rating=models.FloatField(max_length=100)
    issue_date=models.DateTimeField(max_length=10)
    acknowledgment_date=models.DateTimeField(max_length=10)

class historicalPerformance(models.Model):
    vendor=models.ForeignKey(to=vendor, on_delete=models.CASCADE,max_length=200)
    date=models.DateTimeField(max_length=20)
    on_time_delivery_rate=models.FloatField(max_length=50)
    quality_rating_avg=models.FloatField(max_length=50)
    average_response_time=models.FloatField(max_length=50)
    fulfilment_rate=models.FloatField(max_length=10)