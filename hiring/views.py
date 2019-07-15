from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.
def hiring(request):
	return render(request, 'hiring/hiring.html')
