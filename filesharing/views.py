from datetime import timedelta, datetime

from django.shortcuts import render
from django.http import JsonResponse

from filesharing.forms import UploadForm
from shorturl.utilits import get_client_ip

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
        file_object.time_delete = datetime.now() + DELETE_TIME_DELTA[choice_delta_del]

        file_object.save()

        return JsonResponse({
            'status': 1,
            'file_url': file_object.get_absolute_url()
        })
    context['form'] = form
    return render(request, 'filesharing/upload.html', context)
