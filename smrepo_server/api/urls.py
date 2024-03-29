from django.conf.urls.defaults import patterns, include, url
from .utils import _RGX_PLUGIN_NAME, _RGX_BASE_VERSION


urlpatterns = patterns('smrepo_server.api.views',
    url(r'^plugin/%s/$' % _RGX_PLUGIN_NAME, 'download_plugin', name='download-plugin'),
    url(r'^plugin/%s/%s/$' % (_RGX_PLUGIN_NAME, _RGX_BASE_VERSION), 'download_plugin', name='download-plugin-version'),
    url(r'^plugin/%s/version/$' % _RGX_PLUGIN_NAME, 'plugin_version', name='plugin-version'),
    url(r'^plugin/%s/versions/$' % _RGX_PLUGIN_NAME, 'plugin_versions', name='plugin-versions'),
)
