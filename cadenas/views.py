# -*- coding: utf-8 -*-
from datetime import date


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.forms.formsets import formset_factory

from resumenact.models import EfaActividad, Tterminoreferencia, Tterminoreferenciadet, Tsubmatriz, Tlaboratorio, Tsector
from .models import SimuesCadenaCustodia, SimuesTipoMuestra, SimuesPuntoMuestreo, SimuesTipoEnvase, \
    SimuesPuntoMuestreoEnvases, SimuesPuntoMuestreoTerminoReferenciaDet,SimuesUnidadMedida

from .forms import RegistroCadenasForm, RegistroPuntoMuestra, EnvasesForm, ParametrosForm, SubirPuntoMuestraForm



@login_required
def lista(request, actividad_id):
    """ Pantalla inicial del modulo de Seguimiento donde se buscan las actividades
    """

    # Obtenemos la actividad y con esta las cadenas asociadas
    actividad = get_object_or_404(EfaActividad, idactividad=actividad_id)
    cadenas = SimuesCadenaCustodia.objects.filter(actividad = actividad).order_by('nro_orden')

    return render(request, 'cadenas/lista.html', {'cadenas':cadenas, 'actividad':actividad})


@login_required
def registro_cadena(request, actividad_id):
    """  Esta vista se utiliza para crear una nueva cadena de custodia
    """

    actividad = get_object_or_404(EfaActividad, idactividad=actividad_id)
    mostrar = False

    if request.method == 'POST':

         # Crear una instancia del formulario con el Post y la actividad para obtener
         # los laboratorios asociados
        form = RegistroCadenasForm(request.POST, actividad=actividad)

        if form.is_valid():

            # Obtenemos el tdr de la cadena y el número de cadenas relacionadas a ese tdr
            tdr = None
            num_cadenas = None
            if form.cleaned_data['tdr']:
                if Tterminoreferencia.objects.filter(txcodigo=form.cleaned_data['tdr']).exists():
                    tdr = Tterminoreferencia.objects.get(txcodigo=form.cleaned_data['tdr'])
                    num_cadenas = len(tdr.simuescadenacustodia_set.all()) + 1

            tipo_matriz = None
            if form.cleaned_data['tipo_matriz']:
                tipo_matriz = Tsubmatriz.objects.get(idsubmatriz=form.cleaned_data['tipo_matriz'].idsubmatriz)

            # Si se ha elegido un laboratorio en el combo de laboratorios y si existe ese laboratorio en la BD
            laboratorio = None
            if (form.cleaned_data['laboratorio'] and
                Tlaboratorio.objects.filter(idlaboratorio=form.cleaned_data['laboratorio'].idlaboratorio).exists()):
                laboratorio = Tlaboratorio.objects.get(idlaboratorio=form.cleaned_data['laboratorio'].idlaboratorio)

            # Creamos la cadena con los parámetros necesarios.
            # El número de orden es la cantidad de cadenas de custodia pertenecientes
            # a un tdr mas 1
            cadena = SimuesCadenaCustodia(tdr = tdr,
                                          actividad = actividad,
                                          tipo_matriz=tipo_matriz,
                                          nro_orden=num_cadenas,
                                          referencia = form.cleaned_data['referencia'],
                                          laboratorio = laboratorio,
                                          fecha_resultados_lab = form.cleaned_data['fecha_resultados_lab'])
            cadena.save()

            # Agregamos el numero correlativo
            cadena.correlativo = str(cadena.id)+"-"+str(date.today().year)+"-"+cadena.actividad.idsector.txsector

            cadena.created_by = request.user
            cadena.modified_by = request.user

            cadena.save()

            # Mensaje para saber que se guardo con éxito
            messages.success(request, 'La Cadena de Custodia se grabó satisfactoriamente')

            # Una vez guardado se pasa a editar
            return redirect('cadenas:editar', cadena_id=cadena.id)

    else:
        # Si recién se ingresa en la cadena
        form = RegistroCadenasForm(actividad=actividad)

    return render(request, 'cadenas/registro.html', {'form':form, 'mostrar':mostrar})


