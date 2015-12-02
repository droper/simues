from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import SimuesProceso, Ttipsup, Tsubtipsup, SimuesSegActividad, Tterminoreferencia,Tterminoreferenciadet, \
    UsuarioExtendido


class SimuesProcesoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

admin.site.register(SimuesProceso, SimuesProcesoAdmin)


# Define un modelo Inline para el modelo
class UsuarioExtendidoInline(admin.StackedInline):
    model = UsuarioExtendido
    can_delete = False
    verbose_name_plural = 'Datos Adicionales del Usuario'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UsuarioExtendidoInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



