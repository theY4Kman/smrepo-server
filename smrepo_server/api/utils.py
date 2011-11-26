from django.core.serializers.json import simplejson as json
import re
from django.http import Http404, HttpResponse

# Matches a standard plug-in name
_RGX_PLUGIN_NAME = r'(?P<plugin_name>[a-zA-Z0-9_-]+)'
RGX_PLUGIN_NAME = re.compile(_RGX_PLUGIN_NAME, re.I)
# Matches a standard version string
_RGX_BASE_VERSION = r'(?P<version_string>\d(.\d){0,3}(-[a-zA-Z0-9_-]*)?)'
RGX_BASE_VERSION = re.compile(_RGX_BASE_VERSION, re.I)
# Matches a standard version string as well as its version_number and version_generic parts
_RGX_VERSION_STRING = r'(?P<version_string>(?P<version_number>\d(.\d){0,3})(-(?P<version_generic>[a-zA-Z0-9_-]*))?)'
RGX_VERSION_STRING = re.compile(_RGX_VERSION_STRING, re.I)
# Matches a floating point number, the representation of a datetime timestamp, in seconds
_RGX_DATE = r'(?P<date>\d+.\d{0,5})'
RGX_DATE = re.compile(_RGX_DATE)

def get_object_or_404_message(klass, message, **kwargs):
    try:
        return klass.objects.get(**kwargs)
    except klass.DoesNotExist:
        raise Http404(message)

def json_response(object, *args, **kwargs):
    kwargs['mimetype'] = 'text/json'
    response = HttpResponse(json.dumps(object), *args, **kwargs)
    response['Content-Disposition'] = 'inline'
    return response
