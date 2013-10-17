from django.db import models


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
    return user and user.is_authenticated() or False

class Instrument(models.Model):
    objects = InstrumentManager()
    name = models.CharField(max_length=64, unique=True)

    class Yaaac:
        user_passes_test = can_search_instrument
        allows_suggest_by = ['__unicode__']

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class MusicGenre(models.Model):
    objects = MusicGenreManager()
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class Band(models.Model):
    objects = BandManager()
    name = models.CharField(max_length=100, unique=True)
    genre = models.ForeignKey("MusicGenre", null=True, blank=True)

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    def get_full_info(self):
        return u"%s (%s)" % (self.name, self.genre)


class BandMember(models.Model):
    objects = BandMemberManager()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    band = models.ForeignKey("Band", limit_choices_to={"genre__name__in": ["Rock", "Blues/Rock"]},
                             null=True, blank=True)
    favorite_instrument = models.ForeignKey("Instrument", null=True, blank=True)

    class Meta:
        unique_together = (('first_name', 'last_name'),)

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def natural_key(self):
        return (self.first_name, self.last_name)

    def get_full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)
