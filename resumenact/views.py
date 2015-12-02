# -*- coding: utf-8 -*-

import operator

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q

from .models import EfaActividad, SimuesProceso, SimuesProcesoSegActividadDET, SimuesSegActividad,\
                    DATE, INTEGER, BOOL, Tterminoreferencia, Tsector, Tcargosup, Tsubtipsup, \
                    SimuesSeguimientoSupervisores, Tunidadoperativa
from .forms import BusquedaForm, RegistroForm, ElegirCargoInspectoresForm

CODINSPECTORLIDER = 'CRS002'
CODINSPECTOR = 'CRS005'

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


@login_required
def index(request):
    """ Pantalla inicial del modulo de Seguimiento donde se buscan las actividades
    """

    # Obtiene la lista de grupos del usuario
    lista_grupos = []

    # Si no hay grupos en el usuario no lo deja loguearse
    if request.user.groups.all().count() > 0:
        for group in request.user.groups.all():
            lista_grupos.append(Q(txsector=group))

        # Obtiene los ids de los grupos del usuario
        idsector = Tsector.objects.filter(reduce(operator.or_, lista_grupos))
    else:
        messages.success(request, 'El usuario no pertenece a un grupo.', extra_tags='login')
        logout(request)
        return redirect('accounts/login/')


    if request.method == 'GET':
        # Crear una instancia del formulario
        form = BusquedaForm(request.GET)

        # Como hemos agregado a mano las las opciones con jquery
        # las agregamos a mano en el formulario antes de ser validado
        # http://stackoverflow.com/questions/28339713/while-using-ajax-with-django-form-getting-error-select-a-valid-choice-that-is
        #unidad = request.GET['unidad']
        #unidad = Tunidadoperativa.objects.get(idunidadoperativa = unidad)
        #form.fields['unidad'].choices = [(unidad.idunidadoperativa, unidad.txnombreunidad)]

        #print form['unidad']

        # Chequear si es válido

        if form.is_valid():

            mostrar = True

            # Lista las actividades por el grupo al que pertenece el usuario
            actividades = EfaActividad.objects.select_related(
                'idsubunidadoperativa__idunidadoperativa__txnombreunidad', 'idsubtipsup__txsubtipsup',
                'idsubtipsup__idtipsup__txtipsup', 'idadministrado__razonsocial', 'simuessegactividad__id'
            ).only('codactividad', 'fechaini','fechafin', 'idsubunidadoperativa__idunidadoperativa__txnombreunidad',
                   'idsubtipsup__txsubtipsup',
                   'idsubtipsup__idtipsup__txtipsup', 'idadministrado__razonsocial', 'simuessegactividad__id'
            ).filter(idsector_id__in = idsector)

            # Buscamos de acuerdo a los criterios ingresados en el formulario
            if form.cleaned_data['cuc']:
                actividades = actividades.filter(codactividad__contains=form.cleaned_data['cuc'])
            if form.cleaned_data['fecha_ini']:
                actividades = actividades.filter(fechaini__gte=form.cleaned_data['fecha_ini'])
            if form.cleaned_data['fecha_fin']:
                actividades = actividades.filter(fechafin__lte=form.cleaned_data['fecha_fin'])
            if form.cleaned_data['administrado']:
                actividades = actividades.filter(idadministrado=form.cleaned_data['administrado'])
            if form.cleaned_data['unidad']:
                actividades = actividades.filter(idunidadoperativa=form.cleaned_data['unidad'].idunidadoperativa)
            if form.cleaned_data['tdr']:
                if Tterminoreferencia.objects.filter(idtermref=form.cleaned_data['tdr'].idtermref).exists():
                    tdr = Tterminoreferencia.objects.get(idtermref=form.cleaned_data['tdr'].idtermref)
                    actividades = actividades.filter(idactividad=tdr.idactividad.idactividad)
            if form.cleaned_data['tipo_supervision']:
                actividades = actividades.filter(idtipsup_id = form.cleaned_data['tipo_supervision'])
            if form.cleaned_data['sub_tipo_supervision']:
                actividades = actividades.filter(idsubtipsup_id = form.cleaned_data['sub_tipo_supervision'])


            return render(request, 'resumenact/index.html',
                          {'form':form, 'actividades':actividades, 'mostrar':mostrar})

    # Si no es POST entonces se crea el formulario en blanco
    else:
        form = BusquedaForm()

    return render(request, 'resumenact/index.html', {'form':form})


