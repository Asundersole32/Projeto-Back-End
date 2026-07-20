from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from unity.models import GameObject, Metadata, GameObjectTransform, GameObjectScale, GameObjectPosition, GameObjectRotation

from unity.serializers.game_object_position_serializer import GameObjectPositionSerializer
from unity.serializers.game_object_rotation_serializer import GameObjectRotationSerializer
from unity.serializers.game_object_scale_serializer import GameObjectScaleSerializer
from unity.serializers.game_object_serializer import GameObjectSerializer
from unity.serializers.game_object_transform_serializer import GameObjectTransformSerializer
from unity.serializers.metadata_serializer import MetadataSerializer


class GetCompleteGameObjectView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, game_object_id=None):
        try:
            return_info = {}
            
            game_object = GameObject.objects.get(pk=game_object_id)
            metadata = Metadata.objects.filter(gameobject=game_object).last()
            game_object_transform = GameObjectTransform.objects.filter(game_object=game_object).last()
            game_object_position = GameObjectPosition.objects.filter(game_object_transform=game_object_transform).last()
            game_object_rotation = GameObjectRotation.objects.filter(game_object_transform=game_object_transform).last()
            game_object_scale = GameObjectScale.objects.filter(game_object_transform=game_object_transform).last()

            game_object_serializer = GameObjectSerializer(game_object)
            metadata_serializer = MetadataSerializer(metadata)
            game_object_transform_serializer = GameObjectTransformSerializer(game_object_transform)
            game_object_position_serializer = GameObjectPositionSerializer(game_object_position)
            game_object_scale_serializer = GameObjectScaleSerializer(game_object_scale)
            game_object_rotation_serializer = GameObjectRotationSerializer(game_object_rotation)

            return_info['metadata'] = metadata_serializer.data
            return_info['game_object'] = game_object_serializer.data
            return_info['game_object']['transform'] = game_object_transform_serializer.data
            return_info['game_object']['transform']['position'] = game_object_position_serializer.data
            return_info['game_object']['transform']['rotation'] = game_object_rotation_serializer.data
            return_info['game_object']['transform']['scale'] = game_object_scale_serializer.data

            return Response(return_info, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)