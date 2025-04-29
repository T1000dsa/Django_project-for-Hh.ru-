from django.test import TestCase
from users.models import User  # Import your custom User model
from .models import Ad, ExchangeProposal

class ProposalTest(TestCase):
    def setUp(self):
        # Create test users using your custom User model
        self.user1 = User.objects.create_user(
            username='user1', 
            password='testpass123',
            email='user1@test.com'  # Add required fields for your User model
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            password='testpass123',
            email='user2@test.com'
        )
    
    def test_proposal_accept(self):
        ad1 = Ad.objects.create(
            user=self.user1,
            title="Test Ad 1",
            description="Test Description",
            category="books",
            condition="new"
        )
        ad2 = Ad.objects.create(
            user=self.user2,
            title="Test Ad 2",
            description="Test Description",
            category="electronics",
            condition="used"
        )
        
        proposal = ExchangeProposal.objects.create(
            ad_sender=ad1,
            ad_receiver=ad2,
            comment="Test proposal"
        )
        proposal.get_accept_url()
        self.assertEqual(proposal.status, 'accepted')