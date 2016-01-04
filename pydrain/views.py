##
# @package civilsage.views
# This module contain functions to controls veiws of django.
# It include following functions -:
# index()
# file()
# ...
# @author amarjeet kapoor

# @code importing modules
import os,threading
from django.http import HttpResponse
from django.shortcuts import render
import csv,datetime
from django.core.mail import EmailMessage

def index(request):
    return render(request,'pydrain/file.html')

def file(request):
    message='please fill again'
    #getting file uploaded by user
    name='Temp'+request.session.session_key+str(datetime.datetime.now())
    name=name.replace(" ", "")
    f=request.FILES["input_file"]
    if(f.content_type != 'text/csv'):
        return render( request,'pydrain/file.html',
        {'message':'File Not in CSV FORMAT '})
    namecsv=name+'.csv'
    namedxf=name+'.dxf'
    data=f.read()
    f=open(namecsv,'w')
    f.write(data)
    f.close()
    command='python pyDrain.py '+name+'  '+namecsv
    os.system(command)
    #sending pdf as response
    f=open(namedxf)
    response = HttpResponse(f,content_type='plain/text')
    response['Content-Disposition'] ='attachment;filename='+namedxf
    #deleting temperary files
    command='rm '+namedxf+' '+namecsv
    os.system(command)
    return response

##
# A function that run as background process to send pdf as emails and called
# by last() and file() when email option is chossen
# @param request request from calling function
# @param name name of directory to becreated for user
# @exception send error message through email

