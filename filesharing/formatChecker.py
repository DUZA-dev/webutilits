from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat


class ContentTypeRestrictedFileField(FileField):

    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop("max_upload_size", 0)

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if file._size > self.max_upload_size:
                raise forms.ValidationError(
                    'Максимальный размер файла %s. Загруженный файл имеет размер %s' % (filesizeformat(self.max_upload_size), filesizeformat(file._size))
                )
        except:
            forms.ValidationError('Неожиданная ошибка')
