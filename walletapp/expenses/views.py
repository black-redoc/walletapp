from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="expenses/index.html")