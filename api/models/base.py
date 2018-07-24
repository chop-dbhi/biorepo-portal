import random
import string

from django.db import models
from django.utils import timezone
from django.conf import settings


class AutoDateTimeField(models.DateTimeField):
    """A last-modified-style date field."""

    # TODO: Why doesn't `auto_now` work here?

    def pre_save(self, model_instance, add):
        return timezone.now()


class CreatedModified(models.Model):
    """A model with created and modified timestamps."""

    date_help_text = "Please use date format: <em>YYYY-MM-DD</em>"

    created = models.DateTimeField(
        default=timezone.now,
        verbose_name='Record Creation DateTime',
        help_text=date_help_text)

    modified = AutoDateTimeField(
        default=timezone.now,
        verbose_name='Record Last Modified DateTime',
        help_text=date_help_text)

    class Meta(object):
        abstract = True


class Base(CreatedModified):
    """A model that provides access to settings props."""

    def _settings_prop(self, GROUP, KEY, default=None):
        PROTOCOL_PROPS = settings.PROTOCOL_PROPS
        if PROTOCOL_PROPS:
            GROUP_SETTINGS = PROTOCOL_PROPS.get(GROUP)
            if GROUP_SETTINGS:
                return GROUP_SETTINGS.get(KEY, default)
            else:
                return default
        else:
            return default

    # TODO: Is this necessary?
    def save(self, *args, **kwargs):
        # Create an immutable key for this protocol
        super(Base, self).save(*args, **kwargs)

    class Meta:
        app_label = 'api'
        abstract = True


class ImmutableKey(Base):
    """A model with a unique immutable key."""

    key = models.CharField(max_length=255, unique=True,
                           verbose_name='Immutable Key', editable=False,
                           blank=True)

    def _make_random_key(
            self, seed, ja, l, chars=string.ascii_uppercase + string.digits):
        # TODO: What is the `ja` argument for?
        random.seed(random.randrange(0, seed))
        return ''.join(random.choice(chars) for idx in range(l))

    def _set_key(self):
        # Generate new key, override key that was used to create this object
        if not self.pk:
            key_length = self._key_length()
            seed = self._key_seed()
            jump = ImmutableKey.objects.count()
            #
            uk = ''
            idx = 0
            max_idx = 1e6
            while idx < max_idx:
                uk = self._make_random_key(seed=seed, ja=jump + idx,
                                           l=key_length)
                immutables_using_uk = ImmutableKey.objects.filter(key=uk)
                if immutables_using_uk.count() == 0:
                    idx = max_idx
                else:
                    idx += 1
            self.key = uk

    def _key_seed(self, default=123456789):
        return self._settings_prop('IMMUTABLE_KEYS', 'seed', default)

    def _key_length(self, default=15):
        return self._settings_prop('IMMUTABLE_KEYS', 'length', default)

    def save(self, *args, **kwargs):
        self._set_key()
        super(ImmutableKey, self).save()


class BaseWithImmutableKey(Base):
    """A timestamped model with settings access and an immutable key.

    The immutable_key will serve as a unique identifier for the Organization
    which never changes
    """

    # TODO: Why is this a relation?
    immutable_key = models.OneToOneField(
        ImmutableKey, editable=False, blank=True, unique=True, null=True)

    def _create_immutable_key(self):
        """Generate an immutable_key for this entity."""

        if self.immutable_key:
            # If the key already exists then this model is being edited but
            # this key should not change
            return
        else:
            ik = ImmutableKey()
            ik.save()
            self.immutable_key = ik

    def save(self, *args, **kwargs):
        self._create_immutable_key()
        super(BaseWithImmutableKey, self).save(*args, **kwargs)

    class Meta:
        app_label = 'api'
        abstract = True
