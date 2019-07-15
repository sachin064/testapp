from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.
def home(request):
	if request.method == 'GET':
		return render(request, 'main/index.html')

def about(request):
	if request.method == 'GET':
		return render(request, 'about/about.html')
