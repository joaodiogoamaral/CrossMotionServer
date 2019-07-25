# -*- coding: utf-8 -*-
from __future__ import unicode_literals
SCRIPT_DIR = '/home/ieeta/JoaoAmaral_Crossfit/CrossMotionServer/MovementAnalysis/'
UPLOADED_VIDEOS_DIR = 'UploadedVideos/'
OP_OUTPUT_DIR = 'OpenPoseOutput/'
FEEDBACK_DIR = 'Feedback/'
SERVER_DATA = '/home/ieeta/JoaoAmaral_Crossfit/CrossMotionServer/ServerData/'
PROCESSED_VIDEOS_DIR = 'ProcessedVideos/'


from django.shortcuts import redirect

import sys
sys.path.append(SCRIPT_DIR)

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate,login,logout


from models import Document,VideoEntry,Feedback
from forms import DocumentForm


import os
import ServerReadOutput
import ServerCompareVideos
import json

username = ''
password = ''


MEDIA_URL = settings.MEDIA_URL

FEEDBACK_MATRIX = {


	'Error' : 'There was a problem processing the video',

	'UnknownExercise' : 'Your video did not match any exercise in our database!',

	'NoPeople' : 'No people were found in your video!!!',

	'Squat': 'You tried to perform a squat.\n',
	#'DepthOk' : 'Hip crease dropped below knee line.\n'
	'BadDepth' : 'Try to drop your hips further below your knees.\n',
	#'SpineOk'  : 'You kept your chest high during the movement.\n'
	'BadSpine' : 'Try to keep your chest high and a tight back during the descending phase\n',

	'GoodDepth' : 'Your squat depth is correct!.\n',

	'SquatOk'  : 'Your squat was performed perfectly, good job!! \n',

	'kbswing': 'You tried to perform a Kettlebell Swing.\n',

	'Goodkbswing' : 'Your Kettlebell Swing was well performed, good job!\n',

	'BadkbSwing' : 'Your Kettlebell Swing can use some improvements... \n',

	'kbswingTip1' : 'Keep your back straight and use your legs for the swing \n',

	'kbswingTip2' : 'Raise your arms fully extended untill the Kettlebell bottom points to the ceiling. \n', 


}

#def login(request):


#	return HttpResponse(status=200)


@csrf_exempt
def uploadlogin(request):
	global username
	global password
	
	if(request.method=='POST'):

		username = request.META['HTTP_USERNAME']
		password = request.META['HTTP_PASS']

		

		user = authenticate(username=username,password=password)

		if user and user.is_active:

			return HttpResponse(status=200)
		else:
			return HttpResponse(status=401)





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


@csrf_exempt
def upload_video(request):
	
	global username


	if(username==''):
		return HttpResponse(status=401) #unauthorized


	result = []
	print(request.FILES)
	
	if request.method == 'POST' and request.FILES['uploaded_file']:
		

		#form = DocumentForm(request.POST,request.FILES)

		#if(form.is_valid()):
		#	print("VALID FORM")
		#else:
		#	print("Invalid")

		response = 'Files uploaded:\n'

		vid = request.FILES['uploaded_file']

		#print(vid.name)

		fs = FileSystemStorage()

		#filepath = UPLOADED_VIDEOS_DIR + username + '/' + vid.name

		

		filename = fs.save(UPLOADED_VIDEOS_DIR + username + '/' + vid.name,vid)

		videoname = os.path.splitext(os.path.basename(filename))[0]

		print('FILENAME:'+filename + '\nvideoname:' + videoname)



		op_output_path=SERVER_DATA+PROCESSED_VIDEOS_DIR + username + '/' + videoname + '/' + videoname + '.avi' 


		print('op_output_path:'+op_output_path)


		feedback = run_crossmotion(os.path.basename(filename))

		videEntry= VideoEntry(username=username,videoUploaded=os.path.basename(filename),processedVideoPath=username+'/'+videoname+'/'+os.path.basename(filename))

		for i in feedback:

			entry = Feedback(feedback=i)
			entry.save()
			print('Entry to add:')
			print(entry.feedback)
			videEntry.save()
			videEntry.feedback.add(entry)

			

		
		
		videEntry.save()
		# print(videEntry)





		return HttpResponse(status=200)


	else:
		return HttpResponse(status=402)