@login_required
def obtener_unidades(request, administrado_id):
    """
    Función donde se devuelven las unidades relacionadas al administrado
    """

    combo_unidad_html = ""

    if Tunidadoperativa.objects.filter(idadministrado = administrado_id).exists():
        unidades = Tunidadoperativa.objects.filter(idadministrado = administrado_id)

        for unidad in unidades:
            combo_unidad_html += '<option value="'+str(unidad.idunidadoperativa)+'">'+unidad.txnombreunidad+'</option>'
    else:
        combo_unidad_html = "<option value='' selected='selected'>No se encontraron resultados</option>"


    return HttpResponse(combo_unidad_html)


@login_required
def obtener_subtipos_supervision(request, tiposupervision_id):
    """
    Función donde se devuelven las unidades relacionadas al administrado
    """

    combo_subtipo_html = ""

    if Tsubtipsup.objects.filter(idtipsup = tiposupervision_id).exists():
        subtipos = Tsubtipsup.objects.filter(idtipsup = tiposupervision_id)

        for subtipo in subtipos:
            combo_subtipo_html += '<option value="'+str(subtipo.idsubtipsup)+'">'+subtipo.txsubtipsup+'</option>'
            print combo_subtipo_html
    else:
        combo_unidad_html = "<option value='' selected='selected'>No se encontraron resultados</option>"


    return HttpResponse(combo_subtipo_html)



