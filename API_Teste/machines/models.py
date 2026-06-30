from django.db import models


class Line(models.Model):
    machine_qtd=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Machine(models.Model):
    machineName=models.CharField(max_length=100)
    machineType=models.CharField(max_length=100)
    company=models.CharField(max_length=100)
    line=models.ForeignKey(Line, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



