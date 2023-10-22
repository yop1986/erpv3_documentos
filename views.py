from django.views.generic.base import TemplateView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from usuarios.personal_views import (PersonalCreateView, PersonalUpdateView,
    PersonalListView, PersonalDetailView, PersonalDeleteView, PersonalFormView,
    Configuraciones)

from .models import Bodega
# forms

gConfiguracion = Configuraciones()
DISPLAYS = {
    'forms': {
        'submit': _('Guardar'),
        'cancel': _('Cancelar'),
    },
    'delete_form': {
        'confirmacion': _('¿Esta seguro de eliminar el elemento indicado?'),
        'submit': _('Eliminar'),
        'cancel': _('Cancelar'),
    },
    'disable_form': {
        'confirmacion': _('¿Esta seguro de inhabilitar el elemento indicado?'),
        'submit': _('Inhabilitar'),
        'cancel': _('Cancelar'),
    },
    'opciones': {
        'detail': _('Ver'),
        'update': _('Editar'),
        'delete': _('Eliminar'),
    },
    'tabla_vacia': _('No hay elementos para mostrar'),
}

class IndexTemplateView(TemplateView):
    template_name = 'documentos/index.html'

    extra_context ={
        'title': _('Documentos'),
        'general': {
            'nombre_sitio': gConfiguracion.get_value('sitio', 'nombre'),
        },
        'elementos': [
            {
                'display':  _('Bodegas'),
                'desc':     _('Manejo de bodegas en las cuales se encuentran \
                    distribuidos los documentos.'),
                'imagen':   _('docs_bodega.png'),
            },
            {
                'display':  _('Ubicación'),
                'desc':     _('Permite la generación dinámica de ubicación (estantes, \
                    niveles, posiciones y cajas) para determinar la ubicación precisa\
                    en tiempo real.'),
                'imagen':   _('docs_ubicacion.png'),
            },
            {
                'display':  _('Encargados'),
                'desc':     _('Personal encargado de la bodega con permisos administrativos.'),
                'imagen':   _('docs_encargado.png'),
            },
            {
                'display':  _('Personal'),
                'desc':     _('Personal capaz de consultar información y/o realizar \
                    tareas en determinada bodega.'),
                'imagen':   _('docs_personal.png'),
            },
            {
                'display':  _('Correo'),
                'desc':     _('Envío de correo para seguimiento de las actividades o \
                    procesos que afecten los documentos.'),
                'imagen':   _('docs_correo.png'),
            },            
            {                
                'display':  _('Etiquetas'),
                'desc':     _('Impresión de etitquetas con código de barras para facilitar\
                    busqueda, ingreso y egreso a la bodega.'),
                'imagen':   _('docs_etiquetas.png'),
            },
        ],
    }


class BodegaListView(PersonalListView):
    permission_required = 'documentos.view_bodega'
    template_name = 'documentos/list.html'
    model = Bodega
    ordering = ['-vigente', 'codigo']
    paginate_by = 10
    extra_context = {
        'title': _('Bodegas'),
        'campos': {
            #-1: no enumera
            # 0: inicia numeración en 0
            # 1: inicia numeración en 1
            'enumerar': 1,
            # Si hay valor se muestra opciones por linea, de lo contrario no se muestran
            'opciones': _('Opciones'),
            # Lista de campos que se deben mostrar en la tabla
            'lista': [
                'codigo',
                'nombre', 
            ],
        },
        'campos_extra': [
            {
                'nombre':   _('Estado'), #display
                # valor, constante o funcion 
                'funcion': 'get_estado',  
            },
        ],
        'opciones': DISPLAYS['opciones'],
        'create' :{
            'display':  _('Nueva'),
            'url':      Bodega.url_create(),
        },
        'mensaje': {
            'vacio': DISPLAYS['tabla_vacia'],
        },
    }

class BodegaCreateView(PersonalCreateView):
    permission_required = 'documentos.add_bodega'
    template_name = 'documentos/forms.html'
    model = Bodega
    fields = '__all__'
    #form_class = 
    success_url = reverse_lazy('documentos:list_bodega')
    extra_context = {
        'title': _('Nueva bodega'),
        'opciones': DISPLAYS['forms'],
    }

class BodegaDetailView(PersonalDetailView):
    permission_required = 'documentos.view_bodega'
    template_name = 'documentos/detail.html'
    model = Bodega
    extra_context = {
        'title': _('Bodega'),
        'campos': {
            'opciones': _('Opciones'),
            'lista': [
                #'id',
                'codigo', 
                'nombre',
                'direccion',
                'correo_egreso',
                'correo_traslado',
                'encargado',
            ],
        },
        'opciones': DISPLAYS['opciones'],
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['campos_adicionales'] = [
            #{'display': , <'ul_lista', 'valor'>:}, 
            {'display': _('Personal'), 'ul_lista': self.object.get_personal()},
            {'display': _('Estado'), 'valor': self.object.get_estado()},
        ]
        return context

class BodegaUpdateView(PersonalUpdateView):
    permission_required = 'documentos.change_bodega'
    template_name = 'documentos/forms.html'
    model = Bodega
    fields = '__all__'
    extra_context = {
        'title': _('Modificar bodega'),
        'opciones': DISPLAYS['forms'],
    }

    def get_success_url(self):
        return self.object.url_detail()

class BodegaDeleteView(PersonalDeleteView):
    permission_required = 'documentos.delete_bodega'
    template_name = 'documentos/delete_confirmation.html'
    model = Bodega
    success_url = reverse_lazy('documentos:list_bodega')
    extra_context = {
        'title': _('Inhabilitar bodega'),
        'opciones': DISPLAYS['disable_form'],
    }