@login_required
def editar(request, cadena_id):
    """
    Pantalla donde se editan las cadenas de custodia
    """

    cadena = get_object_or_404(SimuesCadenaCustodia, id=cadena_id)
    mostrar = False

    puntos_muestreo = SimuesPuntoMuestreo.objects.filter(cadena=cadena)

    if len(puntos_muestreo) > 0:
        mostrar = True

    # Se crea una instancia del formulario y se guardan los nuevos valores
    if request.method == 'POST':
        form = RegistroCadenasForm(request.POST, actividad=cadena.actividad, cadena=cadena)

        if form.is_valid():

            # Obtenemos el tdr de la cadena y el número de cadenas relacionadas a ese tdr
            if cadena.tdr != form.cleaned_data['tdr']:
                if Tterminoreferencia.objects.filter(idtermref=form.cleaned_data['tdr'].idtermref).exists():
                    cadena.tdr = Tterminoreferencia.objects.get(idtermref=form.cleaned_data['tdr'].idtermref)
                    cadena.nro_orden = len(cadena.tdr.simuescadenacustodia_set.all()) + 1
                else:
                    cadena.tdr = None
                    cadena.nro_orden = None

            # Obtenemos el tipo de muestra
            if cadena.tipo_matriz != form.cleaned_data['tipo_matriz']:
                if Tsubmatriz.objects.filter(idsubmatriz=form.cleaned_data['tipo_matriz'].idsubmatriz).exists():
                    cadena.tipo_matriz = Tsubmatriz.objects.get(
                        idsubmatriz=form.cleaned_data['tipo_matriz'].idsubmatriz)

            cadena.referencia = form.cleaned_data['referencia']
            cadena.laboratorio = form.cleaned_data['laboratorio']
            cadena.fecha_resultados_lab = form.cleaned_data['fecha_resultados_lab']

            cadena.modified_by = request.user

            cadena.save()

            # Mensaje para saber que se guardo con éxito
            messages.success(request, 'La Cadena de Custodia se grabó satisfactoriamente')
    else:

        form = RegistroCadenasForm(actividad=cadena.actividad, cadena=cadena)

    return render(request, 'cadenas/registro.html', {'form':form, 'mostrar':mostrar,
                                                     'puntos_muestreo':puntos_muestreo, 'cadena':cadena})


@login_required
def registro_punto_muestreo(request, cadena_id):
    """
    Vista donde se guarda un nuevo punto de muestreo
    """

    cadena = get_object_or_404(SimuesCadenaCustodia, id=cadena_id)
    mostrar = False

    if request.method == 'POST':

        form_punto = RegistroPuntoMuestra(request.POST)

        if form_punto.is_valid():

            # Se crea y se guarda el punto de muestreo
            punto_muestreo = SimuesPuntoMuestreo(nombre=form_punto.cleaned_data['nombre'],
                                                 cadena=cadena,
                                                 zona=form_punto.cleaned_data['zona'],
                                                 datum=form_punto.cleaned_data['datum'],
                                                 gps=form_punto.cleaned_data['gps'],
                                                 tipomuestra=form_punto.cleaned_data['tipo_muestra'],
                                                 tipopunto=form_punto.cleaned_data['tipo_punto'],
                                                 observacion=form_punto.cleaned_data['observacion'],
                                                 fecha_hora=form_punto.cleaned_data['fecha_hora'],
                                                 altitud=form_punto.cleaned_data['altitud'],
                                                 coord_norte=form_punto.cleaned_data['coord_norte'],
                                                 coord_este=form_punto.cleaned_data['coord_este'])

            punto_muestreo.created_by = request.user
            punto_muestreo.modified_by = request.user

            punto_muestreo.save()

            # Mensaje para saber que se guardo con éxito
            messages.success(request, 'El punto de muestreo se grabó satisfactoriamente',
                             extra_tags='punto')

            mostrar = True

            return redirect('cadenas:editar_punto_muestreo', punto_id=punto_muestreo.id)

    else:

        form_punto = RegistroPuntoMuestra()

    return render(request, 'cadenas/registro_punto_muestreo.html', {'form_punto':form_punto,
                                                                    'mostrar':mostrar})


