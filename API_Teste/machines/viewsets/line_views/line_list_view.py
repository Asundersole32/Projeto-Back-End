import django_filters

from machines.models import Line
from machines.serializers.line_serializer import LineSerializer

from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class LineFilter(django_filters.FilterSet):
    line_name = django_filters.CharFilter(lookup_expr='icontains')
    machine_qtd = django_filters.NumberFilter()  # filtro exato
    machine_qtd_min = django_filters.NumberFilter(field_name='machine_qtd', lookup_expr='gte')
    machine_qtd_max = django_filters.NumberFilter(field_name='machine_qtd', lookup_expr='lte')
    created_at_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    updated_at_after = django_filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    updated_at_before = django_filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Line
        fields = []


class ListLineView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LineSerializer
    queryset = Line.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = LineFilter

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as error:
            return Response({'message': str(error)},status=status.HTTP_400_BAD_REQUEST)