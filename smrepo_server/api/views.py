from django.http import HttpResponse, Http404

from .decorators import version_string, requires_plugin
from .models import PluginVersion
from .utils import json_response

@requires_plugin
@version_string
def download_plugin(request, plugin_ref, version=None):
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

@requires_plugin
def plugin_version(request, plugin_ref):
    versions = plugin_ref.versions.order_by('-major', '-minor', '-maintenance', '-build')
    if not versions:
        return json_response({ 'error': 'Plug-in has no versions' }, status=404)

    plver_ref = versions[0]
    obj = {
        'version': plver_ref.version_string,
        'plugin_author': plugin_ref.author.username,
        'author': plver_ref.author,
        'plugin_description': plugin_ref.description,
        'description': plver_ref.description,
        'plugin_url': plugin_ref.url,
        'url': plver_ref.url,
        'plugin_name': plugin_ref.name,
        'name': plver_ref.name
    }

    return json_response(obj)