@login_required
def editar_punto_muestreo(request, punto_id):
    """
    Vista donde se edita el punto de muestreo
    """

    punto_muestreo = get_object_or_404(SimuesPuntoMuestreo, id=punto_id)
    envases = SimuesTipoEnvase.objects.all()
    detalle_envases = SimuesPuntoMuestreoEnvases.objects.filter(punto=punto_muestreo)

    # Se obtienen los detalles de los tdrs guardados y sus detalles
    detalles_tdrs = Tterminoreferenciadet.objects.filter(idtermref=punto_muestreo.cadena.tdr,
                                                    idsubmatriz=punto_muestreo.cadena.tipo_matriz)

    # Se obtienen los detalles de los parametros y Puntos de Referencia
    detalles_parametros = SimuesPuntoMuestreoTerminoReferenciaDet.objects.filter(punto=punto_muestreo)

    # Se vuelve True para que se muestren los formularios que no se ven en Registrar Punto de Muestreo
    mostrar = True

    form_punto = RegistroPuntoMuestra(punto_muestreo=punto_muestreo)
    form_subir_xml = SubirPuntoMuestraForm()

    # Se crea el formulario donde se ingresan el número de envases por tipo de envase
    form_envases = EnvasesForm(envases=envases, detalle_envases=detalle_envases)

    # Creacion del formset de Parámetros, la data inicial es una lista de diccionarios
    # donde cada diccionario es la data inicial de uno de los formularios del formset
    initial_formset = [{'detalle_tdr': detalle_tdr} for detalle_tdr in detalles_tdrs]

    # Si se ha guardado previamente los valores de los parametros
    # Se agrega al set inicial del formset parametros los valores guardados
    # para que se vean en el formulario

    if len(detalles_parametros) > 0:
        for detalle_dict in initial_formset:
            # Si un parámetro no ha sido guardado y por ende no existe el detalle se verifica para
            # no hacer get a un objeto inexistente.
            if detalles_parametros.filter(tdrdet = detalle_dict['detalle_tdr'].idtermrefdet).exists():
                detalle_dict['detalle_parametro'] = detalles_parametros.get(
                    tdrdet = detalle_dict['detalle_tdr'].idtermrefdet)


    ParametrosFormset = formset_factory(ParametrosForm, extra=0)

    # Si no existen parametros iniciales para el formset, se le da None como valor para que no se muestre
    # En la pantalla
    formset_parametros = None
    if initial_formset:
        formset_parametros = ParametrosFormset(initial=initial_formset)

    if request.method == 'POST':

        # Si se ha guardado el Punto de muestreo
        if "form_punto" in request.POST:

            form_punto = RegistroPuntoMuestra(request.POST, punto_muestreo=punto_muestreo)

            if form_punto.is_valid():

                # Se guarda el punto de muestreo
                punto_muestreo.nombre=form_punto.cleaned_data['nombre']
                punto_muestreo.zona=form_punto.cleaned_data['zona']
                punto_muestreo.datum=form_punto.cleaned_data['datum']
                punto_muestreo.gps=form_punto.cleaned_data['gps']
                punto_muestreo.tipopunto=form_punto.cleaned_data['tipo_punto']
                punto_muestreo.tipomuestra=form_punto.cleaned_data['tipo_muestra']
                punto_muestreo.observacion=form_punto.cleaned_data['observacion']
                punto_muestreo.fecha_hora=form_punto.cleaned_data['fecha_hora']
                punto_muestreo.altitud=form_punto.cleaned_data['altitud']
                punto_muestreo.coord_norte=form_punto.cleaned_data['coord_norte']
                punto_muestreo.coord_este=form_punto.cleaned_data['coord_este']

                punto_muestreo.modified_by = request.user
                punto_muestreo.save()

                # Mensaje para saber que se guardo con éxito
                messages.success(request, 'El punto de muestreo se grabó satisfactoriamente',
                                 extra_tags='punto')


        # Si se han guardado los envases
        elif "form_envases" in request.POST:

            form_envases = EnvasesForm(request.POST, envases=envases, detalle_envases=detalle_envases)

            if form_envases.is_valid():

                # Si no hay cantidad de envases guardados entonces se asume que se está creando
                if len(detalle_envases) == 0:

                   # Se crea y se guarda el formulario de envases
                    for (nombre, valor) in form_envases.cleaned_data.items():
                        detalle = SimuesPuntoMuestreoEnvases(punto=punto_muestreo,
                                                            envase=SimuesTipoEnvase.objects.get(id=nombre),
                                                            numero=valor)

                        detalle.created_by = request.user
                        detalle.modified_by = request.user
                        detalle.save()

                    # Mensaje para saber que se guardo con éxito
                    messages.success(request, 'La cantidad de envases se grabó satisfactoriamente',
                                     extra_tags='envases')

                else:

                    for (nombre, valor) in form_envases.cleaned_data.items():
                        # Comrpobamos si existe en la BD
                        if SimuesPuntoMuestreoEnvases.objects.filter(punto=punto_muestreo,
                                                             envase=SimuesTipoEnvase.objects.get(id=nombre)).exists():
                            detalle = SimuesPuntoMuestreoEnvases.objects.get(punto=punto_muestreo,
                                                                 envase=SimuesTipoEnvase.objects.get(id=nombre))

                            if detalle.numero != form_envases.cleaned_data[str(nombre)]:

                                detalle.numero = valor

                                detalle.modified_by = request.user
                                detalle.save()

                                # Mensaje para saber que se guardo con éxito
                    messages.success(request, 'La cantidad de envases se grabó satisfactoriamente',
                    extra_tags='envases')

        elif "form_parametros" in request.POST:

            formset_parametros = ParametrosFormset(request.POST, initial=initial_formset)

            if formset_parametros.is_valid():

                # Si no hay cantidad de parametros guardados entonces se asume que se está creando
                if len(detalles_parametros) == 0:

                    #Se crea y se guarda el formulario de parametros
                    for form_parametros in formset_parametros:
                        if form_parametros.is_valid():

                            detalle = SimuesPuntoMuestreoTerminoReferenciaDet(
                                punto=punto_muestreo,
                                tdrdet=Tterminoreferenciadet.objects.get(
                                idtermrefdet=form_parametros.cleaned_data['tdrdet_id']),
                                check = form_parametros.cleaned_data['check'],
                                valor = form_parametros.cleaned_data['valor'],
                                unidad_medida = form_parametros.cleaned_data['unidad_medida']
                            )

                            detalle.created_by = request.user
                            detalle.modified_by = request.user

                            detalle.save()

                    # Mensaje para saber que se guardo con éxito
                    messages.success(request, 'Los valores del parámetro se grabaron satisfactoriamente',
                                     extra_tags='parametros')

                else:

                    #Se guarda el formulario de parametros
                    for form_parametros in formset_parametros:
                        if form_parametros.is_valid():

                            if SimuesPuntoMuestreoTerminoReferenciaDet.objects.filter(
                                    punto=punto_muestreo,
                                    tdrdet=Tterminoreferenciadet.objects.get(
                                    idtermrefdet=form_parametros.cleaned_data['tdrdet_id'])
                            ).exists():
                                detalle = SimuesPuntoMuestreoTerminoReferenciaDet.objects.get(
                                    punto=punto_muestreo,
                                    tdrdet=Tterminoreferenciadet.objects.get(
                                    idtermrefdet=form_parametros.cleaned_data['tdrdet_id'])
                                )

                                # Comprobamos si alguna de los parametros del detalle se han cambiado
                                # de ser así
                                if (detalle.check != form_parametros.cleaned_data['check'] or
                                    detalle.valor != form_parametros.cleaned_data['valor'] or
                                    detalle.unidad_medida != form_parametros.cleaned_data['unidad_medida']):
                                        detalle.check = form_parametros.cleaned_data['check']
                                        detalle.valor = form_parametros.cleaned_data['valor']
                                        detalle.unidad_medida = form_parametros.cleaned_data['unidad_medida']

                                        detalle.modified_by = request.user
                                        detalle.save()

                                        # Mensaje para saber que se guardo con éxito
                                        messages.success(
                                            request,
                                            u'Los valores del parámetro '
                                            + detalle.tdrdet.idparametro.txparametro +
                                            u' se grabaron satisfactoriamente',
                                             extra_tags='parametros')

    return render(request, 'cadenas/registro_punto_muestreo.html', {'form_punto':form_punto,
                                                                    'form_subir_xml':form_subir_xml,
                                                                    'form_envases':form_envases,
                                                                    'formset_parametros':formset_parametros,
                                                                    'mostrar':mostrar,
                                                                    'punto':punto_muestreo
                                                                    })


