import re

from django import forms


class ShortenerUrlForm(forms.Form):
    # Форма для ввода ссылки для сокращения
    url = forms.URLField(
        max_length=4000,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ссылку',
        })
    )

    def clean_url(self):
        full_url = self.cleaned_data['url']

        regular_expression = r"^(\w*):[\\\/]{2}(.*)$"
        regular_execute = re.match(regular_expression, full_url)

        try:
            protocol = regular_execute.group(1)
            url = regular_execute.group(2)
        except AttributeError:
            raise forms.ValidationError("Введите правильный URL!")

        if protocol == "http":
            protocol = "https"

        return protocol, url
