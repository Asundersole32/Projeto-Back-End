from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from machines.models import Machine
from machines.serializers.machine_serializer import MachineSerializer

import django_filters


class MachineFilter(django_filters.FilterSet):
    machine_name = django_filters.CharFilter(lookup_expr='icontains')
    machine_type = django_filters.CharFilter(lookup_expr='icontains')
    company = django_filters.CharFilter(lookup_expr='icontains')
    line = django_filters.NumberFilter(field_name='line__id')
    line_name = django_filters.CharFilter(field_name='line__name', lookup_expr='icontains')
    created_at_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    updated_at_after = django_filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    updated_at_before = django_filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Machine
        fields = ['is_active']


class MachineListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MachineSerializer
    queryset = Machine.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MachineFilter

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as error:
            return Response({'message': str(error)},status=status.HTTP_400_BAD_REQUEST)
