from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=128)
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/у')
    ]

    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.title
    
    def get_pk(self):
        return reverse('show_ad', kwargs={'pk':self.pk})
    
    def get_to_update(self):
        return reverse('edit_ad', kwargs={'pk':self.pk})
    
    def get_to_delete(self):
        return reverse('delete_ad', kwargs={'pk':self.pk})
    
    def get_exchange(self, sender_ad_id):
        """Generate proper exchange URL between two ads"""
        logger.debug(f'ad_sender_id: {sender_ad_id} ad_receiver_id: {self.id}')
        return reverse('create_exchange', kwargs={
            'ad_sender_id': sender_ad_id, # User id
            'ad_receiver_id': self.id # Ad id
        }) 


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(
        'Ad',
        on_delete=models.CASCADE,
        related_name='sent_proposals'
    )
    ad_receiver = models.ForeignKey(
        'Ad',
        on_delete=models.CASCADE,
        related_name='received_proposals'
    )

    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal from {self.ad_sender} to {self.ad_receiver}"
    
    def get_accept_url(self):
        
        if self.status != 'pending':
            raise ValueError("Only pending proposals can be accepted")
        
        self.status = 'accepted'
        self.save()
        return reverse('accept_proposal', kwargs={'pk': self.pk})

    def get_reject_url(self):

        if self.status != 'pending':
            raise ValueError("Only pending proposals can be rejected")
        
        self.status = 'rejected'
        self.save()
        return reverse('reject_proposal', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('ad_sender', 'ad_receiver')