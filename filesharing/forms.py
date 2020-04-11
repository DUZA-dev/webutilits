from hashlib import md5

from django import forms

from filesharing.models import File
from django.core.exceptions import ValidationError


DELETE_TIME_CHOICE = [
    ('1', '1 час'),
    ('2', '1 день'),
    ('3', '7 дней'),
    ('4', '30 дней'),
]


class UploadForm(forms.ModelForm):
    time_delete = forms.ChoiceField(choices=DELETE_TIME_CHOICE)

    class Meta:
        model = File
        fields = ['file', 'description', 'password_for_delete', 'password_for_download']

        widgets = {
            'password_for_delete': forms.PasswordInput(
                attrs={'placeholder': 'Пароль для удаления'}
            ),
            'password_for_download': forms.PasswordInput(
                attrs={'placeholder': 'Пароль для скачивания'}
            ),
            'description': forms.TextInput(
                attrs={'placeholder': 'Описание файла'}
            )
        }

    def clean_password_for_delete(self):
        password = self.cleaned_data.get('password_for_delete', None)
        if not password:
            return password
        return md5(password.encode('utf8')).hexdigest()

    def clean_password_for_download(self):
        password = self.cleaned_data.get('password_for_download', None)
        if not password:
            return password
        return md5(password.encode('utf8')).hexdigest()

    def clean_file(self):
        file = self.cleaned_data.get('file', None)
        if not file:
            raise ValidationError('Поле файла - обязательно.')

        max_megabyte = 50
        max_bits = max_megabyte * 1024 * 1024

        if file.size > max_bits:
            raise ValidationError('Файл слишком большой. Максимальный размер файла %i MiB.') % max_megabyte

        return file
