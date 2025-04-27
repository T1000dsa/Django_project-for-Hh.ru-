from django import forms
from ads.models import Ad, ExchangeProposal
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad

        exclude = ['user', 'created_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter item title'
            }),
            'description': forms.Textarea(attrs={
                'cols': 50,
                'rows': 5,
                'class': 'form-textarea'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'image_url': 'Image URL (optional)',
            'category': 'Item Category'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from view
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:  # Set user if provided
            instance.user = self.user
        if commit:
            instance.save()
        return instance

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 128:
            raise ValidationError('Title cannot exceed 128 characters')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 500:  # Assuming you want a limit
            raise ValidationError('Description cannot exceed 500 characters')
        return description


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите ваше предложение обмена...',
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label='Upload Item Image',
        help_text='Maximum size: 2MB',
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'class': 'form-control-file'
        })
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:  # 2MB limit
                raise ValidationError('Image file too large (max 2MB)')
            if not image.content_type.startswith('image'):
                raise ValidationError('File is not an image')
        return image