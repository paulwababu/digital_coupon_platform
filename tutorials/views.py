from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import TutorialForm
from .models import Tutorial
from django.contrib import messages
import uuid
import os
import psutil
import urllib3
from django.core.paginator import Paginator
import datetime
import africastalking
import requests
#random 6 digit generator
def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.


#phone number view
def phone(request):
    if request.method == 'POST':
        number = request.POST['numbari']
        request.session['phonenumber'] = number
        print(request.session['phonenumber'])
        #initialize the sdk
        username = "digital"
        api_key = "24475cdb3f486f244e38a12b3aca908044f81e9f3f1fbf305b809abee0a86aeb"
        africastalking.initialize(username,api_key)
        #recipients
        number1 = ("+"+number)
        recipients = [number1]
        #message
        generatedCode = my_random_string(6)
        request.session['generatedCode'] = generatedCode
        message = generatedCode # For example, D9E50C
        #initialize the service, in our case, SMS
        sms = africastalking.SMS
        #USE THE SERVICE
        def on_finish(error, response):
            if error is not None:
                raise error
            print(response)
        sms.send(message, recipients, callback=on_finish)
        return redirect('otp')
    return render(request, 'tutorial/login.html')

#otp view
def otp(request):
    try:
        number = request.session['phonenumber']
    except:
        return render(request, "home2.html")
    print(number)
    if request.method == 'POST':
        otp_entered = request.POST['otp_code']
        generatedCode = request.session['generatedCode']
        if otp_entered == generatedCode:
            return redirect('scanner')
        return HttpResponse("Wrong Code Entered!")
    return render(request, 'tutorial/otp.html')


#image submit view
def scanner(request):
    try:
        number = request.session['phonenumber']
    except:
        return render(request, "home2.html")
    print(number)
    if request.method == 'POST':
        files = request.FILES['files']
        generatedCode = request.session['generatedCode']
        datetime = "5th January 2021"
        ip = "4.335.432.22"
        saveNow = Tutorial(
            number=number,
            feature_image=files,
            city='NaivasUmoja',
            datetime=datetime,
            ip=ip,
        )
        saveNow.save()
        return redirect('ocr')
    return render(request, 'tutorial/scanner.html')    

#image scanner view using ocr model trained on nanonets platform
def ocr(request):
    try:
        number = request.session['phonenumber']
    except:
        return render(request, "home2.html")
    print(number)
    url = 'https://app.nanonets.com/api/v2/OCR/Model/b7f14685-5f2d-4d10-8693-2b717a902e65/LabelUrls/'
    headers = {
        'accept': 'application/x-www-form-urlencoded'
    }
    data = {'urls' : ['https://pbs.twimg.com/media/CU1eHFvWUAA8wb-.jpg']}
    response = requests.request('POST', url, headers=headers, auth=requests.auth.HTTPBasicAuth('Ct3BzSvuao0XGI63hhFGzqQNDrwfkvMe', ''), data=data)
    print(response.json)
    #delete sessions after user is done with process
    del request.session['generatedCode']
    del request.session['phonenumber']
    return HttpResponse('Check MPESA')

def tutorialList(request):
    tutorials = Tutorial.objects.all()
    return render(request, 'tutorial/list.html', { 'tutorials' : tutorials})

def deleteTutorial(request, pk):
    try:
        number = request.session['phonenumber']
    except:
        return render(request, "home2.html")
    print(number)
    if request.method == 'POST':
        tutorial = Tutorial.objects.get(pk=pk)
        tutorial.delete()
    return redirect('tutorial_list')

def success(request):
	return HttpResponse('successfully uploaded')    