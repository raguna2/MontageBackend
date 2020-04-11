from django.http import HttpResponse


def mainview(request):
    return HttpResponse('Hello, World!')
