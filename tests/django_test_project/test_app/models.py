from django.db import models


class BandManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class BandMemberManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)


class Band(models.Model):
    objects = BandManager()

    name = models.CharField(max_length=100, unique=True )

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class BandMember(models.Model):
    objects = BandMemberManager()

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    band = models.ForeignKey("Band")

    class Meta:
        unique_together = (('first_name', 'last_name'),)

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def natural_key(self):
        return (self.first_name, self.last_name)
