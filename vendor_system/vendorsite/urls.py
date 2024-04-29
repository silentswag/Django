from django.urls import path
from . import views

urlpatterns = [
    path('/api/vendors/', views.vendorViewset.as_view({'post':'createVendor','get':'listVendors'}), name='vendor-create-list'),
    path('api/vendors/<int:pk>/',views.vendorViewset.as_view({'get':'retrieve','put':'updateVdetails','delete':'deleteVendor'}),name='vendor-get-update-delete'),
    path('api/purchase_orders/', views.poViewset.as_view({'post':'createPO','get':'listPO'}),name='PO-create-list'),
    path('api/purchase_orders/<int:pk>/',views.poViewset.as_view({'get':'retrievePOinstance','put':'updatePO','delete':'delPO'}),name='po-ret-update-del'),
    path('api/vendors/<int:id>/performance/', views.HperformanceViewset.as_view({'get': 'getVendor', 'post': 'calculate_performance_metrics'}), name='vendor-performance'),
    #path('api/purchase_orders/<int:pk>/acknowledge/', views.AcknowledgePurchaseOrder.as_view(), name='acknowledge-purchase-order'),
]