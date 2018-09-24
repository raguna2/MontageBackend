from django.http import HttpResponse
from django.shortcuts import render

from .models import MontageUser


def mainview(request):
    user = MontageUser.objects.get(username='raguna2')
    as_atsign = user.as_atsign
    context = {'user': user, 'as_atsign': as_atsign}
    return render(request, 'user.html', context)
