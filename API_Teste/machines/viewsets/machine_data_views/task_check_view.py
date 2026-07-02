from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from machines.tasks import check_task_status


class TaskStatusView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        task_id = request.query_params.get('task_id')
        status = check_task_status(task_id)
        return Response(status)