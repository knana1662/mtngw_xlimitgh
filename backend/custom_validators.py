from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from heapq import merge
from tarfile import TarFile
from zipfile import ZipFile

LIST_OF_MTN_MOBILE_NETWORKS = ["024","025","053","054","055","059"]


def validate_phone_number(value):
    if len(value) != 10:
        raise ValidationError(
            _('%(value)s is not 10 digits'),
            params={'value': value},
        )   

    else:

        if value[:3] not in  LIST_OF_MTN_MOBILE_NETWORKS:
            ...
            raise ValidationError(
                _('%(value)s is not a valid MTN phone number'),
                params={'value': value},
            )


