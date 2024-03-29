from django.utils.functional import wraps
from .models import Plugin
from .utils import RGX_VERSION_STRING, json_response

def requires_plugin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        plugin_name = kwargs.pop('plugin_name')
        try:
            kwargs['plugin_ref'] = Plugin.objects.get(name__iexact=plugin_name)
        except Plugin.DoesNotExist:
            return json_response({ 'error': 'Plug-in not found' }, status=404)
        return fn(*args, **kwargs)
    return wrapper

def version_string(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        version_string = kwargs.pop('version_string') if 'version_string' in kwargs else None

        if version_string is not None:
            match = RGX_VERSION_STRING.match(version_string)

            version_number = map(int, match.group('version_number').split('.'))
            version = {}
            for key in ('major', 'minor', 'maintenance', 'build'):
                version[key] = version_number.pop(0) if version_string else 0
            kwargs['version'] = (version, match.group('version_generic'))
        else:
            kwargs['version'] = None

        return fn(*args, **kwargs)
    return wrapper