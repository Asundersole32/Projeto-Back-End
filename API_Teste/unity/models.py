from django.db import models


class Prefab(models.Model):
    prefab_name = models.CharField(max_length=100)

    def __str__(self):
        return self.prefab_name


class Tag(models.Model):
    tag_name=models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name


class Layer(models.Model):
    layer_name=models.CharField(max_length=100)

    def __str__(self):
        return self.layer_name


class GameObject(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name=models.CharField(max_length=100)
    tag=models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    layer=models.ForeignKey(Layer, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    prefab_name=models.CharField(max_length=100)
    pre_existing_parent = models.CharField(max_length=100, null=True, blank=True, default=None)
    line_position = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', default=None)

    def __str__(self):
        return self.name


class GameObjectTransform(models.Model):
    game_object=models.ForeignKey(GameObject, on_delete=models.CASCADE, null=True, blank=True, default=None)
    prefab = models.ForeignKey(Prefab, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return str(self.game_object)


class GameObjectPosition(models.Model):
    game_object_transform=models.ForeignKey(GameObjectTransform, on_delete=models.CASCADE)
    x=models.FloatField()
    y=models.FloatField()
    z=models.FloatField()

    def __str__(self):
        return str(self.game_object_transform)


class GameObjectRotation(models.Model):
    game_object_transform=models.ForeignKey(GameObjectTransform, on_delete=models.CASCADE)
    x=models.FloatField()
    y=models.FloatField()
    z=models.FloatField()

    def __str__(self):
        return str(self.game_object_transform)

class GameObjectScale(models.Model):
    game_object_transform=models.ForeignKey(GameObjectTransform, on_delete=models.CASCADE)
    x=models.FloatField()
    y=models.FloatField()
    z=models.FloatField()

    def __str__(self):
        return str(self.game_object_transform)
    

class Metadata(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    scene=models.CharField(max_length=100)
    gameobject=models.ForeignKey(GameObject, on_delete=models.CASCADE)

    def __str__(self):
        return self.scene + ' + ' + str(self.gameobject)