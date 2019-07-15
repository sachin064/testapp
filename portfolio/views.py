from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.
def portfolio(request):
	return render(request, 'portfolio/portfolio.html')

def partners(request):
	return render(request, 'partners/partners.html')

