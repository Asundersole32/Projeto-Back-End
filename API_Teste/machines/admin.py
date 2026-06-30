from django.contrib import admin

from machines.models import Line, Machine, MachineData


class LineAdmin(admin.ModelAdmin):
    list_display = ['id', 'line_name', 'machine_qtd', 'created_at', 'updated_at']
    list_display_links = ['id', 'line_name']
    search_fields = ['id', 'line_name']


admin.site.register(Line, LineAdmin)

class MachineAdmin(admin.ModelAdmin):
    list_display = ['id', 'machine_name', 'machine_type', 'company', 'line', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'machine_name', 'machine_type']
    search_fields = ['id', 'machine_name', 'machine_type']

admin.site.register(Machine, MachineAdmin)


class MachineDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'machine', 'data', 'created_at']
    list_display_links = ['id', 'machine']
    search_fields = ['id', 'machine']

admin.site.register(MachineData, MachineDataAdmin)