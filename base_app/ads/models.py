from django.db import models

class Ad(models.Model):
    user = models.CharField(max_length=128,unique=True)
    
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    image_url = models.URLField()
    category = models.CharField(max_length=128)
    condition = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class ExchangeProposal(models.Model):
    ad_sender = models.IntegerField()
    ad_receiver = models.IntegerField()
    comment = models.CharField(max_length=128)
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