@login_required
def registro(request, actividad_id):
     """ Formulario de registro de Seguimiento de Actividades """

     # Se elige el tipo de inspector líder de la tabla de Cargos de Supervisiones
     tipo_inspector_lider = Tcargosup.objects.get(idcargosup=CODINSPECTORLIDER)
     # Se elige el tipo de inspector de la tabla de Cargos de Supervisiones
     tipo_inspector = Tcargosup.objects.get(idcargosup=CODINSPECTOR)

     # Lee los valores de Proceso
     procesos = SimuesProceso.objects.all().order_by('id')

     # Si no obtiene el id de la actividad redirige al error 404
     actividad = get_object_or_404(EfaActividad, idactividad=actividad_id)

     # Asignamos los valores iniciales
     supervisores_actividad = SimuesSeguimientoSupervisores.objects.filter(actividad=actividad)

     supervisores = {}

     if supervisores_actividad.filter(cargo=tipo_inspector).exists():
         supervisores['inspector'] = supervisores_actividad.get(cargo=tipo_inspector)
     if supervisores_actividad.filter(cargo=tipo_inspector_lider).exists():
         supervisores['inspector_lider'] = supervisores_actividad.get(cargo=tipo_inspector_lider)

     # Inicializamos el formulario para Elegir los cargos de los inspectores asociados a la actividad
     form_elegir = ElegirCargoInspectoresForm(actividad=actividad, supervisores=supervisores)

     if request.method == 'POST':

         # Crear una instancia del formulario con los parametros extras
         form_seguimiento = RegistroForm(request.POST, extra = procesos)

         # Chequear si es válido
         if form_seguimiento.is_valid():

             if SimuesSegActividad.objects.filter(id=actividad).exists():
                 segact = SimuesSegActividad.objects.get(id=actividad)

                 # Iteramos sobre los campos del formulario y guardamos los valores dependiendo del tipo de dato
                 for (nombre, valor) in form_seguimiento.procesos():
                     # Comprobamos si existe el Proceso en la bd antes de obtenerlo
                     if SimuesProceso.objects.filter(id = nombre).exists():
                         proceso = SimuesProceso.objects.get(id = nombre)

                         # Comprobamos si existe el detalle del proceso y seguimiento.
                         # Si existe guardamos el valor del campo
                         if SimuesProcesoSegActividadDET.objects.filter(idsegactividad=segact,
                                                                        idproceso=proceso).exists():
                             detalle = SimuesProcesoSegActividadDET.objects.get(idsegactividad=segact,
                                                                                idproceso=proceso)

                             grabar = False
                             if proceso.tipo_dato == DATE  and detalle.fecha != form_seguimiento.cleaned_data[str(nombre)]:
                                 detalle.fecha = form_seguimiento.cleaned_data[str(nombre)]
                                 grabar = True
                             elif proceso.tipo_dato == INTEGER and detalle.num != form_seguimiento.cleaned_data[str(nombre)]:
                                 detalle.num = form_seguimiento.cleaned_data[str(nombre)]
                                 grabar = True
                             elif proceso.tipo_dato == BOOL and detalle.sino != form_seguimiento.cleaned_data[str(nombre)]:
                                 detalle.sino = form_seguimiento.cleaned_data[str(nombre)]
                                 grabar = True

                             if grabar:
                                 detalle.modified_by = request.user
                                 detalle.save()


                 # Mensaje para saber que se guardo con éxito
                 messages.success(request, 'Las actividades de Supervisión se grabaron satisfactoriamente',
                                  extra_tags='seguimiento')

             else:
                 # En caso de que no exista se crea el Seguimiento
                 segact = SimuesSegActividad(id=actividad)
                 segact.save()

                 # Iteramos sobre los campos del formulario y guardamos los valores dependiendo del tipo de dato
                 for (nombre, valor) in form_seguimiento.procesos():
                     proceso = SimuesProceso.objects.get(id = nombre)

                     if proceso.tipo_dato == DATE:
                         detalle = SimuesProcesoSegActividadDET(idsegactividad=segact,
                                                                idproceso=proceso, fecha=valor)
                     elif proceso.tipo_dato == INTEGER:
                         detalle = SimuesProcesoSegActividadDET(idsegactividad=segact,
                                                                idproceso=proceso, num=valor)
                     elif proceso.tipo_dato == BOOL:
                         detalle = SimuesProcesoSegActividadDET(idsegactividad=segact,
                                                                idproceso=proceso, sino=valor)

                     detalle.created_by = request.user
                     detalle.modified_by = request.user
                     detalle.save()

                 # Mensaje para saber que se guardo con éxito
                 messages.success(request, 'Las actividades de Supervisión se grabaron satisfactoriamentes',
                                  extra_tags='seguimiento')

             return render(request, 'resumenact/registro.html',
                           {'form_seguimiento':form_seguimiento,
                            'form_elegir':form_elegir,
                            'segact_id':actividad_id,
                            'actividad':actividad})

     else:

         # Si existe se obtiene el Seguimiento
         segact = get_or_none(SimuesSegActividad, id=actividad)

         if segact:
             form_seguimiento = RegistroForm(extra = procesos, segact=segact)

             return render(request, 'resumenact/registro.html', {'form_seguimiento':form_seguimiento,
                                                                 'segact_id':actividad_id,
                                                                 'form_elegir':form_elegir,
                                                                 'actividad':actividad})
         else:
             form_seguimiento = RegistroForm(extra = procesos)

     return render(request, 'resumenact/registro.html', {'form_seguimiento':form_seguimiento,
                                                         'form_elegir':form_elegir,
                                                         'actividad':actividad})



