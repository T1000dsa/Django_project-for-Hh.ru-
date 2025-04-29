from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
import logging

import base_app.settings as sett 
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordForm
from ads.utils import DataMixin

logger = logging.getLogger(__name__)

class UserLogin(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    title_page = 'Вход'
    

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_done')
    title_page = 'Регистрация'


class RegisterUserDone(DataMixin, TemplateView):
    template_name = 'users/register_200.html'

class LogoutUser(LogoutView):pass

class ProfileUser(DataMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    title_page = 'Профиль'
    extra_context = {'default_image': sett.DEFAULT_USER_IMAGE}
    
    def get_success_url(self):
        return reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):

        selected_message = form.cleaned_data.get('message')
        logger.debug(f'{selected_message}')
        if selected_message:
            return redirect('proposal_detail', pk=selected_message.pk)
        return super().form_valid(form)
    
    
class UserPassChange(DataMixin, LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class PasswordChangeDoneViewMofify(DataMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'


class PassReset(DataMixin, PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

class PassResetDone(DataMixin, PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class PassConfirm(DataMixin, PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class PassResetComplete(DataMixin, PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'