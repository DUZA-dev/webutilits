from django.core.exceptions import ObjectDoesNotExist

from background_task import background

from privatenote.models import Note
from filesharing.models import File


@background(schedule=60*60*24)
def delete_note_schedule(note_id):
    try:
        note = Note.objects.get(id=note_id)
        note.delete()
    except ObjectDoesNotExist:
        pass


@background(schedule=60*60*24)
def delete_file_schedule(file_id):
    try:
        file = File.objects.get(id=file_id)
        file.delete()
    except ObjectDoesNotExist:
        pass