def elegir_cargo_inspectores(request, actividad_id):
    """Seleccionar los inspectores en sus respectivos cargos"""

    # Se elige el tipo de inspector líder de la tabla de Cargos de Supervisiones
    tipo_inspector_lider = Tcargosup.objects.get(idcargosup=CODINSPECTORLIDER)
    # Se elige el tipo de inspector de la tabla de Cargos de Supervisiones
    tipo_inspector = Tcargosup.objects.get(idcargosup=CODINSPECTOR)

    # Si no obtiene el id de la actividad redirige al error 404
    actividad = get_object_or_404(EfaActividad, idactividad=actividad_id)

    # Queryset de de los supervisores de la actividad
    supervisores_actividad = SimuesSeguimientoSupervisores.objects.filter(actividad=actividad)

    # diccionario a pasar como valor inicial al formulario
    supervisores = {}

    if supervisores_actividad.filter(cargo=tipo_inspector).exists():
         supervisores['inspector'] = supervisores_actividad.get(cargo=tipo_inspector)
    if supervisores_actividad.filter(cargo=tipo_inspector_lider).exists():
         supervisores['inspector_lider'] = supervisores_actividad.get(cargo=tipo_inspector_lider)

    # Inicializamos el formulario para Elegir los cargos de los inspectores asociados a la actividad
    form_elegir = ElegirCargoInspectoresForm(actividad=actividad, supervisores=supervisores)

    if request.method == 'POST':

        form_elegir = ElegirCargoInspectoresForm(request.POST,actividad=actividad, supervisores=supervisores)

        if form_elegir.is_valid():

            # Se comprueba si existe el inspector lider, si existe se modifica, caso contrario se
            # crea un nuevo objeto.

            if form_elegir.cleaned_data['inspector_lider'] :

                if supervisores_actividad.filter(cargo=tipo_inspector_lider).exists():

                    inspector_lider = supervisores_actividad.get(cargo=tipo_inspector_lider)

                    if inspector_lider.supervisor != form_elegir.cleaned_data['inspector_lider']:

                        inspector_lider.supervisor = form_elegir.cleaned_data['inspector_lider']
                        inspector_lider.modified_by = request.user
                        inspector_lider.save()

                        messages.success(request, 'Los datos del Inspector Lider se grabaron correctamente',
                                         extra_tags='inspector')

                else:

                    inspector_lider = SimuesSeguimientoSupervisores(
                        actividad=actividad,
                        cargo=tipo_inspector_lider,
                        #supervisor=EfaSupervisor.objects.get(id=form_elegir.cleaned_data['inspector_lider'])
                        supervisor=form_elegir.cleaned_data['inspector_lider']
                    )

                    inspector_lider.created_by = request.user
                    inspector_lider.modified_by = request.user

                    inspector_lider.save()

                    # Mensaje para saber que se guardo con éxito
                    messages.success(request, 'Los datos del Inspector Lider se grabaron correctamente',
                                     extra_tags='inspector')

            # Se comprueba si existe el inspector, si existe se modifica, caso contrario se
            # crea un nuevo objeto.

        if form_elegir.cleaned_data['inspector']:

            if supervisores_actividad.filter(cargo=tipo_inspector).exists():

                inspector = supervisores_actividad.get(cargo=tipo_inspector)

                if inspector.supervisor != form_elegir.cleaned_data['inspector']:

                    inspector.supervisor = form_elegir.cleaned_data['inspector']
                    inspector.modified_by = request.user
                    inspector.save()

                    messages.success(request, 'Los datos del Inspector se grabaron correctamente',
                                 extra_tags='inspector')

            else:
                inspector = SimuesSeguimientoSupervisores(
                    actividad=actividad,
                    cargo=tipo_inspector,
                    supervisor=form_elegir.cleaned_data['inspector'])

                inspector.created_by = request.user
                inspector.modified_by = request.user
                inspector.save()

                # Mensaje para saber que se guardo con éxito
                messages.success(request, 'Los datos del Inspector se grabaron correctamente',
                                 extra_tags='inspector')

    return redirect('resumenact:registro', actividad_id=actividad_id)