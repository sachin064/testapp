import requests
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
import socket
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .helpers.secure import PasswordResetTokenGenerator, hashing_method
from .helpers.secure import account_activation_token

from crowdnext import settings
from .models import User
from .helpers import secure
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, response


@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        try:
            ip = get('https://api.ipify.org').text
            email = request.POST.get('email')
            password = request.POST.get('txt_pwd')
            password1 = request.POST.get('txt-pwd2')
            current_site = get_current_site(request)
            if password == password1:
                context = {
                    'email': email,
                    'password': password,
                    'ip': ip,
                }
                r = User(**context)
                r.save()
                html_content = render_to_string('email conform1.html', {
                    'uid': urlsafe_base64_encode(force_bytes(r.pk)).decode(),
                    'token': account_activation_token.make_token(r),
                    'ip': ip,
                    'domain': current_site.domain,
                    'email': email
                })
                text_content = strip_tags(html_content)
                print(urlsafe_base64_encode(force_bytes(r.pk)).decode())
                from_email = settings.EMAIL_HOST_USER
                subject = 'Thank you for Registreaing  with crowdnext'
                to_list = [email, settings.EMAIL_HOST_USER]
                msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
                msg.attach_alternative(html_content, "text/html")
                print(account_activation_token.make_token(r))
                msg.send()
                return render(request, 'gmail autentication.html',{'email':email})

            else:
                return render(request, 'register.html', {"message": "password miss matching"})
        except Exception as e:
            return render(request, 'register.html', {"message": "this email already exists"})


@api_view(["GET"])
def get_message(request):
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)
    send_url = 'http://api.ipstack.com/2401:4900:3306:f7c0:f9a4:e91a:126a:dc8f?access_key=38232ac57f8eef77a92b96b3fcb97ff7'
    r = requests.get(send_url)
    message = r.content
    data = json.loads(message)
    custom_message = "you are loged with  into your account with ip addtress" + IPAddr + "gps location is" + data[
        'continent_name'] + "place" + data['country_name'] + "city" + data['region_name']
    print(data)
    return Response({"data": custom_message})

@api_view(['GET'])
def logout_view(request):
    if request.method == 'GET':
        return render(request,'login.html')

@api_view(['GET', 'POST'])
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_register = True
        user.save()
        login(request, user)
        print(user)
        return render(request, 'login.html',
                      {"res": 'Thank you for your email confirmation. Now you can login to your account'})
    else:
        return render(request, 'already_conformed.html')


@api_view(['GET', 'POST'])
def password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_register = True
        user.save()
        login(request, user)
        print(user)
        return render(request, 'newpassword.html', {"res": uid})
    else:
        return HttpResponse('Activation link is invalid!')


@api_view(['GET', 'POST'])
def reset_paswoord(request):
    if request.method == 'POST':
        try:
            pwd = request.data.get('password')
            user = User.objects.get(id=request.session._session.get('id'))
            password1 = request.data.get('password1')
            password2 = request.data.get('password2')
            if password1 == password2 and user.password == pwd:
                user.password = password1
                user.save()
            return render(request,'login.html',{'message':'password changed sucesfully'})
        except Exception as e:
            return render(request,'login.html',{'message':'password mismatching'})


@api_view(['GET'])
def wallet(request):
    if request.method == 'GET':
        return render(request, 'wallet.html')


@csrf_exempt
@api_view(['POST'])
def confirm_otp(request, otp):
    if request.method == 'POST':
        user_otp = request.data.get('otp')
        print(type(otp), type(user_otp))
        if int(user_otp) == int(otp):
            return render(request, 'dashboard.html', {'message': 'sucess', 'id': request.session._session.get('id')})
        else:
            return render(request, 'login.html', {"message": "invalid otp"})
    else:
        return render(request,'login.html')


@api_view(['GET', 'POST'])
def newpassword(request, uid):
    if request.method == 'GET':
        return render(request, 'newpassword.html')

    elif request.method == 'POST':
        user = User.objects.get(id=uid)
        password = request.data.get('password')
        conformpassword = request.data.get('password')
        if password == conformpassword:
            user.password = password
            user.save()
            return render(request, 'login.html')
    else:
        return HttpResponse("invallid user")


from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import random


def gen_ran():
    ran = random.randrange(100000, 1000000)
    return ran


