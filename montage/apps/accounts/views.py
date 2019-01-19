from django.shortcuts import render

from .models import MontageUser


def mainview(request):
    user = MontageUser.objects.get(username='montage')
    as_atsign = user.as_atsign
    context = {'user': user, 'as_atsign': as_atsign}
    return render(request, 'user.html', context)
