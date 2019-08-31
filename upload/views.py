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


from models import Document,VideoEntry,Feedback,Rep
from forms import DocumentForm


import os
import ServerReadOutput
import ServerCompareVideos
import json

username = ''
password = ''


MEDIA_URL = settings.MEDIA_URL

FEEDBACK_MATRIX = {


	'NoRepsFound' : 'There was a problem identifying the repetitions on your video.\n',

	'Error' : 'There was a problem processing the video\n',

	'UnknownExercise' : 'We could not identify yout movement\n',

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


		feedbackEntries = run_crossmotion(os.path.basename(filename))

		videEntry= VideoEntry(username=username,videoUploaded=os.path.basename(filename),repCount=len(feedbackEntries),processedVideoPath=username+'/'+videoname+'/'+os.path.basename(filename))
		videEntry.save()
		repNo = 0

		
		for i in feedbackEntries:

			print('\n\nfeedbackEntries:\n\n')
			print(i)
			#create new class Rep
			rep = Rep(repNumber=repNo+1)
			
			repNo = repNo + 1 

			for j in i:
			#create new class feedback
				print('\n\n Adding feedback: \n\n' + j)
				feedback = Feedback(feedback=j)
				feedback.save()
				
				rep.save()

				rep.feedback.add(feedback)

				rep.save()
			
			print(rep.feedback.all())
			
			print('Adding one rep!!!\n\n')
			videEntry.rep.add(rep)

			videEntry.save()

		print('Entry to add:')
		print(videEntry.rep.all())
		
		
		print('REPCOUNT: ' + str(videEntry.repCount))

			

		
		
		
		# print(videEntry)





		return HttpResponse(status=200)


	else:
		return HttpResponse(status=402)


def show_uploaded(request):
	
	global username
	

	if(request.user.is_authenticated()):
		username = request.user.username
	else:
		return reverse_lazy('upload:login')


	print('\nLOGGED IN: \n' + username)

	media_folder = SERVER_DATA

	
	db_list = VideoEntry.objects.all()
	
	response = 'Current videos in server:\n'
	flist = []
	if(len(db_list)>0):
		
		for i in db_list:

			if(i.username==username):

				flist.append(i.videoUploaded.decode('utf-8'))


		print(flist)

		return render(request,'upload/show_uploaded.html',{'flist':flist,'user':username})
	
	
	
	return HttpResponse('No files to show')

		

def run_crossmotion(filename):


	#print(filename)
	global username

	print >> sys.stderr, 'RUNNING: ' + '/home/ieeta/JoaoAmaral_Crossfit/CrossMotionServer/MovementAnalysis/CrossMotionRunOP.sh --compare '+ filename 


	os.system('/home/ieeta/JoaoAmaral_Crossfit/CrossMotionServer/MovementAnalysis/CrossMotionRunOP.sh --check ' + filename + ' ' + username )


	outputPath = os.path.splitext(SERVER_DATA + OP_OUTPUT_DIR+username+'/'+filename)[0]


	[rawOutput,output] = ServerReadOutput.readOutputs(outputPath)

	#ServerCompareVideos.checkReps(rawOutput)

	

	if(len(output.keys())==1):

		result.append(FEEDBACK_MATRIX['NoPeople'])

		#print(result)

		return result
	else:

		
		


		feedbackEntries = []

		comparison=ServerCompareVideos.compareVideos(rawOutput,output)

		if(len(comparison) == 0):
			result = []

			result.append(FEEDBACK_MATRIX['NoRepsFound'])

			feedbackEntries.append(result)

			return feedbackEntries

		
		for i in comparison:
			
			result=[]

			if(i['exercise'] == 'squat'):

				result.append(FEEDBACK_MATRIX['Squat'])


				#return SPINE OK when in frontal plane
				if(i['depth'] == 'OK' and i.get('spine','OK') == 'OK'):

					result.append(FEEDBACK_MATRIX['SquatOk'])

					
				
				if(i['depth'] == 'NOK'):

					result.append(FEEDBACK_MATRIX['BadDepth'])
				else:
					result.append(FEEDBACK_MATRIX['GoodDepth'])

				if( (i.get('spine',None) != None) and i['spine'] == 'NOK'):

					result.append(FEEDBACK_MATRIX['BadSpine'])


			elif(i['exercise'] == 'kbswing'):

				result.append(FEEDBACK_MATRIX['kbswing'])

				if(i['depth'] == 'NOK'):
					#result.append(FEEDBACK_MATRIX['BadkbSwing'])
					result.append(FEEDBACK_MATRIX['kbswingTip1'])
					result.append(FEEDBACK_MATRIX['kbswingTip2'])
				else:
					result.append(FEEDBACK_MATRIX['Goodkbswing'])




			else:

				result.append(FEEDBACK_MATRIX['UnknownExercise'])

			feedbackEntries.append(result)


		#print(feedbackEntries)

		return feedbackEntries








def feedback(request,video_name):

	#MEDIA_URL = SERVER_DATA + PROCESSED_VIDEOS_DIR 

	db_list = VideoEntry.objects.all()
	
	global username

	print(db_list)

	print(username)

	op_output_path = ''

	flist = []

	rlist = []

	reps = []

	repTips = []

	for i in db_list:

		if(i.videoUploaded==video_name and i.username == username):

			rep_list = i.rep.all()
			
			
			#print(len(rep_list))

			op_output_path = i.processedVideoPath

			print(i.repCount)

			#print(i)
			for j in rep_list:
				
				print(j.repNumber)
				reps.append(j.repNumber)

				print('\n\n Showing rep:' + str(j) +'\n\n\n')

				tip_list = j.feedback.all()

				res = []
				for tip in tip_list:
					res.append(tip.feedback)
				repTips.append(res)	

				


				
	


	return render(request,'upload/feedback.html',{ 'repTips':repTips ,'reps': reps ,'rlist':rlist,'video_name':video_name , 'op_output_path':op_output_path  , 'MEDIA_URL':MEDIA_URL} )




class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('upload:login')
    template_name = 'registration/signup.html'



