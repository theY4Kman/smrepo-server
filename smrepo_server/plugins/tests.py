from django.test import TestCase
import os.path
import validate

def rel_to_abs(path):
    return os.path.join(os.path.dirname(__file__), path)

class ArchiveValidationTests(TestCase):
    VALID_SOURCE_PATH = rel_to_abs('../api/fixtures/static/valid_source.tar.gz')
    INVALID_TYPE_PATH = rel_to_abs('../api/fixtures/static/invalid_type.tar.gz')
    BLACKLISTED_PATH = rel_to_abs('../api/fixtures/static/blacklisted_source.tar.gz')
    PLUGIN_PREPENDED_PATH = rel_to_abs('../api/fixtures/static/prepend_plugin.tar.gz')

    def test_valid_source_with_correct_plugin_name_validates(self):
        """Valid source archive successfully passes validation"""
        self.assertTrue(validate.validate_archive(self.VALID_SOURCE_PATH, 'test'))

    def test_valid_source_with_correct_plugin_name_does_not_validate(self):
        """Valid source archive unsuccessfully passes validation when wrong plug-in name passed in"""
        self.assertEqual(validate.validate_archive(self.VALID_SOURCE_PATH, 'not_test'),
            [('./addons/sourcemod/scripting/test.sp', 'Invalid path')])

    def test_invalid_filetype_does_not_validate(self):
        """A file with the wrong filetype should not validate"""
        self.assertEqual(validate.validate_archive(self.INVALID_TYPE_PATH, 'who_cares'),
            [('./addons/sourcemod/scripting/not_the_right_file_type.blank', 'Invalid path')])

    def test_blacklisted_file_does_not_validate(self):
        """A blacklisted should not validate"""
        self.assertEqual(validate.validate_archive(self.BLACKLISTED_PATH, 'basecomm'),
            [('./addons/sourcemod/scripting/basecomm.sp', 'Blacklisted path')])

    def test_prepend_plugin_validates_blacklisted_filename(self):
        """A blacklisted should not validate"""
        self.assertEqual(validate.validate_archive(self.PLUGIN_PREPENDED_PATH, 'basecomm'), True)

