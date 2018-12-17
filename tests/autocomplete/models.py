from django import VERSION as DJ_VERSION
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class InstrumentManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class MusicGenreManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class BandManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class BandMemberManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)


def can_search_instrument(instance, user):
    if DJ_VERSION < (1, 10):
        return user and user.is_authenticated() or False
    else:
        return user and user.is_authenticated or False


@python_2_unicode_compatible
class Instrument(models.Model):
    objects = InstrumentManager()
    name = models.CharField(max_length=64, unique=True)

    class Yaaac:
        user_passes_test = can_search_instrument
        allows_suggest_by = ['__str__', '__unicode__']

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    def get_absolute_url(self):
        return "http://en.wikipedia.org/wiki/%s" % self.name


@python_2_unicode_compatible
class MusicGenre(models.Model):
    objects = MusicGenreManager()
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


@python_2_unicode_compatible
class Band(models.Model):
    objects = BandManager()
    name = models.CharField(max_length=100, unique=True)
    genre = models.ForeignKey("MusicGenre", models.SET_NULL, null=True, blank=True)

    class Yaaac:
        user_passes_test = lambda instance, u: True
        allows_suggest_by = ['name', 'get_full_info']

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    def get_full_info(self):
        return u"%s (%s)" % (self.name, self.genre)


@python_2_unicode_compatible
class BandMember(models.Model):
    objects = BandMemberManager()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    band = models.ForeignKey("Band", models.SET_NULL,
                             limit_choices_to={"genre__name__in": ["Rock", "Blues/Rock"]},
                             null=True, blank=True)
    favorite_instrument = models.ForeignKey("Instrument", models.SET_NULL,
                                            null=True, blank=True)

    class Meta:
        unique_together = (('first_name', 'last_name'),)

    class Yaaac:
        user_passes_test = lambda instance, u: True
        allows_suggest_by = ['get_full_name']

    def __str__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def natural_key(self):
        return (self.first_name, self.last_name)

    def get_full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)
