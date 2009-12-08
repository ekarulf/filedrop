from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from filedrop.checksum import checksum
from datetime import date
from tempfile import mkdtemp
import string
import random
import os
import mimetypes

class ChecksumFormats(object):
    CHOICES = (
        ('adler32', 'Adler-32'),
        ('crc32', 'CRC-32'),
        ('md5', 'MD5'),
        ('sha1', 'SHA-1'),
        ('sha224', 'SHA-224'),
        ('sha256', 'SHA-256'),
        ('sha384', 'SHA-384'),
        ('sha512', 'SHA-512'),
    )

def _upload_directory():
    return os.path.join(settings.FILEDROP_ROOT, date.today().strftime('uploads/%Y/%m/%d/'))

def _file_directory(instance, filename, directory=None):
    if not hasattr(instance, 'directory') or instance.directory is None:
        if directory is None:
            directory = _upload_directory()
        if not os.path.exists(directory):
            os.makedirs(directory, 0700)
        instance.directory = mkdtemp(suffix='', prefix='', dir=directory)
    return os.path.join(instance.directory, filename)

class File(models.Model):
    data            = models.FileField(upload_to=_file_directory)
    checksum_format = models.CharField(verbose_name=_("Checksum Format"), max_length=16, choices=ChecksumFormats.CHOICES)
    checksum        = models.CharField(verbose_name=_("Checksum"), max_length=32)
    size            = models.PositiveIntegerField(verbose_name=_("Size"), help_text="File size in bytes")
    
    def __init__(self, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        self.directory = kwargs.get('directory', None)
    
    @property
    def mimetype(self):
        mimetype = mimetypes.guess_type(self.data.storage.path)[0]
        if mimetype is not None:
            return mimetype
        else:
            return 'application/octet-stream'
    
    @property
    def path(self):
        return self.data.storage.path
    
    @property
    def filename(self):
        return os.path.basename(self.data.storage.path)
    
    def generate_checksum(self, format='sha512'):
        with open(self.data.storage.path, 'rb+') as f:
            self.checksum = checksum(format, f)
            self.checksum_format = format

    def verify(self):
        with open(self.data.storage.path, 'rb+') as f:
            return checksum(self.checksum_format, f) == self.checksum

    def __unicode__(self):
        return self.filename

class Message(models.Model):
    key             = models.CharField(max_length=16, unique=True, db_index=True)
    sender          = models.ForeignKey(User, verbose_name=_("Sender"), db_index=True, related_name="filedrop_sent")
    recipients      = models.ManyToManyField(User, verbose_name=_("Recipients"), related_name="filedrop_recieved")
    date            = models.DateTimeField(verbose_name=("Date"))
    expiration      = models.DateTimeField(verbose_name=("Expiration Date"), null=True, blank=True, db_index=True)
    text            = models.TextField(verbose_name=("Text"))
    files           = models.ManyToManyField(File)
    require_authentication = models.BooleanField(verbose_name=_("Require Authentication"))
    
    class Meta:
        permissions = (
            ("can_receive", "Can receive messages"),
            ("can_send", "Can send messages"),
        )
    
    def set_key(self, key=''):
        if len(key) == 0:
            key_chars = re.sub(r'[cCIkKloOpPsSuUvVwWxXyYzZ01]', '', string.ascii_letters + string.digits)
            key = str()
            for n in range(4):
                key += random.choice(key_chars)
        self.key = key
    
    def __unicode__(self):
        return self.title

