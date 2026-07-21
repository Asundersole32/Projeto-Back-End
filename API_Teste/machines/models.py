from django.db import models


class Line(models.Model):
    line_name=models.CharField(max_length=100)
    machine_qtd=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.line_name


class Machine(models.Model):
    machine_id = models.CharField(max_length=100, null=True, blank=True, default=None)
    machine_name=models.CharField(max_length=100)
    machine_type=models.CharField(max_length=100)
    company=models.CharField(max_length=100)
    line=models.ForeignKey(Line, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.machine_name


class MachineData(models.Model):
    machine=models.ForeignKey(Machine, on_delete=models.CASCADE)
    data=models.JSONField(default=dict, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.machine) + ' - ' + str(self.created_at)

