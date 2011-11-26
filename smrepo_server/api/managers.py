from django.db import models

class PluginVersionManager(models.Manager):
    def get_query_set(self):
        return super(PluginVersionManager, self).get_query_set().filter(is_valid=True).exclude(major__isnull=True)