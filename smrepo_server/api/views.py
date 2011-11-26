from django.http import HttpResponse, Http404

from .decorators import version_string
from .models import Plugin, PluginVersion
from .utils import json_response

@version_string
def download_plugin(request, plugin_name, version=None):
    try:
        plugin_ref = Plugin.objects.get(name__iexact=plugin_name)
    except Plugin.DoesNotExist:
        return json_response({ 'error': 'Plug-in not found' }, status=404)

    if version is None:
        versions = plugin_ref.versions.filter(is_valid=True, built_archive__isnull=False).order_by('-major', '-minor', '-maintenance', '-build')
        if not versions:
            return json_response({ 'error': 'No suitable plug-in version found' }, status=404)
        plver_ref = versions[0]
    else:
        try:
            plver_ref = PluginVersion.objects.get(plugin=plugin_ref, **version[0])
        except PluginVersion.DoesNotExist:
            return json_response({ 'error': 'Plug-in version not found' }, status=404)

    plver_ref.built_archive.open()
    response = HttpResponse(plver_ref.built_archive.read(), mimetype='application/x-tar-gz')
    response['Content-Disposition'] = 'attachment; filename=%s_%s.tar.gz;' % (plugin_ref.name, plver_ref.version_string)
    plver_ref.built_archive.close()

    return response

        