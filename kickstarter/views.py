from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from kickstarter import kickstarterservice


def index(request):
    res = kickstarterservice.get_campaigns()
    return render(request, 'kickstarter/index.html', res)


def get_popular_campaigns(request):
    if not request.method == 'GET':
        return HttpResponseBadRequest()

    hour = int(request.GET.get('hours', 0))
    res = kickstarterservice.get_campaigns(hour)
    return JsonResponse(res)
