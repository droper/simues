from django.contrib import admin

from .models import SimuesTipoMuestra, SimuesTipoEnvase, SimuesUnidadMedida, SimuesGPS, SimuesDatum, SimuesZona, \
    SimuesTipoPunto

admin.site.register(SimuesTipoMuestra)
admin.site.register(SimuesTipoEnvase)
admin.site.register(SimuesUnidadMedida)
admin.site.register(SimuesDatum)
admin.site.register(SimuesZona)
admin.site.register(SimuesGPS)
admin.site.register(SimuesTipoPunto)



