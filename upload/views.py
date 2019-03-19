# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from models import Document
from forms import DocumentForm


import os

# Create your views here.
def upload(request):
	
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		return render(request, 'upload.html', {
			'uploaded_file_url': uploaded_file_url
		})
    
		return render(request, 'upload.html')
	else:
		return HttpResponse('Invalid HTTP method!!!')


def model_form_upload(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST,request.FILES)
		
		if form.is_valid():
			
			return upload_video(request)
	else:
		form = DocumentForm()
		
	return render(request,'upload/model_form_upload.html',{'form':form})

def upload_video(request):
	
	
	if request.method == 'POST' and (len(request.FILES)>0):
		response = 'Files uploaded:\n'

		for key in request.FILES.keys():
			vid = request.FILES[key]
			fs = FileSystemStorage()
			filename = fs.save(vid.name,vid)
			response = response + vid.name + '\n'
		return HttpResponse(response)
	else:
		return HttpResponse('Invalid Method or no files in post!!!')


def show_uploaded(request):
	
	media_folder = settings.MEDIA_ROOT
	file_list = os.listdir(media_folder)
	
	response = 'Current videos in server:\n'
	
	if(len(file_list)>0):
		
		return render(request,'upload/show_uploaded.html',{'flist':file_list})
	
	
	
	return HttpResponse('No files to show')

		
