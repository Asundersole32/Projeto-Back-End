import django_filters
from rest_framework.response import Response
from rest_framework import status

from users.models import CustomUser
from users.serializers.custom_user_serializer import CustomUserDetailsSerializer


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    date_joined_after = django_filters.DateFilter(field_name='date_joined', lookup_expr='gte')
    date_joined_before = django_filters.DateFilter(field_name='date_joined', lookup_expr='lte')
    last_login_before = django_filters.DateFilter(field_name='date_joined', lookup_expr='lte')
    last_login_after = django_filters.DateFilter(field_name='date_joined', lookup_expr='gte')

    class Meta:
        model = CustomUser
        fields = ['is_active', 'email', 'is_admin', 'is_staff', 'is_superuser']


class UserRepository():

    async def create_user(self, user_data):
        try:
            serializer = CustomUserDetailsSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                status_return = {'status': "OK", 'msg': "user successfully created!"}
                return status_return
            error_status = {'status': "ERROR", 'msg': 'serializer not valid!'}
            return error_status
        except Exception as error:
            error_status = {'status': "ERROR", 'msg': 'error on user creation!', 'error_msg': str(error)}
            return error_status
        
    async def update_user(self, data, uid):
        try:
            user = CustomUser.objects.get(uid=uid)
            serializer = CustomUserDetailsSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                status_return = {'status': "OK", 'msg': "user successfully updated!"}
                return status_return
            error_status = {'status': "ERROR", 'msg': 'serializer not valid!'}
            return error_status
        except Exception as error:
            error_status = {'status': "ERROR", 'msg': 'error on user update!', 'error_msg': str(error)}
            return error_status

    async def get_user(self, uid):
        try:
            user = CustomUser.objects.get(uid=uid)
            serializer = CustomUserDetailsSerializer(user)
            status_return = {'status': "OK", 'msg': "successfully get user's data!", "data": serializer}
            return status_return
        except Exception as error:
            error_status = {'status': "ERROR", 'msg': 'error on getting the user!', 'error_msg': str(error)}
            return error_status
        
    async def remove_user(self, uid):
        try:
            user = CustomUser.objects.get(uid=uid)
            user.delete()
            status_return = {'status': "OK", 'msg': "User successfully deleted!", "data": user}
            return status_return
        except Exception as error:
            error_status = {'status': "ERROR", 'msg': 'error on deleting the user!', 'error_msg': str(error)}
            return error_status