def show_uploaded(request):
	
	global username
	username = None

	if(request.user.is_authenticated()):
		username = request.user.username



	print('\nLOGGED IN: \n' + username)

	media_folder = SERVER_DATA

	
	db_list = VideoEntry.objects.all()
	
	response = 'Current videos in server:\n'
	flist = []
	if(len(db_list)>0):
		
		for i in db_list:

			if(i.username==username):

				flist.append(i.videoUploaded.decode('utf-8'))
				#flist.append('batata')

		print(flist)

		return render(request,'upload/show_uploaded.html',{'flist':flist,'user':username})
	
	
	
	return HttpResponse('No files to show')

		

def run_crossmotion(filename):


	#print(filename)
	global username

	print >> sys.stderr, 'RUNNING: ' + '/home/ieeta/JoaoAmaral_Crossfit/CrossMotionServer/MovementAnalysis/CrossMotionRunOP.sh --compare '+ filename 


	os.system('/home/ieeta/JoaoAmaral_Crossfit/CrossMotionServer/MovementAnalysis/CrossMotionRunOP.sh --check ' + filename + ' ' + username )


	outputPath = os.path.splitext(SERVER_DATA + OP_OUTPUT_DIR+username+'/'+filename)[0]


	output = ServerReadOutput.readOutputs(outputPath)

	result = []

	if(len(output.keys())==1):

		result.append(FEEDBACK_MATRIX['NoPeople'])

		#print(result)

		return result
	else:

		
		



		comparison=ServerCompareVideos.compareVideos(output)



		if(comparison['exercise'] == 'squat'):

			result.append(FEEDBACK_MATRIX['Squat'])


			#return SPINE OK when in frontal plane
			if(comparison['depth'] == 'OK' and comparison.get('spine','OK') == 'OK'):

				result.append(FEEDBACK_MATRIX['SquatOk'])

				return result
			
			if(comparison['depth'] == 'NOK'):

				result.append(FEEDBACK_MATRIX['BadDepth'])
			else:
				result.append(FEEDBACK_MATRIX['GoodDepth'])

			if( (comparison.get('spine',None) != None) and comparison['spine'] == 'NOK'):

				result.append(FEEDBACK_MATRIX['BadSpine'])


		elif(comparison['exercise'] == 'kbswing'):

			result.append(FEEDBACK_MATRIX['kbswing'])

			if(comparison['depth'] == 'NOK'):
				result.append(FEEDBACK_MATRIX['BadkbSwing'])
				result.append(FEEDBACK_MATRIX['kbswingTip1'])
				result.append(FEEDBACK_MATRIX['kbswingTip2'])
			else:
				result.append(FEEDBACK_MATRIX['Goodkbswing'])




		else:

			result.append(FEEDBACK_MATRIX['UnknownExercise'])




		print(result)

		return result








def feedback(request,video_name):

	#MEDIA_URL = SERVER_DATA + PROCESSED_VIDEOS_DIR 

	db_list = VideoEntry.objects.all()
	
	global username

	print(db_list)

	print(username)

	op_output_path = ''

	flist = []

	for i in db_list:

		if(i.videoUploaded==video_name and i.username == username):


			

			op_output_path = i.processedVideoPath

			print(op_output_path)

			for j in i.feedback.all():
				#Feedback model object has a charField named feedback
				flist.append(j.feedback)
	


	return render(request,'upload/feedback.html',{'directives':flist,'video_name':video_name , 'op_output_path':op_output_path  , 'MEDIA_URL':MEDIA_URL} )




class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('upload:login')
    template_name = 'registration/signup.html'



