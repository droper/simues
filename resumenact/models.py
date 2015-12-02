# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry

from allauth.account.models import EmailAddress, EmailConfirmation


from simues.settings import SIMUES_USER


class Tlaboratorio(models.Model):
    idlaboratorio = models.CharField(primary_key=True, max_length=6)
    txlaboratorio = models.CharField(max_length=150, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tlaboratorio"'

    def __unicode__(self):
        return self.txlaboratorio

class Tsector(models.Model):
    idsector = models.CharField(primary_key=True, max_length=20)
    txsector = models.CharField(max_length=255, blank=True, null=True)
    txsigla = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tsector"'



class EfaActividad(models.Model):
    idactividad = models.BigIntegerField(primary_key=True)
    idtipsup = models.ForeignKey('Ttipsup', db_column='idtipsup', blank=True, null=True)
    idsubtipsup = models.ForeignKey('Tsubtipsup', db_column='idsubtipsup', blank=True, null=True)
    agua = models.CharField(max_length=5, blank=True, null=True)
    aire = models.CharField(max_length=5, blank=True, null=True)
    analitica = models.CharField(max_length=5, blank=True, null=True)
    codactividad = models.CharField(max_length=255, blank=True, null=True)
    departamento = models.CharField(max_length=255, blank=True, null=True)
    departamentodes = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    distrito = models.CharField(max_length=255, blank=True, null=True)
    distritodes = models.CharField(max_length=255, blank=True, null=True)
    efluentes = models.CharField(max_length=5, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    estadoejec = models.CharField(max_length=255, blank=True, null=True)
    estadomatriz = models.CharField(max_length=255, blank=True, null=True)
    fechafin = models.DateTimeField(blank=True, null=True)
    fechaini = models.DateTimeField(blank=True, null=True)
    hallazgo = models.CharField(max_length=5, blank=True, null=True)
    horafin = models.CharField(max_length=5, blank=True, null=True)
    horaini = models.CharField(max_length=5, blank=True, null=True)
    idefa = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    idsupres = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    nivel = models.CharField(max_length=1, blank=True, null=True)
    provincia = models.CharField(max_length=255, blank=True, null=True)
    provinciades = models.CharField(max_length=255, blank=True, null=True)
    suelo = models.CharField(max_length=5, blank=True, null=True)
    supervision = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    flgactivo = models.CharField(max_length=2, blank=True, null=True)
    usuario = models.CharField(max_length=20, blank=True, null=True)
    perfil = models.CharField(max_length=20, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)
    txdescactividad = models.CharField(max_length=500, blank=True, null=True)
    idsector = models.ForeignKey(Tsector, db_column='idsector', max_length=6, blank=True, null=True)
    idadministrado = models.ForeignKey('Tadministrado', db_column='idadministrado', blank=True, null=True)
    idunidadoperativa = models.CharField(max_length=20, blank=True, null=True)
    idsubunidadoperativa = models.ForeignKey('Tsubunidadoperativa', db_column='idsubunidadoperativa',
                                             blank=True, null=True)
    messup = models.BigIntegerField(blank=True, null=True)
    txobsotros = models.CharField(max_length=500, blank=True, null=True)
    fgfuente = models.CharField(max_length=1, blank=True, null=True)
    laboratorios = models.ManyToManyField(Tlaboratorio, through='EfaActividadLaboratorio')

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."efa_actividad"'

    def __unicode__(self):
        return str(self.idactividad)

    def tdrs(self):
        tdrs = self.tterminoreferencia_set.all()
        tdr_list = []
        for tdr in tdrs:
            tdr_list.append(tdr.txcodigo)
        return tdr_list


class EfaActividadLaboratorio(models.Model):
    idactividadlaboratorio = models.BigIntegerField(primary_key=True, db_column='idactividadlaboratorio ')
    idactividad = models.ForeignKey(EfaActividad, db_column='idactividad')
    idlaboratorio = models.ForeignKey('Tlaboratorio', db_column='idlaboratorio')
    fgexcluido = models.CharField(max_length=1, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."efa_actividad_laboratorio"'
        unique_together = (('idactividad', 'idlaboratorio'),)


class EfaActividadSupervisor(models.Model):
    idactividadsupervisor = models.BigIntegerField(primary_key=True, db_column='idactividadsupervisor', null=True)
    idactividad = models.ForeignKey(EfaActividad, db_column='idactividad', null=True)
    idsupervisor = models.ForeignKey('EfaSupervisor', db_column='idsupervisor', null=True)
    idcargosup = models.ForeignKey('Tcargosup', db_column='idcargosup', null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."efa_actividad_supervisor"'
        unique_together = (('idcargosup', 'idsupervisor', 'idactividad'),)


    def save(self, *args, **kwargs):
        if self.idactividadsupervisor is None:
            self.idactividadsupervisor = \
                self.__class__.objects.all().order_by("-idactividadsupervisor")[0].idactividadsupervisor + 1
        else:
            self.idactividadsupervisor = self.idactividadsupervisor
        super(self.__class__, self).save(*args, **kwargs)


    def __unicode__(self):
        return str(self.idsupervisor)


class EfaSupervisor(models.Model):
    id = models.BigIntegerField(primary_key=True)
    apmaterno = models.CharField(max_length=255, blank=True, null=True)
    appaterno = models.CharField(max_length=255, blank=True, null=True)
    cargo = models.CharField(max_length=255, blank=True, null=True)
    correo = models.CharField(max_length=255, blank=True, null=True)
    correo_ins = models.CharField(max_length=255, blank=True, null=True)
    cuenta_bco = models.CharField(max_length=255, blank=True, null=True)
    departamento = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    distrito = models.CharField(max_length=255, blank=True, null=True)
    dni = models.CharField(max_length=8, blank=True, null=True)
    estado_civil = models.CharField(max_length=1, blank=True, null=True)
    fecha_nac = models.DateTimeField(blank=True, null=True)
    fin_laboral = models.DateTimeField(blank=True, null=True)
    ini_laboral = models.DateTimeField(blank=True, null=True)
    modalidad = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    nro_contrato = models.CharField(max_length=255, blank=True, null=True)
    otro_bco = models.CharField(max_length=255, blank=True, null=True)
    otro_bco_nro = models.CharField(max_length=255, blank=True, null=True)
    profesion = models.CharField(max_length=255, blank=True, null=True)
    provincia = models.CharField(max_length=255, blank=True, null=True)
    remuneracion = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    telefono = models.CharField(max_length=25, blank=True, null=True)
    flgactivo = models.CharField(max_length=2, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    usureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    usumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."efa_supervisor"'

    def __unicode__(self):
        return self.nombre +" "+self.appaterno+" "+self.apmaterno



class Tcargosup(models.Model):
    idcargosup = models.CharField(primary_key=True, max_length=6)
    txcargosup = models.CharField(max_length=150, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tcargosup"'


class Ttipsup(models.Model):
    idtipsup = models.CharField(primary_key=True, max_length=6)
    txtipsup = models.CharField(max_length=150, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."ttipsup"'

    def __unicode__(self):
        return self.txtipsup


class Tsubtipsup(models.Model):
    idsubtipsup = models.CharField(primary_key=True, max_length=6)
    idtipsup = models.ForeignKey(Ttipsup, db_column='idtipsup', blank=True, null=True)
    txsubtipsup = models.CharField(max_length=100, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tsubtipsup"'

    def __unicode__(self):
        return self.txsubtipsup


class Tanalisis(models.Model):
    idanalisis = models.CharField(primary_key=True, max_length=7)
    txanalisis = models.CharField(max_length=60, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1)
    idusureg = models.CharField(max_length=50)
    fereg = models.DateField()
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tanalisis"'


class Tactividad(models.Model):
    idactividad = models.CharField(primary_key=True, max_length=20)
    idcategoria = models.ForeignKey('Tcategoria', db_column='idcategoria', blank=True, null=True)
    txactividad = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tactividad"'


class Tcategoria(models.Model):
    idcategoria = models.CharField(primary_key=True, max_length=20)
    idsector = models.ForeignKey('Tsector', db_column='idsector', blank=True, null=True)
    txcategoria = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tcategoria"'


class Tparametro(models.Model):
    idparametro = models.CharField(primary_key=True, max_length=7)
    txparametro = models.CharField(max_length=150, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tparametro"'

    def __unicode__(self):
        return self.txparametro


class Tmatriz(models.Model):
    idmatriz = models.CharField(primary_key=True, max_length=7)
    idanalisis = models.ForeignKey(Tanalisis, db_column='idanalisis', blank=True, null=True)
    txmatriz = models.CharField(max_length=150, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tmatriz"'


class Tsubmatriz(models.Model):
    idsubmatriz = models.CharField(primary_key=True, max_length=7)
    idmatriz = models.ForeignKey(Tmatriz, db_column='idmatriz', blank=True, null=True)
    txsubmatriz = models.CharField(max_length=150, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tsubmatriz"'

    def __unicode__(self):
        return self.txsubmatriz


class TsubmatrizParametro(models.Model):
    idsubmatriz = models.ForeignKey(Tsubmatriz, db_column='idsubmatriz')
    idparametro = models.ForeignKey(Tparametro, db_column='idparametro')
    idanalisis = models.CharField(max_length=7, blank=True, null=True)
    idmatriz = models.CharField(max_length=7, blank=True, null=True)
    monto = models.DecimalField(max_digits=16, decimal_places=4, blank=True, null=True)
    fgcontrato = models.CharField(max_length=1, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tsubmatriz_parametro"'
        unique_together = (('idsubmatriz', 'idparametro'),)


class Tterminoreferencia(models.Model):
    idtermref = models.CharField(primary_key=True, max_length=10)
    idtipotermref = models.ForeignKey('Ttipotermref', db_column='idtipotermref', blank=True, null=True)
    txcodigo = models.CharField(max_length=15, blank=True, null=True)
    txanio = models.CharField(max_length=4, blank=True, null=True)
    txmetasiaf = models.CharField(max_length=10, blank=True, null=True)
    txnotref = models.CharField(max_length=250, blank=True, null=True)
    feprogramada = models.DateField(blank=True, null=True)
    feentmateriales = models.DateField(blank=True, null=True)
    nupretotal = models.DecimalField(max_digits=16, decimal_places=4, blank=True, null=True)
    idestado = models.CharField(max_length=6, blank=True, null=True)
    txacttermref = models.CharField(max_length=20, blank=True, null=True)
    txmattermref = models.CharField(max_length=250, blank=True, null=True)
    idsector = models.ForeignKey(Tsector, db_column='idsector', max_length=6, blank=True, null=True)
    idanalisis = models.CharField(max_length=7, blank=True, null=True)
    txobstermref = models.CharField(max_length=250, blank=True, null=True)
    txnotreftermref = models.CharField(max_length=250, blank=True, null=True)
    txdniperreferencia = models.CharField(max_length=8, blank=True, null=True)
    txdniperoficina = models.CharField(max_length=8, blank=True, null=True)
    txdnipertecnico = models.CharField(max_length=8, blank=True, null=True)
    txptomonitoreo = models.CharField(max_length=25, blank=True, null=True)
    fefinprogramada = models.DateField(blank=True, null=True)
    txcodidentificacion = models.CharField(max_length=10, blank=True, null=True)
    idactividad = models.ForeignKey(EfaActividad, db_column='idactividad', blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)
    txnomperreferencia = models.CharField(max_length=300, blank=True, null=True)
    txnomperoficina = models.CharField(max_length=300, blank=True, null=True)
    txnompertecnico = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tterminoreferencia"'

    def __unicode__(self):
        return self.txcodigo


class Tterminoreferenciadet(models.Model):
    idtermrefdet = models.BigIntegerField(primary_key=True)
    idtermref = models.ForeignKey(Tterminoreferencia, db_column='idtermref')
    idmatriz = models.CharField(max_length=7, blank=True, null=True)
    idsubmatriz = models.ForeignKey(Tsubmatriz, db_column='idsubmatriz')
    idparametro = models.ForeignKey(Tparametro, db_column='idparametro')
    cntmuestra = models.BigIntegerField(blank=True, null=True)
    txobservacion = models.CharField(max_length=4000, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tterminoreferenciadet"'
        unique_together = (('idtermref', 'idsubmatriz', 'idparametro'),)

    def __unicode__(self):
        return str(self.idtermref)+" / "+str(self.idtermrefdet)+" / "+self.idsubmatriz.txsubmatriz \
               +" / "+self.idparametro.txparametro


class Ttipotermref(models.Model):
    idtipotermref = models.CharField(primary_key=True, max_length=6)
    txtipotermref = models.CharField(max_length=100, blank=True, null=True)
    txabreviacion = models.CharField(max_length=20, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."ttipotermref"'


class Tadministrado(models.Model):
    idadministrado = models.CharField(primary_key=True, max_length=20)
    tipopersona = models.CharField(max_length=2, blank=True, null=True)
    ruc = models.CharField(unique=True, max_length=11, blank=True, null=True)
    razonsocial = models.CharField(max_length=255, blank=True, null=True)
    tipodoc = models.CharField(max_length=1, blank=True, null=True)
    numerodoc = models.CharField(max_length=12, blank=True, null=True)
    nombres = models.CharField(max_length=255, blank=True, null=True)
    appaterno = models.CharField(max_length=255, blank=True, null=True)
    apmaterno = models.CharField(max_length=255, blank=True, null=True)
    departamento = models.CharField(max_length=20, blank=True, null=True)
    departamentodes = models.CharField(max_length=255, blank=True, null=True)
    provincia = models.CharField(max_length=20, blank=True, null=True)
    provinciades = models.CharField(max_length=255, blank=True, null=True)
    distrito = models.CharField(max_length=20, blank=True, null=True)
    distritodes = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    reptipodoc = models.CharField(max_length=20, blank=True, null=True)
    repnumdoc = models.CharField(max_length=12, blank=True, null=True)
    repnombres = models.CharField(max_length=255, blank=True, null=True)
    repappaterno = models.CharField(max_length=255, blank=True, null=True)
    repapmaterno = models.CharField(max_length=255, blank=True, null=True)
    flgactivo = models.CharField(max_length=2, blank=True, null=True)
    txcodigo = models.CharField(max_length=50, blank=True, null=True)
    txemail1 = models.CharField(max_length=100, blank=True, null=True)
    txemail2 = models.CharField(max_length=100, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tadministrado"'

    def __unicode__(self):
        return self.razonsocial


class Tsituacion(models.Model):
    idsituacion = models.CharField(primary_key=True, max_length=6)
    txsituacion = models.CharField(max_length=150, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tsituacion"'

    def __unicode__(self):
        return self.razonsocial


class Tunidadoperativa(models.Model):
    idunidadoperativa = models.CharField(primary_key=True, max_length=20)
    idadministrado = models.ForeignKey(Tadministrado, db_column='idadministrado', blank=True, null=True)
    txtelefono = models.CharField(max_length=20, blank=True, null=True)
    txcorreo = models.CharField(max_length=150, blank=True, null=True)
    txdomfiscal = models.CharField(max_length=255, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)
    txnombreunidad = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tunidadoperativa"'

    def __unicode__(self):
        return self.txnombreunidad


class Tsubunidadoperativa(models.Model):
    idsubunidadoperativa = models.CharField(primary_key=True, max_length=20)
    sector = models.CharField(max_length=20, blank=True, null=True)
    actividad = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    tipodm = models.CharField(max_length=20, blank=True, null=True)
    nombredm = models.CharField(max_length=100, blank=True, null=True)
    codinacc = models.CharField(max_length=30, blank=True, null=True)
    departamento = models.CharField(max_length=2, blank=True, null=True)
    departamentodes = models.CharField(max_length=255, blank=True, null=True)
    provincia = models.CharField(max_length=2, blank=True, null=True)
    provinciades = models.CharField(max_length=255, blank=True, null=True)
    distrito = models.CharField(max_length=2, blank=True, null=True)
    distritodes = models.CharField(max_length=255, blank=True, null=True)
    cuenca = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    norte = models.CharField(max_length=15, blank=True, null=True)
    este = models.CharField(max_length=15, blank=True, null=True)
    zona = models.CharField(max_length=5, blank=True, null=True)
    direccionunidad = models.CharField(max_length=255, blank=True, null=True)
    nombresubunidad = models.CharField(max_length=255, blank=True, null=True)
    flgactivo = models.CharField(max_length=2, blank=True, null=True)
    idunidadoperativa = models.ForeignKey('Tunidadoperativa', db_column='idunidadoperativa', blank=True, null=True)
    idsituacion = models.ForeignKey(Tsituacion, db_column='idsituacion', blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tsubunidadoperativa"'

    def __unicode__(self):
        return self.idunidadoperativa.txnombreunidad


class TsubunidadoperativaActividad(models.Model):
    idsubunidadoperativaactividad = models.CharField(primary_key=True, max_length=20)
    idcategoria = models.CharField(max_length=20, blank=True, null=True)
    idactividad = models.CharField(max_length=20, blank=True, null=True)
    fgsitreg = models.CharField(max_length=1, blank=True, null=True)
    idusureg = models.CharField(max_length=50, blank=True, null=True)
    fereg = models.DateField(blank=True, null=True)
    idusumod = models.CharField(max_length=50, blank=True, null=True)
    femod = models.DateField(blank=True, null=True)
    idusueli = models.CharField(max_length=50, blank=True, null=True)
    feeli = models.DateField(blank=True, null=True)
    idsubunidadoperativa = models.ForeignKey(Tsubunidadoperativa, db_column='idsubunidadoperativa', blank=True,
                                             null=True)

    class Meta:
        managed = False
        db_table = '"' + SIMUES_USER +'"'+ '."tsubunidadoperativa_actividad"'


# Modelos modificados

User._meta.db_table =  SIMUES_USER +'\"'+ '.\"auth_user'
Group._meta.db_table = SIMUES_USER +'\"'+ '.\"auth_group'
Permission._meta.db_table = SIMUES_USER +'\"'+ '.\"auth_permission'
Group.permissions.through._meta.db_table = '"' + SIMUES_USER +'"."auth_group_permissions"'
User.groups.through._meta.db_table = '"' + SIMUES_USER +'"."auth_user_groups"'
User.user_permissions.through._meta.db_table = '"' + SIMUES_USER +'"'+ '."AUTH_USER_USER_PERMISSIONS"'
#User.user_permissions.through._meta.db_table = '"SISUD"."AUTH_USER_USER_PERMISSIONS"'

EmailAddress._meta.db_table = SIMUES_USER +'\"'+ '.\"account_emailaddress'
EmailConfirmation._meta.db_table = '"' + SIMUES_USER +'"."account_emailconfirmation"'


Site._meta.db_table = SIMUES_USER + '\"' + '.\"django_site'
#Session._meta.db_table = '"' + SIMUES_USER +'"'+ '."django_session"'
Session._meta.db_table = SIMUES_USER + '\"' + '.\"django_session'
ContentType._meta.db_table = SIMUES_USER + '\"' + '.\"django_content_type'
LogEntry._meta.db_table = SIMUES_USER + '\"' + '.\"django_admin_log'


# Clases Propias

class UsuarioExtendido(models.Model):
    user = models.OneToOneField(User)
    apellido_materno = models.CharField(max_length=100)

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."resumenact_UsuarioExtendido"'


DATE = 'DATE'
BOOL = 'BOOL'
INTEGER = 'INTEGER'
MAX_LENGTH = 20


class Auditable(models.Model):
    """Modelo abstracto con la data de auditoria, todos los modelos heredaran de este"""

    created_on = models.DateTimeField(auto_now_add = True,
                                      editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="%(class)s_related",
                                   editable=False,
                                   null=True,
                                   blank=True)

    modified_on = models.DateTimeField(auto_now = True,
                                       editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="%(class)s_related_mod",
                                    editable=False,
                                    null=True,
                                    blank=True)

    class Meta:
        abstract = True


class SimuesProceso(models.Model):
    TIPO_DATOS = ((DATE, 'Fecha'),
                  (BOOL, 'Booleano'),
                 (INTEGER, 'Entero'))

    nombre = models.CharField(max_length=100)
    tipo_dato = models.CharField(max_length=MAX_LENGTH,
                              choices=TIPO_DATOS,
                              default=DATE)

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."resumenact_simuesproceso"'


class SimuesSegActividad(models.Model):
    id = models.OneToOneField(EfaActividad, primary_key=True)
    procesos = models.ManyToManyField(SimuesProceso, through='SimuesProcesoSegActividadDET')

    def __unicode__(self):
        return unicode(self.id)

    class Meta:
        db_table = '"' + SIMUES_USER +'"'+ '."resumenact_SimuesSegActividad"'


class SimuesProcesoSegActividadDET(Auditable):
    """
    Modelo many to many entre Seguimiento y Procesos
    """
    idsegactividad = models.ForeignKey(SimuesSegActividad, blank=True, null=True)
    idproceso = models.ForeignKey(SimuesProceso, db_column='idsimuesproceso_id', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    sino = models.NullBooleanField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (("idsegactividad", "idproceso" ),)
        db_table = '"' + SIMUES_USER +'"'+ '."resumenact_SimuesProcesoSe4521"'


class SimuesSeguimientoSupervisores(Auditable):
    """
    Modelo donde se guardan los los Supervisores asignados al Seguimiento
    """
    actividad = models.ForeignKey(EfaActividad, blank=True, null=True)
    cargo = models.ForeignKey(Tcargosup, blank=True, null=True)
    supervisor = models.ForeignKey(EfaSupervisor, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.supervisor)

    class Meta:
        db_table = '"' + SIMUES_USER +'"."resumenact_SimuesSeguimiendf8e"'
