import time, datetime
from django.contrib.auth.models import User
from django.db import models

from .managers import PluginVersionManager

class Plugin(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    
    author = models.ForeignKey(User)
    name = models.CharField(max_length=127, unique=True)
    description = models.TextField(blank=True, default='')
    url = models.URLField(blank=True, default='')

    def __unicode__(self):
        return self.name


class PluginVersion(models.Model):
    plugin = models.ForeignKey(Plugin, related_name='versions')
    creation_date = models.DateTimeField(auto_now_add=True)

    is_valid = models.BooleanField(default=False)

    major = models.IntegerField(null=True, blank=True)
    minor = models.IntegerField(null=True, blank=True)
    maintenance = models.IntegerField(null=True, blank=True)
    build = models.IntegerField(null=True, blank=True)
    generic = models.CharField(max_length=128, null=True, blank=True)

    name = models.CharField(max_length=128, help_text='The name field extracted from the binary.', null=True, blank=True)
    author = models.CharField(max_length=128, help_text='The author field extracted from the binary.', null=True, blank=True)
    version = models.CharField(max_length=128, help_text='The version field extracted from the binary.', null=True, blank=True)
    description = models.TextField(help_text='The description field extracted from the binary.', null=True, blank=True)
    url = models.CharField(max_length=256, help_text='The URL field extracted from the binary.', null=True, blank=True)

    @staticmethod
    def get_source_archive_path(instance, filename):
        self = instance
        return '../plugins/source/%s/%s_%s.tar.gz' % (time.strftime('%Y/%m/%d'), self.name, datetime.datetime.now().microsecond)

    @staticmethod
    def get_built_archive_path(instance, filename):
        self = instance
        return '../static/plugins/%s/%s.tar.gz' % (time.strftime('%Y/%m/%d'), self.name)

    source_archive = models.FileField(upload_to=get_source_archive_path)
    built_archive = models.FileField(upload_to=get_built_archive_path, null=True)

    objects = PluginVersionManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return self.plugin.name + ' ' + self.version_string

    @property
    def version_number(self):
        return '.'.join(map(str, filter(lambda x: x is not None, (self.major, self.minor, self.maintenance, self.build))))

    @property
    def version_string(self):
        return self.version_number + (('-' + self.generic) if self.generic else '')


