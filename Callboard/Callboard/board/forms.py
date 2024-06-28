from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Announcement, Comment
from django import forms
from django.core.exceptions import ValidationError
from .extensions import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from string import hexdigits
import random
from django.conf import settings
from django.core.mail import send_mail


class PostForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=ROLES,
        label='Выберите категорию',
        help_text='*Обязательное поле',
        error_messages={
            'required': 'Необходимо выбрать категорию!'
        },
        widget=forms.Select(attrs={'class': 'myfield'})
    )

    title = forms.CharField(
        min_length=1,
        label='Заголовок',
        help_text='*Обязательное поле',
        error_messages={
            'required': 'Необходимо добавить заголовок!'
        },
        widget=forms.TextInput(attrs={'class': 'myfield'})
    )

    content = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label='Содержание объявления',
        required=True,
    )
    class Meta:
        model = Announcement
        fields = ['category', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        title = cleaned_data.get('title')

        if title == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Текст отклика:"


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user