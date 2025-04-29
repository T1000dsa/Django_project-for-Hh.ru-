from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, FormView, CreateView, UpdateView, DeleteView, ListView
from ads.utils import DataMixin
from django.http import HttpResponse
from ads.models import Ad, ExchangeProposal
from users.models import User
from ads.forms import AdForm, ExchangeProposalForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.http import HttpRequest, Http404
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

import logging

logger = logging.getLogger(__name__)


def page_not_found(request, exception):
    return render(request, 'ads/not_found.html')


def ad_list(request):
    ads = Ad.objects.all()
    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category = request.GET.get('category')
    if category:
        ads = ads.filter(category=category)
    return render(request, 'ads/list.html', {'page_obj': page_obj})

@login_required
def accept_proposal(request, pk):
    logger.debug(f'accept_proposal')
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    
    if request.user != proposal.ad_receiver.user:
        messages.error(request, "You don't have permission to accept this proposal")
        return redirect('some_redirect_view')
    
    if proposal.get_accept_url():
        messages.success(request, "Proposal accepted successfully")
    else:
        messages.warning(request, "Only pending proposals can be accepted")
    
    return redirect('proposal_detail', pk=proposal.pk)

@login_required
def reject_proposal(request, pk):
    logger.debug(f'reject_proposal')
    proposal = get_object_or_404(ExchangeProposal, pk=pk)

    logger.debug(f'reject_proposal 1')
    if request.user != proposal.ad_receiver.user:
        messages.error(request, "You don't have permission to reject this proposal")
        return redirect('some_redirect_view')
    
    logger.debug(f'reject_proposal 2')
    
    if proposal.get_reject_url():
        messages.success(request, "Proposal rejected")
    else:
        messages.warning(request, "Only pending proposals can be rejected")
    logger.debug(f'reject_proposal 3')
    
    return redirect('proposal_detail', pk=proposal.pk)
    

class IndexHome(DataMixin, TemplateView):
    template_name = 'ads/main_page.html'
    title_page = 'Главная'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context)
    
    
class CreateAd(DataMixin, LoginRequiredMixin, CreateView):
    template_name = 'ads/create_ad.html'
    title_page = 'Добавить Объявление'
    success_url = reverse_lazy('home_page')
    model = Ad
    form_class = AdForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    

class EditAd(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = 'ads/edit_ad.html'
    title_page = 'Редактировать'
    fields = ['title', 'description', 'image_url', 'category', 'condition']
    success_url = reverse_lazy('home_page')
    model = Ad

    
    def dispatch(self, request, *args, **kwargs):
        try:
            ad = Ad.objects.get(pk=kwargs['pk'])
            if ad.user != request.user:
                return render(request, 'ads/not_users_ad.html')
            self.object = ad
            return super().dispatch(request, *args, **kwargs)
        except Ad.DoesNotExist:
            return render(request, 'ads/not_users_ad.html')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
    

class DeleteAd(DataMixin, LoginRequiredMixin, DeleteView):
    template_name = 'ads/delete_ad.html'
    title_page = 'Удалить Объявление'
    success_url = reverse_lazy('home_page')
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            ad = Ad.objects.get(pk=kwargs['pk'])
            if ad.user != request.user:
                return render(request, 'ads/not_users_ad.html')
            self.object = ad
            return super().dispatch(request, *args, **kwargs)
        except Ad.DoesNotExist:
            return render(request, 'ads/not_users_ad.html')
            
    

class ShowAds(DataMixin, LoginRequiredMixin, ListView):
    template_name = 'ads/show_ads.html'
    title_page = 'Смотреть Объявления'
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            index_list=context['ad_list']
            )
    

class ShowAd(DataMixin,LoginRequiredMixin, DetailView):
    template_name = 'ads/show_ad.html'
    title_page = 'Смотреть Объявление'
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_pk = self.request if self.request.user.is_authenticated else None
        
        return self.get_mixin_context(
            context,
            current_user=user_pk
        )
    

class CreateExchange(DataMixin, LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/barter.html'
    success_url = reverse_lazy('create_exchange')
    title_page = 'Обмен'

    def get_success_url(self):

        return reverse('show_ad', kwargs={'pk': self.kwargs['ad_receiver_id']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_receiver'] = Ad.objects.get(pk=self.kwargs['ad_receiver_id'])
        return context

    def form_valid(self, form):
        try:
            sender_user = get_object_or_404(
                get_user_model(),
                pk=self.kwargs['ad_sender_id']
            )

            if sender_user != self.request.user:
                raise PermissionDenied("Вы не можете создавать обмен от имени другого пользователя")

            sender_ads = Ad.objects.filter(user=sender_user)

            if sender_ads.count() == 0:
                logger.info("No ads found for sender user")
                form.add_error(None, "У вас нет объявлений для обмена")
                return self.form_invalid(form)
            
            ad_sender = sender_ads.first()
            
            ad_receiver = get_object_or_404(
                Ad, 
                pk=self.kwargs['ad_receiver_id']
            )

            if ad_sender.user == ad_receiver.user:
                form.add_error(None, "Нельзя предложить обмен на своё же объявление")
                return self.form_invalid(form)

            form.instance.ad_sender = ad_sender
            form.instance.ad_receiver = ad_receiver
            form.instance.status = 'pending'
            
            response = super().form_valid(form)
            messages.success(self.request, "Обмен успешно предложен!")
            return response
            
        except (Ad.DoesNotExist, get_user_model().DoesNotExist):
            raise Http404("Объект не найден")
        
        except IntegrityError as err:
            return render(self.request, "ads/already_exist.html")

        except Exception as err:
            logger.error(f"Exchange creation failed: {err}", exc_info=True)
            raise err
        

class ProposalDetailView(DataMixin, LoginRequiredMixin, DetailView):
    model = ExchangeProposal
    template_name = 'ads/barter_detail.html'
    context_object_name = 'proposal'

    def get_queryset(self):
        return super().get_queryset().filter(
            models.Q(ad_sender__user=self.request.user) |
            models.Q(ad_receiver__user=self.request.user)
        )
        