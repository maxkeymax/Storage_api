from django.urls import path
from .views import WasteDistributionView, StorageAPIView

urlpatterns = [
    path('factory/<int:factory_id>/distribute/', WasteDistributionView.as_view(), name='waste-distribution'),
    path('storages/', StorageAPIView.as_view(), name='storages_observation'),
]