def valor_field(field, namespace):
    """Función que devuelve el valor del campo"""

    if field is not None:
        value = field.find('{0}FormattedValue'.format(namespace))
        if value is not None:
            return value.text
        else:
            return None


def subir_xml_punto_muestreo(request, punto_id):
    """Vista encargada de subir el xml a punto de muestreo"""

    import xml.etree.ElementTree as ET

    # El namespace de los xmls de Crystal Report
    namespace = "{urn:crystal-reports:schemas:report-detail}"

    lista_secciones = []

    if request.method == 'POST':
        form = SubirPuntoMuestraForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['archivo']

            tree = ET.parse(f)
            # Obtenemos la raiz del XML
            root = tree.getroot()
            # Buscamos todas las secciones que es donde está la data en este documento
            sections = root.findall("{0}Group[@Level='1'][2]//{0}Section[@SectionNumber='0']".format(namespace))

            # Recorremos las secciones para obtener sus datos una por una
            for section in sections:

                if section is not None:
                    data_section = {}
                    # Buscamos el nombre del parámetro y el resultado en cada section
                    field_nombre = section.find("{0}Field[@Name='Parametro2']".format(namespace))
                    field_valor = section.find("{0}Field[@Name='Resultado2']".format(namespace))
                    field_unidad = section.find("{0}Field[@Name='Unidades2']".format(namespace))

                    # Obtenemos los valores correspondientes
                    valor_nombre = valor_field(field_nombre, namespace)
                    valor_resultado = valor_field(field_valor, namespace)
                    valor_unidad = valor_field(field_unidad, namespace)

                    # Guardamos los valores en un diccionario al cual agregamos a una lista de diccionarios
                    # donde están los resultados de todos los parámetros en el xml
                    if valor_nombre is not None:
                        data_section['nombre'] = valor_nombre
                    if valor_unidad is not None:
                        data_section['unidad'] = valor_unidad
                    if valor_resultado is not None:
                        if len(valor_resultado.split()) == 1:
                            data_section['valor'] = valor_resultado.replace(',','.')
                        else:
                            # En caso de que el el valor este compuesto por más de un caracter ("< 1,00"p.ej)

                            data_section['valor'] = \
                            valor_resultado.split()[len(valor_resultado.split())-1].replace(',','.')
                        lista_secciones.append(data_section)


            # GUARDAMOS LA DATA EN LA BD
            punto_muestreo = get_object_or_404(SimuesPuntoMuestreo, id=punto_id)
            detalles_tdrs = Tterminoreferenciadet.objects.filter(idtermref=punto_muestreo.cadena.tdr,
                                                                idsubmatriz=punto_muestreo.cadena.tipo_matriz)
            detalles_parametros = SimuesPuntoMuestreoTerminoReferenciaDet.objects.filter(punto=punto_muestreo)

            # Recorremos los datos de los parametros y del detalle del tdr para guardar la data en común.
            for seccion in lista_secciones:
                for detalle_tdr in detalles_tdrs:
                    if detalle_tdr.idparametro.txparametro == seccion['nombre']:
                        # Comprobamos si existen o no detalles previos con este parametro
                        if detalles_parametros.filter(tdrdet=detalle_tdr).count() == 0:
                            detalle = SimuesPuntoMuestreoTerminoReferenciaDet(
                                punto=punto_muestreo,
                                tdrdet=detalle_tdr,
                                check = True,
                                valor = seccion['valor'],
                                unidad_medida = SimuesUnidadMedida.objects.get(simbolo=seccion['unidad'])
                            )

                            detalle.created_by = request.user
                            detalle.modified_by = request.user

                            detalle.save()

                        else:
                            detalle = detalles_parametros.get(tdrdet=detalle_tdr)
                            detalle.check = True
                            detalle.valor = seccion['valor']
                            detalle.unidad_medida = SimuesUnidadMedida.objects.get(simbolo=seccion['unidad'])

                            detalle.modified_by = request.user

                            detalle.save()

            # Mensaje para saber que se guardo con éxito
            messages.success(request, 'El archivo se subio satisfactoriamente', extra_tags='subido')


    return redirect('cadenas:editar_punto_muestreo', punto_id=punto_id)

