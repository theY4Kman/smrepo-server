from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Plugin
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
        plugin_ref = Plugin.objects.get(pk=1)
        plver_ref = plugin_ref.versions.all()[0]

        response = self.client.get(reverse('download-plugin', kwargs={ 'plugin_name': plugin_ref.name }))
        self.assertEqual(response.status_code, 200, 'Plug-in could not be found')
        self.assertEqual(response['Content-Type'], 'application/x-tar-gz')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=%s_%s.tar.gz;' % (plugin_ref.name,
                                                                                                  plver_ref.version_string))

    def test_plugin_version_download(self):
        plugin_ref = Plugin.objects.get(pk=1)
        plver_ref = plugin_ref.versions.all()[0]

        url_args = {
            'plugin_name': plugin_ref.name,
            'version_string': plver_ref.version_string
        }

        response = self.client.get(reverse('download-plugin-version', kwargs=url_args))
        self.assertEqual(response.status_code, 200, 'Plug-in could not be found')
        self.assertEqual(response['Content-Type'], 'application/x-tar-gz')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=%s_%s.tar.gz;' % (plugin_ref.name,
                                                                                                  plver_ref.version_string))
