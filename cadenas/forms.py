# -*- coding: utf-8 -*-
from datetimewidget.widgets import DateTimeWidget

from django import forms
from django.forms.widgets import NumberInput

from resumenact.models import Tterminoreferencia, EfaActividad, Tsubmatriz
from .models import SimuesTipoMuestra, SimuesGPS, SimuesDatum, SimuesTipoPunto, SimuesZona, SimuesUnidadMedida, \
    Tlaboratorio

# Formatos posibles para introducir fechas y horas
input_formats = ['%d/%m/%Y %H:%M:%S','%d/%m/%y %H:%M:%S', '%d-%m-%Y %H:%M:%S','%d-%m-%y %H:%M:%S',
                 '%d/%m/%Y %H:%M','%d/%m/%y %H:%M', '%d-%m-%Y %H:%M:%S','%d-%m-%y %H:%M',
                 '%d/%m/%Y %H','%d/%m/%y %H', '%d-%m-%Y %H','%d-%m-%y %H',
                 '%d/%m/%Y','%d/%m/%y', '%d-%m-%Y','%d-%m-%y']

datetimeOptions = {
'format': 'dd/mm/yyyy hh:ii',
'autoclose': True,
'showMeridian' : True
}

dateOptions = {
'format': 'dd/mm/yyyy',
'autoclose': True,
'showMeridian' : True
}

RANGO_COORDENADAS_NORTE = [7969000, 9997000]
RANGO_COORDENADAS_ESTE = [100000, 900000]



class RegistroCadenasForm(forms.Form):
    """ Formulario para el registro y edición de cadenas de custodia
    """
    tipo_matriz = forms.ModelChoiceField(queryset=Tsubmatriz.objects.all().order_by('txsubmatriz'))
    referencia= forms.CharField(required=False, widget=forms.Textarea)
    fecha_resultados_lab =forms.DateTimeField(input_formats=input_formats, required=False,
                                              label = "Fecha resultados recibidos del laboratorio",
                                     widget=DateTimeWidget(attrs={'id':"fechahora"},
                                     bootstrap_version=3, options=datetimeOptions)
                                     )
    laboratorio = forms.ModelChoiceField(queryset=Tlaboratorio.objects.all().order_by('txlaboratorio'),
                                         required=False)


    def __init__(self,*args,**kwargs):
        """
        Inicializacion de valores
        """

        cadena= None
        if 'cadena' in kwargs:
            cadena = kwargs.pop('cadena')

        # El parametro extra obtenido en la vista es objeto Actividad
        actividad = kwargs.pop('actividad')

        super(RegistroCadenasForm, self).__init__(*args, **kwargs)

        self.fields['tdr'] = \
             forms.ModelChoiceField(queryset=Tterminoreferencia.objects.filter(idactividad=actividad.idactividad),
                                     required=False)


        # Si se pasa una cadena se inicializa el formulario con el valor de la cadena
        if cadena:
            self.initial['tdr'] = cadena.tdr
            self.initial['tipo_matriz'] = cadena.tipo_matriz
            self.initial['laboratorio'] = cadena.laboratorio
            self.initial['referencia'] = cadena.referencia
            self.initial['fecha_resultados_lab'] = cadena.fecha_resultados_lab


