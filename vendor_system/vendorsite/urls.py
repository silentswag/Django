from django.urls import path
from . import views

urlpatterns = [
    path('vendors/', views.vendorViewset.as_view({'post':'createVendor','get':'listVendors'}), name='create-Vendor'),
    path('vendors/<int:pk>',views.vendorViewset.as_view({'get':'retrieve','put':'UpdateVdetails','delete':'deleteVendor'}),name='vendor-get-update-delete'),
    path('purchase_orders/', views.poViewset.as_view({'post':'createPO','get':'listPO'}),name='PO-create-list'),
    path('purchase_orders/<int:pk>',views.poViewset.as_view({'get':'retrievePOinstance','put':'updatePO','delete':'delPO'}),name='po-ret-update-del'),
    path('vendors/<int:pk>/performance', views.HperformanceViewset.as_view({'get': 'get'}), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', views.AckPurchaseOrderViewSet.as_view({'put':'put'}), name='acknowledge-purchase-order'),
]