from django_otp.oath import hotp

secret_key = b'1234567890123467890'


def otp():
    for counter in range(5):
        l = (hotp(key=secret_key, counter=counter, digits=6))
        return l

from requests import get
from ipware import get_client_ip
from django.http import HttpRequest
@csrf_exempt
@api_view(['POST', 'GET'])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        try:
            ip =requests.get('https://ipinfo.io/geo')
            data = json.loads(ip._content)
            # ip = get('https://api.ipify.org').text
            os = request.user_agent.os.family,
            browser = request.user_agent.browser.family
            browserversion = request.user_agent.os.version
            # send_url = 'http://api.ipstack.com/check?access_key=38232ac57f8eef77a92b96b3fcb97ff7&ipAddress={}'.format(ip)
            # r = requests.get(send_url)
            email = request.data.get('email')
            password = request.data.get('password')
            user = User.objects.get(email=email)
            if user.is_register:
                if user.password == password:
                    if user.ip == ip:
                        html_content = render_to_string('loginemail1.html', {
                            'ip': data['ip'],
                            'city': data['city'],
                            'country':data['country'],
                            'region':data['region'],
                        })
                        text_content = strip_tags(html_content)
                        from_email = settings.EMAIL_HOST_USER
                        subject = 'you have succesfully Loged in to your Account'
                        to_list = [email, settings.EMAIL_HOST_USER]
                        msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        random_n = gen_ran()
                        html_content = render_to_string('otpemail.html', {
                            'otp': random_n
                        })
                        text_content = strip_tags(html_content)
                        from_email = settings.EMAIL_HOST_USER
                        subject = 'your login otp'
                        to_list = [email, settings.EMAIL_HOST_USER]
                        msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        request.session['id'] = user.id
                        # return render_to_response('dashboard.html', {"otp": random_n, "id": user.id},{'message':'sucess'})
                        return render_to_response('otp.html', {"otp": random_n, "id": user.id},{'message':'sucesss'})
                    else:
                        os = request.user_agent.os.family,
                        browser = request.user_agent.browser.family
                        browserversion = request.user_agent.os.version
                        html_content = render_to_string('loginemail1.html', {
                            'ip': data['ip'],
                            'city': data['city'],
                            'country': data['country'],
                            'region': data['region'],
                        })
                        text_content = strip_tags(html_content)
                        from_email = settings.EMAIL_HOST_USER
                        subject = 'you have  Loged in with the new ip If it is you Ignore this message'
                        to_list = [email, settings.EMAIL_HOST_USER]
                        msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        random_n = gen_ran()
                        html_content = render_to_string('otpemail.html', {
                            'otp': random_n
                        })
                        text_content = strip_tags(html_content)
                        from_email = settings.EMAIL_HOST_USER
                        subject = 'your login otp'
                        to_list = [email, settings.EMAIL_HOST_USER]
                        msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        request.session['id'] = user.id
                        return render(request, 'otp.html', {"otp": random_n,"id": user.id})
                else:
                    return render(request, 'login.html', {'message': 'invalid password'})
            else:
                return render(request, 'login.html', {'message': 'please conform your emailaddres'})
        except Exception as e:
            return render(request, 'login.html', {'message': 'invalid email addres'})


@api_view(['GET', 'POST'])
def forget_password(request):
    if request.method == 'GET':
        return render(request, 'forgot-password.html')
    elif request.method == 'POST':
        try:
            email = request.data.get('email')
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            html_content = render_to_string('forgotemailpass.html', {
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'domain': current_site.domain,
                'token': account_activation_token.make_token(user)
            })
            text_content = strip_tags(html_content)
            from_email = settings.EMAIL_HOST_USER
            subject = 'click the given link to change your password '
            to_list = [email, settings.EMAIL_HOST_USER]
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render(request, 'passwordresetmsg.html', {'message': 'new ip message'})
        except Exception as e:
            return render(request,'forgot-password.html',{'message':'invalid email addres '})


@api_view(['GET'])
def user_data(request, id):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=id)
            payload = {
                "email": user.email,
                "ip": user.ip,
                "host_name": user.host_name,
                "last_login": user.last_login
            }
        except Exception as e:
            message = str(e)
    return Response({"data": payload, "id": user.id})


