from rest_framework import serializers
from models import vendor, purchaseOrder,historicalPerformance

class vendorSerializer(serializers.ModelSerializer):
    class Meta:
        model= vendor
        fields= '__all__'

class purchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= purchaseOrder
        fields= '__all__'

class historicalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model= historicalPerformance
        fields='__all__'

