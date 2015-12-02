# -*- coding: utf-8 -*-
from datetimewidget.widgets import DateWidget

from django import forms


from .models import Ttipsup, Tsubtipsup, Tadministrado, SimuesProcesoSegActividadDET, \
Tterminoreferencia, EfaSupervisor, EfaActividadSupervisor, DATE, BOOL, INTEGER, Tunidadoperativa



input_formats_busqueda = ['%d/%m/%Y','%d/%m/%y','%m/%Y','%m/%y','%Y','%y', '%d-%m-%Y','%d-%m-%y','%m-%Y','%m-%y']
input_formats_registro = ['%d/%m/%Y','%d/%m/%y','%d-%m-%Y','%d-%m-%y']

dateOptions = {
'format': 'dd/mm/yyyy',
'autoclose': True,
'showMeridian' : True
}


class BusquedaForm(forms.Form):
    """ Formulario para la Búsqueda de Actividades de Supervisión
    """
    cuc = forms.CharField(label='CUC', max_length=25, required=False)
    fecha_ini = forms.DateField(required=False, input_formats=input_formats_busqueda,
                                widget=DateWidget(attrs={'id':"fecha_ini", 'class':'fecha'},
                                                  bootstrap_version=3, options=dateOptions)
                                )
    fecha_fin = forms.DateField(required=False, input_formats=input_formats_busqueda,
                                widget=DateWidget(attrs={'id':"fecha_fin", 'class':'fecha'},
                                                  bootstrap_version=3, options=dateOptions)
                                )
    administrado = forms.ModelChoiceField(queryset=Tadministrado.objects.all().order_by('razonsocial'),
                                          required=False)
    unidad = forms.ModelChoiceField(
        queryset=Tunidadoperativa.objects.all().only(
            'idunidadoperativa','txnombreunidad').order_by('txnombreunidad'),
        required=False)
        #queryset=Tsubunidadoperativa.objects.select_related(
        #    'idunidadoperativa__txnombreunidad').all().order_by('idunidadoperativa__txnombreunidad'),
        #required=False)

    tdr = forms.ModelChoiceField(queryset=Tterminoreferencia.objects.exclude(txcodigo="").order_by('txcodigo'),
                                 required=False, label="TDR")
    tipo_supervision = forms.ModelChoiceField(queryset=Ttipsup.objects.all().order_by('txtipsup'),
                                              required=False, label="Tipo Supervisión")
    sub_tipo_supervision = forms.ModelChoiceField(queryset=Tsubtipsup.objects.all().order_by('txsubtipsup'),
                                                  required=False, label="Sub Tipo Supervisión")



class RegistroForm(forms.Form):
    """ Formulario dinamico para el registro del Seguimiento de Actividades
    """

    def __init__(self,*args,**kwargs):

        # El parametro extra obtenido en la vista es un queryset con todos los procesos
        procesos = kwargs.pop('extra')
        # Si hemos pasado un Seguimiento de Actividad lo asignamos a una variable
        if 'segact' in kwargs:
            segact = kwargs.pop('segact')
        else:
            segact = None

        super(RegistroForm, self).__init__(*args, **kwargs)

        #Si se abre el formulario para edición de un seguimiento ya existente
        if segact:
            # Creamos y llenamos los campos del formulario en base a los procesos y a su tipo de dato
            for proceso in procesos:
                if proceso.tipo_dato == DATE:
                    # Obtenemos el valor del campo
                    valor = SimuesProcesoSegActividadDET.objects.get(idsegactividad=segact,
                                                                idproceso=proceso).fecha
                    self.fields[str(proceso.id)] = forms.DateField(label=proceso.nombre, required=False,
                                                              input_formats=input_formats_registro,
                                                              initial=valor,
                                                              localize=True,
                                                              widget=DateWidget(attrs={'id':str(proceso.id)},
                                                              bootstrap_version=3, options=dateOptions))
                elif proceso.tipo_dato == INTEGER:
                    valor = SimuesProcesoSegActividadDET.objects.get(idsegactividad=segact,
                                                                idproceso=proceso).num
                    self.fields[str(proceso.id)] = forms.IntegerField(label=proceso.nombre,
                                                                           required=False, min_value=0,
                                                                           initial=valor)
                elif proceso.tipo_dato == BOOL:
                    valor = SimuesProcesoSegActividadDET.objects.get(idsegactividad=segact,
                                                                idproceso=proceso).sino
                    self.fields[str(proceso.id)] = forms.BooleanField(label=proceso.nombre,
                                                                      required=False,
                                                                       initial=valor)
        else:
            # Creamos los campos del formulario en base a los procesos y a su tipo de dato
            for proceso in procesos:
                if proceso.tipo_dato == DATE:
                    self.fields[str(proceso.id)] = forms.DateField(label=proceso.nombre, required=False,
                                                              input_formats=input_formats_registro,
                                                              localize=True,
                                                              widget=DateWidget(attrs={'id':str(proceso.id)},
                                                              bootstrap_version=3, options=dateOptions))
                elif proceso.tipo_dato == INTEGER:
                    self.fields[str(proceso.id)] = forms.IntegerField(label=proceso.nombre,
                                                                           required=False, min_value=0)
                elif proceso.tipo_dato == BOOL:
                    self.fields[ str(proceso.id)] = forms.BooleanField(label=proceso.nombre, required=False)


    def procesos(self):
        """ Se devuelven el nombre y el valor de los campos del formulario """
        for name, value in self.cleaned_data.items():
             yield (name, value)


class ElegirCargoInspectoresForm(forms.Form):


    def __init__(self,*args,**kwargs):

        supervisores = None
        if 'supervisores' in kwargs:
            supervisores = kwargs.pop('supervisores')

        # El parametro extra obtenido en la vista es objeto Actividad
        actividad = kwargs.pop('actividad')

        super(ElegirCargoInspectoresForm, self).__init__(*args, **kwargs)

        # Por defecto los combos solo muestran los supervisores asociados a la actividad
        self.fields['inspector'] = forms.ModelChoiceField(
            queryset=EfaSupervisor.objects.filter(
                id__in=EfaActividadSupervisor.objects.filter(idactividad=actividad).values('idsupervisor')),
            required=False)

        self.fields['inspector_lider'] = forms.ModelChoiceField(
            queryset=EfaSupervisor.objects.filter(
                id__in=EfaActividadSupervisor.objects.filter(idactividad=actividad).values('idsupervisor')),
            required=False)

        if supervisores:
            if 'inspector' in supervisores.keys():
                self.fields['inspector'].initial = supervisores['inspector'].supervisor
            if 'inspector_lider' in supervisores.keys():
                self.fields['inspector_lider'].initial = supervisores['inspector_lider'].supervisor


