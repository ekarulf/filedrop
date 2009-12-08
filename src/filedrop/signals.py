from django.db.models.signals import pre_save

def set_key(sender, instance):
    if len(instance.key) == 0:
        instance.set_key()

def generate_checksum(sender, instance):
    if len(instance.checksum) == 0 or len(instance.checksum_format) == 0:
        instance.generate_checksum()

pre_save.connect(set_key, sender=Message)
pre_save.connect(generate_checksum, sender=File)
