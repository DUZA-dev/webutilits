from hashlib import md5

from datetime import timedelta, datetime

from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from core.utilits import get_client_ip
from privatenote.forms import NoteForm
from privatenote.models import Note

DELETE_TIME_DELTA = {
    '1': timedelta(hours=1),
    '2': timedelta(days=1),
    '3': timedelta(days=7),
    '4': timedelta(days=30),
}


def index(request):
    context = {}
    form = NoteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        note_object = form.save(commit=False)

        choice_delta_del = form.cleaned_data.get('time_delete', 3)

        note_object.creator_ip = get_client_ip(request)
        note_object.time_delete = datetime.now(tz=timezone.utc) + DELETE_TIME_DELTA[choice_delta_del]
        note_object.url = md5("".join([
            str(note_object.id),
            str(note_object.note),
            str(datetime.now())
        ]).encode("utf8")).hexdigest()

        note_object.save()

        context['note_url'] = request.build_absolute_uri(note_object.get_absolute_url())

    context['form'] = form
    return render(request, 'privatenote/create.html', context)


def note(request, note):
    note = get_object_or_404(Note, url=note)
    if request.is_ajax() and request.method == "POST":
        password = request.POST.get('password', None)
        if note.password_for_read and note.password_for_read != md5(password.encode('utf8')).hexdigest():
            return JsonResponse({'status': 0, 'errors':['Не правильный пароль']})
        note.delete()
        return JsonResponse({'status': 1, 'note': note.note, 'pub_date': note.pub_date})
    return render(request, 'privatenote/note.html', context={'note': note})
