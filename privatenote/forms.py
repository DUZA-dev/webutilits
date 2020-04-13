from hashlib import md5

from django import forms

from privatenote.models import Note


DELETE_TIME_CHOICE = [
    ('1', '1 час'),
    ('2', '1 день'),
    ('3', '7 дней'),
    ('4', '30 дней'),
]


class NoteForm(forms.ModelForm):
    time_delete = forms.ChoiceField(choices=DELETE_TIME_CHOICE)

    class Meta:
        model = Note
        fields = ['note', 'password_for_read']

        widgets = {
            'password_for_read': forms.PasswordInput(
                attrs={'placeholder': 'Пароль для чтения'}
            ),
            'note': forms.Textarea(
                attrs={'placeholder': 'Введите заметку'}
            )
        }

    def clean_password_for_read(self):
        password = self.cleaned_data.get('password_for_read', None)
        if not password:
            return password
        return md5(password.encode('utf8')).hexdigest()
