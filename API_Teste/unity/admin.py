from django.contrib import admin

from unity.models import (Tag, 
                    Prefab,
                    Layer, 
                    GameObject, 
                    GameObjectTransform, 
                    GameObjectPosition, 
                    GameObjectRotation,
                    GameObjectScale,
                    Metadata,
                    MachineGameObject
                    )


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag_name']
    list_display_links = ['id', 'tag_name']
    search_fields = ['id', 'tag_name']


admin.site.register(Tag, TagAdmin)


class LayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'layer_name']
    list_display_links = ['id', 'layer_name']
    search_fields = ['id', 'layer_name']


admin.site.register(Layer, LayerAdmin)


class GameObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'tag', 'prefab', 'pre_existing_parent', 'line_position', 'parent']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']


admin.site.register(GameObject, GameObjectAdmin)


class GameObjectTransformAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_object', 'prefab']
    list_display_links = ['id', 'game_object', 'prefab']
    search_fields = ['id', 'game_object', 'prefab']


admin.site.register(GameObjectTransform, GameObjectTransformAdmin)


class GameObjectPositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_object_transform', 'x', 'y', 'z']
    list_display_links = ['id', 'game_object_transform']
    search_fields = ['id', 'game_object_transform']


admin.site.register(GameObjectPosition, GameObjectPositionAdmin)


class GameObjectRotationAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_object_transform', 'x', 'y', 'z']
    list_display_links = ['id', 'game_object_transform']
    search_fields = ['id', 'game_object_transform']


admin.site.register(GameObjectRotation, GameObjectRotationAdmin)


class GameObjectScaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_object_transform', 'x', 'y', 'z']
    list_display_links = ['id', 'game_object_transform']
    search_fields = ['id', 'game_object_transform']


admin.site.register(GameObjectScale, GameObjectScaleAdmin)


class MetadataAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'scene', 'gameobject']
    list_display_links = ['id', 'gameobject']
    search_fields = ['id', 'gameobject']


admin.site.register(Metadata, MetadataAdmin)


class PrefabAdmin(admin.ModelAdmin):
    list_display = ['id', 'prefab_name']
    list_display_links = ['id', 'prefab_name']
    search_fields = ['id', 'prefab_name']


admin.site.register(Prefab, PrefabAdmin)


class MachineGameObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_object', 'machine']
    list_display_links = ['id', 'game_object', 'machine']
    search_fields = ['id', 'game_object', 'machine']


admin.site.register(MachineGameObject, MachineGameObjectAdmin)