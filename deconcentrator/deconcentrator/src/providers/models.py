from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField


def _method_populate(m):
    return "%s.%s" % (m.package, m.method,)


class Method(models.Model):
    """ a method to let some provider do the hard NLU stuff. this is usually
    done via a specific http interface.
    """
    package = models.CharField(max_length=200)
    method = models.CharField(max_length=20)
    ident = AutoSlugField(
        primary_key=True,
        unique=True,
        populate_from=_method_populate,
        sep='.'
    )

    class Meta:
        unique_together = [('package', 'method',)]

    def __str__(self):
        return '.'.join([self.package, self.method])


class Provider(models.Model):
    """ a single NLU provider. in other words: an instance of this class represents
    a way of interpreting natural language.
    """
    name = models.CharField(max_length=30)
    ident = AutoSlugField(primary_key=True, populate_from='name')
    method = models.ForeignKey('Method', on_delete=models.CASCADE, help_text=_("the function to use for this provider."))
    args = JSONField(help_text=_("a list of arguments to pass to the method."), blank=True)
    kwargs = JSONField(help_text=_("a dict of keyword arguments to pass to the method."), blank=True)

    def __str__(self):
        return self.name
