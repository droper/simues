# -*- coding: utf-8 -*-

from django.db import models

from resumenact.models import Tterminoreferencia, Tlaboratorio, EfaActividad, Tsubmatriz, Tterminoreferenciadet, \
    Auditable, Tanalisis

from simues.settings import SIMUES_USER



class SimuesZona(models.Model):
    nombre = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesZona"'


class SimuesDatum(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesDatum"'


class SimuesGPS(models.Model):
    marca = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.marca

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesGPS"'


class SimuesTipoPunto(models.Model):
    nombre = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesTipoPunto"'

class SimuesTipoMuestra(models.Model):
    nombre = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesTipoMuestra"'


class SimuesTipoEnvase(models.Model):
    nombre = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesTipoEnvase"'


class SimuesCadenaCustodia(Auditable):
    tdr = models.ForeignKey(Tterminoreferencia, blank=True, null=True)
    tipo_matriz = models.ForeignKey(Tsubmatriz, blank=True, null=True, to_field='idsubmatriz')
    actividad = models.ForeignKey(EfaActividad, to_field='idactividad', blank=True, null=True)
    nro_orden = models.IntegerField(default=1, blank=True, null=True)
    laboratorio = models.ForeignKey(Tlaboratorio, to_field='idlaboratorio', blank=True, null=True)
    correlativo = models.CharField(max_length=40, default='SIN CORRELATIVO')
    fecha_resultados_lab =  models.DateTimeField(blank=True, null=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.correlativo

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesCadenaCustodia"'

    def analisis(self):
        """
        Devuelve el análisis del tdr de la cadena
        """
        if self.tdr:
            if Tanalisis.objects.filter(idanalisis = self.tdr.idanalisis).exists():
                return Tanalisis.objects.get(idanalisis = self.tdr.idanalisis).txanalisis
        return False

    def numero_cadenas(self):
        """
        Devuelve la cantidad de cadenas asociadas al tdr
        """
        num_cadenas = 0

        if self.tdr:
            num_cadenas = self.tdr.simuescadenacustodia_set.all().count()
        return num_cadenas


class SimuesPuntoMuestreo(Auditable):
    nombre = models.CharField(max_length=40, blank=True, null=True)
    cadena = models.ForeignKey(SimuesCadenaCustodia, blank=True, null=True)
    zona = models.ForeignKey(SimuesZona, blank=True, null=True)
    datum = models.ForeignKey(SimuesDatum, blank=True, null=True)
    gps =  models.ForeignKey(SimuesGPS, blank=True, null=True)
    tipomuestra = models.ForeignKey(SimuesTipoMuestra, blank=True, null=True)
    tipopunto =  models.ForeignKey(SimuesTipoPunto, blank=True, null=True)
    observacion = models.TextField(max_length=300, blank=True, null=True)
    envases = models.ManyToManyField(SimuesTipoEnvase, through='SimuesPuntoMuestreoEnvases')
    parametros = models.ManyToManyField(Tterminoreferenciadet,
                                        through='SimuesPuntoMuestreoTerminoReferenciaDet')
    fecha_hora = models.DateTimeField(blank=True, null=True)
    altitud = models.BigIntegerField(blank=True, null=True)
    coord_norte = models.BigIntegerField(blank=True, null=True)
    coord_este = models.BigIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesPuntoMuestreo"'


class SimuesUnidadMedida(models.Model):
    nombre = models.CharField(max_length=40)
    simbolo = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesUnidadMedida"'


class SimuesPuntoMuestreoTerminoReferenciaDet(Auditable):
    punto = models.ForeignKey(SimuesPuntoMuestreo)
    tdrdet = models.ForeignKey(Tterminoreferenciadet,    to_field='idtermrefdet')
    unidad_medida = models.ForeignKey(SimuesUnidadMedida, blank=True, null=True)
    check = models.NullBooleanField()
    valor = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.punto.nombre

    class Meta:
        unique_together = (("punto", "tdrdet" ),)
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesPuntoMuestre0bc3"'


class SimuesPuntoMuestreoEnvases(Auditable):
    punto = models.ForeignKey(SimuesPuntoMuestreo)
    envase= models.ForeignKey(SimuesTipoEnvase)
    numero = models.IntegerField(blank=True, null=True  )

    class Meta:
        unique_together = (("punto", "envase"),)
        db_table = '"' + SIMUES_USER +'"'+ '."cadenas_SimuesPuntoMuestre0ad9"'

    def __unicode__(self):
        return self.punto.nombre + " " + self.envase.nombre + " " + str(self.numero)
