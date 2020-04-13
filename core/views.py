from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')


def handler404(request, msg="Старница не найдена :(", status=404, *args, **argv):
    context = {
        "title_": "Ошибка 404",
        "message": msg,
        "robots": "noindex,nofollow"
    }
    return render(request, "core/error.html", context, status=status)
