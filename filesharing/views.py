import os
from datetime import timedelta, datetime

from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse
from django.utils.html import escape
from django.urls import reverse

from webutilits.settings import MEDIA_ROOT
from core.utilits import get_client_ip, incCountHit, incCountDownload
from filesharing.models import File
from filesharing.forms import (
    UploadForm,
    DeletePasswordForm,
    DownloadPasswordForm
)

DELETE_TIME_DELTA = {
    '1': timedelta(hours=1),
    '2': timedelta(days=1),
    '3': timedelta(days=7),
    '4': timedelta(days=30),
}


def upload(request):
    context = {}
    form = UploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        file_object = form.save(commit=False)

        choice_delta_del = form.cleaned_data.get('time_delete', 3)

        file_object.name = form.cleaned_data['file'].name
        file_object.creator_ip = get_client_ip(request)
        file_object.time_delete = datetime.now(tz=timezone.utc) + DELETE_TIME_DELTA[choice_delta_del]

        file_object.save()

        context['file_url'] = request.build_absolute_uri(file_object.get_absolute_url())
        print(context)
    context['form'] = form
    return render(request, 'filesharing/upload.html', context)


def file(request, file_id):
    context = dict()

    context['file'] = get_object_or_404(File, id=file_id)
    context['file_url'] = request.build_absolute_uri(context['file'].get_absolute_url())
    context['delete_form'] = DeletePasswordForm()
    context['download_form'] = DownloadPasswordForm()

    # Инкрементирую счетчик просмотров
    incCountHit(request, context['file'])

    return render(request, 'filesharing/file.html', context)


def checkPassword(request, file_id, field_name, form):
    # Совершает проверку над запросом, переданными данными и паролем
    if request.method == "POST":
        file = get_object_or_404(File, id=file_id)
        form = form(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == getattr(file, field_name):
                return file
            return JsonResponse({'status': 0, 'errors': ['Не правильный пароль']})
        return JsonResponse({'status': 0, 'errors': form.errors})
    return JsonResponse({'status': 0, 'errors': ['Разрешены только POST запросы']})


def download(request, file_id):
    # Реализует загрузку файла
    file = get_object_or_404(File, id=file_id)
    if file.password_for_download:
        # Проверка пароля
        response = checkPassword(request, file_id, 'password_for_download', DownloadPasswordForm)
        if type(response) is JsonResponse:
            return response

    if request.is_ajax():
        # Если запрос пришел на проверку пароля
        return JsonResponse({'status': 1})

    response = StreamingHttpResponse(open(MEDIA_ROOT+file.file.name, 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file.name)

    incCountDownload(request, file)

    return response


def delete(request, file_id):
    # Удаляет файл, если изначально был установлен пароль на его удаление, в
    # ином случае, это не возможно
    file = get_object_or_404(File, id=file_id)
    if not file.password_for_download:
        return JsonResponse({'status': 0, 'errors': ['Удаление - не возможно']})

    response = checkPassword(request, file_id, 'password_for_delete', DeletePasswordForm)
    if type(response) is JsonResponse:
        return response

    response.delete()
    return JsonResponse({'status': 1})
