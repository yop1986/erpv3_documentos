# ERPv3 - Documentos

## Desarrollo

### Configuración del Ambiente

Esta aplicacion depende del [Modulo de usuarios](https://github.com/yop1986/erpv3_usuarios) 
por lo que es necesario instalar este y sus dependencias previamente.

Desde la consola de Git se procede a clonar este repositorio, en la raiz del 
proyecto.

    $ git clone https://github.com/yop1986/erpv3_documentos.git documentos

#### Settings

Es necesario modificar el archivo **settings.py** del proyecto general con la
siguiente informacion:

    INSTALLED_APPS = [
        ...
        'documentos',
    ]

    INFORMACION_APLICACIONES = {
        'documentos': {
            'nombre':       'Documentos',
            'descripcion':  _('Control de documentos para una bodega o sede administrativa.'),
            'url':          reverse_lazy('documentos:index'),
            'imagen':       'docs_documentos.png',
        },
    }

#### Urls

Posterior a esta configuracion es necesario agregar las urls al proyecto base __< Base >/urls.py__

    path('documentos', include('documentos.urls')),

#### Comandos adicionales de Django

    (venv) ERPv3> python manage.py check
    (venv) ERPv3> python manage.py makemigrations documentos
    (venv) ERPv3> python manage.py migrate documentos
