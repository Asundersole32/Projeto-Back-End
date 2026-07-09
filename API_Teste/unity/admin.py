from django.contrib import admin

from unity.models import (Tag, 
                    Layer, 
                    GameObject, 
                    GameObjectTransform, 
                    GameObjectPosition, 
                    GameObjectRotation,
                    GameObjectScale,
                    Metadata,
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
    list_display = ['id', 'name', 'tag', 'prefab_name', 'parent_id']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']


admin.site.register(GameObject, GameObjectAdmin)


class GameObjectTransformAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_object']
    list_display_links = ['id', 'game_object']
    search_fields = ['id', 'game_object']


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
