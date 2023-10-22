import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from simple_history.models import HistoricalRecords


class Bodega(models.Model):
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo  = models.CharField(_('Código'), max_length=3, unique=True, 
        help_text=_('Código de 3 caracteres'))
    nombre  = models.CharField(_('Nombre'), max_length=120, unique=True)
    direccion = models.CharField(_('Dirección'), max_length=210)
    vigente = models.BooleanField(_('Estado'), default=True) # para eliminación lógica
    correo_egreso = models.BooleanField(_('Correo por egreso'), default=True)
    correo_traslado = models.BooleanField(_('Correo por traslado'), default=True)

    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
        help_text=_('Usuarios en grupos que inicien con "Expedientes"'), 
        verbose_name=_('Encargado'))
    personal = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bodega_personal', 
        help_text=_('Usuarios en grupos que inicien con "Expedientes"'), 
        verbose_name=_('Personal'))

    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    
    class Meta:
        permissions = [
            ("genera_estructura", "Permite generar estructura de la bodega"),
            ("view_estructura", "Permite visualizar la estructura de la bodega"),
        ]

    def __str__(self):
        return self.nombre

    def get_estado(self):
        return _('Habilitada') if self.vigente else 'Inhabilitada'

    def get_personal(self, formato='text'):
        return self.personal.all()
        
    def url_create():
        return reverse_lazy('documentos:create_bodega')

    def url_detail(self):
        return reverse_lazy('documentos:detail_bodega', kwargs={'pk': self.id})

    def url_update(self):
        return reverse_lazy('documentos:update_bodega', kwargs={'pk': self.id})

    def url_delete(self):
#        if Estructura.objects.filter(tipo = self.id).count()>0:
#            return None
        return reverse_lazy('documentos:delete_bodega', kwargs={'pk': self.id})

    def validate_fields(self, exclude=None):
        qs = Bodega.objects.filter(models.Q(codigo=self.codigo) | models.Q(nombre=self.nombre)).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(_('Código o nombre repetido.'))

    def save(self, *args, **kwargs):
        self.codigo = self.codigo.upper()
        self.nombre = self.nombre.upper()

        self.validate_fields()
        super().save(*args, **kwargs)

    def delete(self):
        self.vigente = not self.vigente
        self.save()

    def hard_delete(self):
        super().delete()
