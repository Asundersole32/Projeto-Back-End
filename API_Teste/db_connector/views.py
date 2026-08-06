from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.db_connector import DatabaseConnector
from .serializers import ConnectionSerializer


class ConnectView(APIView):
    def post(self, request):
        serializer = ConnectionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                conn_id = DatabaseConnector.connect(serializer.validated_data)
                return Response({'connection_id': conn_id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TablesListView(APIView):
    def get(self, request):
        conn_id = request.headers.get('X-Connection-Id')
        if not conn_id:
            return Response({'error': 'Missing X-Connection-Id header'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tables = DatabaseConnector.get_tables(conn_id)
            return Response({'tables': tables})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TableInfoView(APIView):
    def get(self, request, table_name):
        conn_id = request.headers.get('X-Connection-Id')
        if not conn_id:
            return Response({'error': 'Missing X-Connection-Id header'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            info = DatabaseConnector.get_table_info(conn_id, table_name)
            return Response(info)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TableDataView(APIView):
    def get(self, request, table_name):
        conn_id = request.headers.get('X-Connection-Id')
        if not conn_id:
            return Response({'error': 'Missing X-Connection-Id header'}, status=status.HTTP_400_BAD_REQUEST)

        # Parâmetros de paginação e ordenação
        limit = request.query_params.get('limit', 100)
        offset = request.query_params.get('offset', 0)
        order_by = request.query_params.getlist('order_by')

        # Filtros: todos os outros parâmetros são considerados filtros
        filters = {}
        for key, value in request.query_params.items():
            if key not in ['limit', 'offset', 'order_by']:
                filters[key] = value

        try:
            data = DatabaseConnector.get_table_data(
                conn_id, table_name,
                filters=filters,
                order_by=order_by,
                limit=int(limit),
                offset=int(offset)
            )
            return Response({
                'data': data,
                'count': len(data),
                'limit': limit,
                'offset': offset
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, table_name):
        conn_id = request.headers.get('X-Connection-Id')
        if not conn_id:
            return Response({'error': 'Missing X-Connection-Id header'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        if not isinstance(data, dict):
            return Response({'error': 'Data must be a JSON object'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = DatabaseConnector.insert_row(conn_id, table_name, data)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TableRowDetailView(APIView):
    def put(self, request, table_name, pk):
        conn_id = request.headers.get('X-Connection-Id')
        if not conn_id:
            return Response({'error': 'Missing X-Connection-Id header'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        if not isinstance(data, dict):
            return Response({'error': 'Data must be a JSON object'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = DatabaseConnector.update_row(conn_id, table_name, pk, data)
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, table_name, pk):
        conn_id = request.headers.get('X-Connection-Id')
        if not conn_id:
            return Response({'error': 'Missing X-Connection-Id header'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = DatabaseConnector.delete_row(conn_id, table_name, pk)
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)