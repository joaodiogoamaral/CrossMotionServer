# -*- coding: utf-8 -*-
from __future__ import unicode_literals
SCRIPT_DIR = '/home/ieeta/JoaoAmaral_Crossfit/MovementAnalysis'
UPLOADED_VIDEOS_DIR = 'UploadedVideos/'
OP_OUTPUT_DIR = 'server_output'
FEEDBACK_DIR = 'feedback/'



from django.shortcuts import redirect

import sys
sys.path.insert(0, SCRIPT_DIR)
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from models import Document
from forms import DocumentForm


import os
import ServerReadOutput
import ServerCompareVideos
import json


FEEDBACK_MATRIX = {
	'Squat': 'You tried to perform a squat.\n',
	#'DepthOk' : 'Hip crease dropped below knee line.\n'
	'BadDepth' : 'Try to drop your hips further below your knees.\n',
	#'SpineOk'  : 'You kept your chest high during the movement.\n'
	'BadSpine' : 'Try to keep your chest high and a tight back during the descending phase\n',

	'SquatOk'  : 'Your squat was performed perfectly, good job!! \n'


}







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
	
	result = []
	
	if request.method == 'POST' and (len(request.FILES)>0):
		response = 'Files uploaded:\n'

		for key in request.FILES.keys():
			vid = request.FILES[key]
			fs = FileSystemStorage()
			filename = fs.save(vid.name,vid)
			response = response + vid.name + 'uploaded \n'


			#run_crossmotion(filename)			
			feedback = run_crossmotion(filename)
			feedback['videoName'] = vid.name


			result.append(feedback)


		

		with open(os.path.join(os.getcwd(),FEEDBACK_DIR,'feedback'),'w') as outfile:
			json.dump(result,outfile)



		return redirect('feedback/')

	else:
		return HttpResponse('Invalid Method or no files in post!!!')


def show_uploaded(request):
	
	media_folder = OP_OUTPUT_DIR
	file_list = os.listdir(media_folder)
	
	response = 'Current videos in server:\n'
	
	if(len(file_list)>0):
		
		return render(request,'upload/show_uploaded.html',{'flist':file_list})
	
	
	
	return HttpResponse('No files to show')

		

def run_crossmotion(filename):



	print >> sys.stderr, 'RUNNING: ' + '/home/ieeta/JoaoAmaral_Crossfit/MovementAnalysis/CrossMotionRunOP.sh --compare '+ UPLOADED_VIDEOS_DIR + filename 


	os.system('/home/ieeta/JoaoAmaral_Crossfit/MovementAnalysis/CrossMotionRunOP.sh --check '+ UPLOADED_VIDEOS_DIR + filename )


	result = ServerCompareVideos.compareVideos(ServerReadOutput.readOutputs(OP_OUTPUT_DIR))

	return result






def feedback(request):





	with open(os.path.join(os.getcwd(),FEEDBACK_DIR,'feedback'),'r') as infile:

		data = json.load(infile)

		
	print(data)
	


	vidFeed = ''
	feedback = []
	for i in data:

		vidFeed += 'VIDEO -- ' + i['videoName'] + ':\n'

		if(i['exercise'] == 'squat'):

			vidFeed += 'Your video is a squat attempt!!\n'

			if(i['depth'] == 'OK' and i['spine'] == 'OK'):

				vidFeed+=FEEDBACK_MATRIX['SquatOk']
				continue

			if(i['depth'] == 'NOK'):

				print(i['depth'])

				vidFeed+=FEEDBACK_MATRIX['BadDepth']
				#vidFeed+=FEEDBACK_MATRIX['BadSpine']

			if(i['spine'] == 'NOK'):

				print(i['spine'])

				vidFeed+=FEEDBACK_MATRIX['BadSpine']

		feedback.append(vidFeed)

	return render(request,'upload/show_uploaded.html',{'flist':feedback})
	


	#return HttpResponse(vidFeed)