class RegistroPuntoMuestra(forms.Form):
    """ Formulario para el registro de Puntos de Muestreo
    """
    nombre = forms.CharField()
    observacion = forms.CharField(widget=forms.Textarea, required=False)
    fecha_hora = forms.DateTimeField(input_formats=input_formats, required=False,
                                     widget=DateTimeWidget(attrs={'id':"fechahora"},
                                     bootstrap_version=3, options=datetimeOptions)
                                     )
    datum = forms.ModelChoiceField(queryset=SimuesDatum.objects.all().order_by('nombre'), required=False)
    gps = forms.ModelChoiceField(queryset=SimuesGPS.objects.all().order_by('marca'), required=False)
    tipo_punto = forms.ModelChoiceField(queryset=SimuesTipoPunto.objects.all().order_by('nombre'),
                                        required=False)
    tipo_muestra = forms.ModelChoiceField(queryset=SimuesTipoMuestra.objects.all().order_by('nombre'),
                                          required=False)
    altitud = forms.IntegerField(required=False, max_value=9999999999, label='Altitud (Solo valores enteros)')
    coord_norte = forms.IntegerField(required=False, label="UTM Norte (Solo valores enteros)")
    coord_este = forms.IntegerField(required=False, label="UTM Este (Solo valores enteros)")
    zona = forms.ModelChoiceField(queryset=SimuesZona.objects.all().order_by('nombre'), required=False)

    def __init__(self,*args,**kwargs):
        """
        Inicialización de valores
        """

        punto_muestreo= None
        if 'punto_muestreo' in kwargs:
            punto_muestreo = kwargs.pop('punto_muestreo')

        super(RegistroPuntoMuestra, self).__init__(*args, **kwargs)


        # Si se pasa una cadena se inicializa el formulario con el valor de la cadena
        if punto_muestreo:
            self.initial['observacion'] = punto_muestreo.observacion
            self.initial['nombre'] = punto_muestreo.nombre
            self.initial['datum'] = punto_muestreo.datum
            self.initial['gps'] = punto_muestreo.gps
            self.initial['tipo_punto'] = punto_muestreo.tipopunto
            self.initial['tipo_muestra'] = punto_muestreo.tipomuestra
            self.initial['fecha_hora'] = punto_muestreo.fecha_hora
            self.initial['altitud'] = punto_muestreo.altitud
            self.initial['coord_norte'] = punto_muestreo.coord_norte
            self.initial['coord_este'] = punto_muestreo.coord_este
            self.initial['zona'] = punto_muestreo.zona


    def clean_altitud(self):
        """Valida que coord_norte este dentro de sus coordenadas"""
        data = self.cleaned_data['altitud']

        if data is not None and type(data) is not int:
                raise forms.ValidationError("Valor no es entero")

        return data


    def clean_coord_norte(self):
        """Valida que coord_norte este dentro de sus coordenadas"""
        data = self.cleaned_data['coord_norte']
        if data is not None:
            # Comprobamos si el campo es un numero
            if type(data) is not int:
                raise forms.ValidationError("Valor no es entero")

            # Comprobamos si esta dentro del rango
            elif data < RANGO_COORDENADAS_NORTE[0] or data > RANGO_COORDENADAS_NORTE[1]:
                raise forms.ValidationError("Valor fuera del rango " + str(RANGO_COORDENADAS_NORTE[0]) +
                                            "-"+str(RANGO_COORDENADAS_NORTE[1]))

        return data


    def clean_coord_este(self):
        """Valida que coord_este este dentro de sus coordenadas"""
        data = self.cleaned_data['coord_este']

        if self.cleaned_data['coord_este'] is not None:
            if data < RANGO_COORDENADAS_ESTE[0] or data > RANGO_COORDENADAS_ESTE[1]:
                raise forms.ValidationError("Valor fuera del rango " + str(RANGO_COORDENADAS_ESTE[0]) +
                                            "-"+str(RANGO_COORDENADAS_ESTE[1]))

            elif type(data) is not int:
                raise forms.ValidationError("Valor no es entero")

        return data







class EnvasesForm(forms.Form):
    """
    Formulario donde se ingresa el número de envases por cada tipo
    """

    def __init__(self,*args,**kwargs):

        envases = None
        detalle_envases = None

        if 'envases' in kwargs:
            envases = kwargs.pop('envases')

        if 'detalle_envases' in kwargs:
            detalle_envases = kwargs.pop('detalle_envases')

        super(EnvasesForm, self).__init__(*args, **kwargs)

        if envases:
            # Se crean los campos
            for envase in envases:
                self.fields[str(envase.id)] = forms.IntegerField(required=False, min_value=0, max_value=1000,
                                                                 label=envase.nombre)

                if detalle_envases:
                    #Se les da valores a los campos
                    self.initial[str(envase.id)] = detalle_envases.get(envase=envase).numero



class ParametrosForm(forms.Form):
    """
    Formulario donde se ingresa si existe o no un parametro y el valor en el Punto de Muestreo
    """

    tdrdet_id = forms.CharField(required=False, max_length=40, widget=forms.HiddenInput())

    def __init__(self,*args,**kwargs):

        initial= None
        if 'initial' in kwargs:
            initial = kwargs.pop('initial')


        super(ParametrosForm, self).__init__(*args, **kwargs)

        if initial:
            # Campos escondidos donde se guardan los ids del parametro y del tdrdet

            # Se crean los campos bool e integer
            self.fields['check'] = \
                    forms.BooleanField(required=False,
                                       label=initial['detalle_tdr'].idparametro.txparametro+" check")
            self.fields['valor'] = \
                    forms.FloatField(required=False, label=initial['detalle_tdr'].idparametro.txparametro+" resultado")

            self.fields['unidad_medida'] = forms.ModelChoiceField(queryset=SimuesUnidadMedida.objects.all(),
                                                            required=False)

            # Valores iniciales de los campos escondidos
            self.initial['tdrdet_id'] = initial['detalle_tdr'].idtermrefdet

            if 'detalle_parametro' in initial:
                    #Se les da valores a los campos
                    self.initial['valor'] = initial['detalle_parametro'].valor
                    self.initial['check'] = initial['detalle_parametro'].check
                    self.initial['unidad_medida'] = initial['detalle_parametro'].unidad_medida


class SubirPuntoMuestraForm(forms.Form):

    archivo = forms.FileField(label="Archivo", required=True)



    def clean_archivo(self):
        """Clean file function"""

        archivo = self.cleaned_data.get('archivo')

        if archivo.content_type != 'text/xml':
            raise forms.ValidationError(('Solo se admiten Archivos Xml'))

        return archivo





