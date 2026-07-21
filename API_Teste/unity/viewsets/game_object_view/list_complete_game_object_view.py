from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from unity.models import GameObject, Metadata, GameObjectTransform, GameObjectScale, GameObjectPosition, GameObjectRotation, MachineGameObject

from unity.serializers.game_object_position_serializer import GameObjectPositionSerializer
from unity.serializers.game_object_rotation_serializer import GameObjectRotationSerializer
from unity.serializers.game_object_scale_serializer import GameObjectScaleSerializer
from unity.serializers.game_object_serializer import GameObjectSerializer
from unity.serializers.game_object_transform_serializer import GameObjectTransformSerializer
from unity.serializers.metadata_serializer import MetadataSerializer
from unity.serializers.machine_game_object_serializer import MachineGameObjectSerializer


class ListCompleteGameObjectsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, game_object_id=None):
        try:
            return_list = []
            
            game_objects = GameObject.objects.all()

            for game_object in game_objects:
                return_info = {}
                
                metadata = Metadata.objects.filter(gameobject=game_object).last()
                try:
                    machine_game_object = MachineGameObject.objects.get(game_object=game_object)
                except:
                    machine_game_object = None

                if game_object.prefab != None:
                    if game_object.prefab.prefab_name != "Vazio":
                        game_object_transform = GameObjectTransform.objects.filter(prefab=game_object.prefab).last()
                    else:
                        game_object_transform = GameObjectTransform.objects.filter(game_object=game_object).last()
                else:
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
                return_info['machine'] = machine_game_object.machine.machine_id if machine_game_object != None else None
                return_info['game_object'] = game_object_serializer.data
                return_info['game_object']['transform'] = game_object_transform_serializer.data
                return_info['game_object']['transform']['position'] = game_object_position_serializer.data
                return_info['game_object']['transform']['rotation'] = game_object_rotation_serializer.data
                return_info['game_object']['transform']['scale'] = game_object_scale_serializer.data

                return_list.append(return_info)

            return Response(return_list, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)