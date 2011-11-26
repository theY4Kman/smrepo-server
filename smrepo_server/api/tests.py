import json
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Plugin, PluginVersion
from .utils import RGX_VERSION_STRING, RGX_BASE_VERSION

class UtilsRegexTest(TestCase):
    def test_version_string(self):
        version_number = '1.2.3.4'
        version_generic = 'test'
        version_string = version_number + '-' + version_generic

        match = RGX_VERSION_STRING.match(version_string)
        self.assert_(match, 'Could not match valid version string')
        self.assertEqual(match.group('version_string'), version_string)
        self.assertEqual(match.group('version_generic'), version_generic)
        self.assertEqual(match.group('version_number'), version_number)

        match = RGX_BASE_VERSION.match(version_string)
        self.assert_(match, 'Base regex could not match valid version string')

        version_number = '1.2.3.4'
        version_generic = None
        version_string = version_number

        match = RGX_VERSION_STRING.match(version_string)
        self.assert_(match, 'Could not match valid version string')
        self.assertEqual(match.group('version_string'), version_string)
        self.assertEqual(match.group('version_generic'), version_generic)
        self.assertEqual(match.group('version_number'), version_number)

        match = RGX_BASE_VERSION.match(version_string)
        self.assert_(match, 'Base regex could not match valid version string')


class DownloadPluginTest(TestCase):
    fixtures = ['api_data']

    def test_plugin_download(self):
        """Plug-in download without version downloads latest plug-in version"""
        plugin_ref = Plugin.objects.get(pk=1)
        plver_ref = plugin_ref.versions.order_by('-major', '-minor', '-maintenance', '-build')[0]

        response = self.client.get(reverse('download-plugin', kwargs={ 'plugin_name': plugin_ref.name }))
        self.assertEqual(response.status_code, 200, 'Plug-in could not be found')
        self.assertEqual(response['Content-Type'], 'application/x-tar-gz')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=%s_%s.tar.gz;' % (plugin_ref.name,
                                                                                                  plver_ref.version_string))

    def test_plugin_version_download(self):
        """Plug-in download with specific version downloads correct version"""
        plugin_ref = Plugin.objects.get(pk=1)
        plver_ref = plugin_ref.versions.order_by('-major', '-minor', '-maintenance', '-build')[0]

        url_args = {
            'plugin_name': plugin_ref.name,
            'version_string': plver_ref.version_string
        }

        response = self.client.get(reverse('download-plugin-version', kwargs=url_args))
        self.assertEqual(response.status_code, 200, 'Plug-in could not be found')
        self.assertEqual(response['Content-Type'], 'application/x-tar-gz')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=%s_%s.tar.gz;' % (plugin_ref.name,
                                                                                                  plver_ref.version_string))


class PluginVersionsTest(TestCase):
    fixtures = ['api_data']

    def test_plugin_version(self):
        """Latest version listed for plug-in"""
        plugin_ref = Plugin.objects.get(pk=1)
        plver_ref = plugin_ref.versions.order_by('-major', '-minor', '-maintenance', '-build')[0]

        response = self.client.get(reverse('plugin-version', kwargs={ 'plugin_name': plugin_ref.name }))
        obj = json.loads(response.content)
        expected = {
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

        self.assertEqual(response.status_code, 200, 'Could not retrieve plug-in version')
        self.assertEqual(obj, expected, 'Response differs from what was expected')

    def test_plugin_versions(self):
        """All versions of a plug-in are listed"""
        plugin_ref = Plugin.objects.get(pk=1)

        def ret(plver_ref):
            return {
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
        expected = map(ret, plugin_ref.versions.order_by('-major', '-minor', '-maintenance', '-build'))

        response = self.client.get(reverse('plugin-versions', kwargs={ 'plugin_name': plugin_ref.name }))
        obj = json.loads(response.content)

        self.assertEqual(response.status_code, 200, 'Could not find plug-in')
        self.assertEqual(obj, expected, 'Response differs from what was expected')

