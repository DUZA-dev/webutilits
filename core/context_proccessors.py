import os
import random

from webutilits.settings import MEDIA_ROOT


def BgImgPathMiddleware(request):
    return {
        'bgImgPath': random.choice(os.listdir(MEDIA_ROOT+'backgrounds/')),
        'bgGifPath': random.choice(os.listdir(MEDIA_ROOT+'backgrounds-gif/'))
    }
