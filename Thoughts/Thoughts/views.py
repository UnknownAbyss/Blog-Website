from django.http import HttpResponse
from django.shortcuts import render


def home(request):
	return render(request, "home.html")
	# return HttpResponse("Hey!! It's the home page")

def about(request):
	return HttpResponse("About hehe")