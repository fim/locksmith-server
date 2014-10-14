from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lock(models.Model):
    stub = models.TextField(editable=False)
    description = models.TextField(default=None, null=True, blank=True)
    expire = models.DateTimeField(default=None, null=True)
    locked = models.BooleanField(default=False)
    multilock = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name="owner", null=True,
        editable=False, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}'.format(self.stub)

    def lock(self, user=None):
        if self.locked:
            if self.owner == user and self.multilock == True:
                return
            else:
                raise Exception("Lock already locked")

        self.locked = True
        if user: self.owner = user
        self.save()

    def unlock(self, user=None):
        if self.owner and user != self.owner:
            raise Exception("Not allowed to unlock resource")
        self.locked = False
        self.owner = None
        self.save()# Create your models here.
