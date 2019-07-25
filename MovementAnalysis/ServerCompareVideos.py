

import processOutputs
import ServerReadOutput
import os,os.path
import sys
import numpy
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import math

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial



#import file
import json
import os

from numpy import dot
from numpy.linalg import norm
from scipy import spatial


MODEL_FOLDER = os.path.dirname(os.path.realpath(__file__))+'/models/'
SIMILARITY_TRESHOLD = 0.5




def checkReps(vid):

	print('AUTOCORR:\n\n')
	for key,val in vid.items():
		if(key=='plane'):
			continue
		print(key)
		print(processOutputs.autocorr(val))
		print('\n\n\n')

#array of directories
def compareVideos(featureDict):



	plane = featureDict['plane']

	results = {}

	foundMatch = False
	
	print('compareVideos:\n\n\n\n\n\n')

	#print(featureDict.keys())
	modelsCompared = 0
	vid = dict(featureDict)

	#checkReps(vid)
	#exit(0)

	maxMean = 0
	exercise = ''
	for i in os.listdir(MODEL_FOLDER): #iterate through movements

		
		directory=os.path.join(os.getcwd(),MODEL_FOLDER,i+'/',plane)


		print(directory)


		for j in os.listdir(directory): #iterate through planes inside a given movement
			
			if(foundMatch == True):
				break

			if(i == 'squat'):
				
				

				
				print('\n\n\n\n\n\n\n\n\n\nCOMPARING SQUATS\n\n')
				with open(os.path.join(directory,j)) as jsonFile:
					

					model = json.load(jsonFile)
					
					#plotFeatures(model,vid)


					similarity = compareFeatures(model,vid)
					
					
					if(evaluate_movement(similarity,plane)):
						

						
						print("SQUAT: foundMatch!!!")
						
						foundMatch = True

						results['exercise'] = i

						getFeedBack(featureDict,results,similarity)

						break
						
					else:
						
						continue
			
			


			elif(i=='kbswing'):
				
				

				print('\n\n\n\n\nCOMPARING KBSWINGS\n\n\n\n\n')
				with open(os.path.join(directory,j)) as jsonFile:
					

					model = json.load(jsonFile)
					#vid = dict(featureDict)
					similarity = compareFeatures(model,vid)


					minim = min( similarity, key = similarity.get)
					#plotFeatures(model,vid)

					if(evaluate_movement(similarity,plane)):


						
						print("\n\n\nKBSWING:foundMatch!!!\n\n\n\n")
						
						foundMatch = True

						results['exercise'] = i

						getFeedBack(featureDict,results,similarity)

						break
					
					else:
						
						continue



			else:
				continue #irrelevant folder 


			


	if(foundMatch==False):
		results['exercise'] = 'NOK'

	print(results)




	print('exercise:' + exercise)
	print(maxMean)



	return results




def evaluate_movement(similarity,plane):


	temp={}

	if(plane == 'left'):
		temp['lKneeAnkle'] = similarity['lKneeAnkle']
		temp['lHipKnee'] = similarity['lHipKnee']
		temp['lShoulderHip'] = similarity['lShoulderHip']
		minKey = min(temp,key=temp.get)
		if(temp[minKey] > 0 or minKey == 'lHipKnee'):
			return True
		else:
			return False

	elif(plane == 'right'):

		temp['rKneeAnkle'] = similarity['rKneeAnkle']
		temp['rHipKnee'] = similarity['rHipKnee']
		temp['rShoulderHip'] = similarity['rShoulderHip']
		minKey = min(temp,key=temp.get)
		if(temp[minKey] > 0 or minKey == 'rHipKnee'):
			return True
		else:
			return False

	else:#front plane


		temp['rKneeAnkle'] = similarity['rKneeAnkle']
		temp['rHipKnee'] = similarity['rHipKnee']
		temp['rShoulderHip'] = similarity['rShoulderHip']
		temp['lKneeAnkle'] = similarity['lKneeAnkle']
		temp['lHipKnee'] = similarity['lHipKnee']
		temp['lShoulderHip'] = similarity['lShoulderHip']

		minKey = min(temp,key=temp.get)


		if( (temp[minKey] > 0 or minKey == 'rHipKnee' or minKey == 'lHipKnee' ) and 
			(temp['lKneeAnkle'] > 0 and temp['rKneeAnkle'] > 0)  ):
			return True
		else:
			return False




def print_mean(similarity):


	temp = dict(similarity)
	items=0
	total = 0

	#temp.pop('lShoulderlElbow',0)
	#temp.pop('lElbowlWrist',0)
	#temp.pop('rElbowrWrist',0)
	#temp.pop('rShoulderrElbow',0)

	for key,val in temp.items():

		if(key != 'plane'):
			total += val
			items = items + 1
	print('\n\n\n\n MEAN: ' + str(total/items))
#similarity is a dictionary with the similarity values for each key
def compareFeatures(model,vid):

	#pop plane
	
	print(vid.keys())
	print(model.keys())

	#model.pop('plane')
	#vid.pop('plane')

	sim = {}

	for key,val in vid.items():

		if(key=='plane'):
			continue

		#check if key exists and is in the farther plane
		if(model.get(key,None) == None):
			print('Key '+key +'not found in model!\n')

			if(vid['plane'] == 'left'):
				if(key in ['rElbowrWrist','rShoulderrElbow','rShoulderHip','rHipKnee','rKneeAnkle']):
					continue
				else:
					continue
			elif(vid['plane'] == 'right'):
				if(key in ['lHipKnee','lElbowlWrist','lShoulderlElbow','lShoulderHip','lKneeAnkle']):
					continue
				else:
					continue
			


			continue
		

		#print('\nCOMPARING KEY' + key)
		sim[key] = getSimilarity(model[key],vid[key])

	
	#print('Similarity matrix: \n')
	#for key,val in sim.items():
	#	print(key + ':' + str(val))

	return sim	
		

			#print('\nCorrelation coefficient between videos ' + str(i) + 'and' + str(j) + ':	' + str(numpy.corrcoef(angleMatrix[i],angleMatrix[j])))

			#print('\nMinimum of CosineSimilarity between videos \n'+ str(i) + 'and' + str(j) + ':	' + str(min(sim)))
			#print('\nMaximum of CosineSimilarity between videos \n'+ str(i) + 'and' + str(j) + ':	' + str(max(sim)))


#the input is two numeric vectors to get the similarity
def getSimilarity(a,b):



	coef=numpy.corrcoef(a,b)

	print('COEF')
	print(coef)




	#cosSim = 1 - spatial.distance.cosine(a, b)




	#cosSim=cosine_similarity(a,b)

	#return cosSim[0][0]

	return coef[0][1]

 


#this function checks if both arms are elevated to a certain height by seeing if the angle between the shoulder and elbow goes above zero
# receives the uploaded video extracted features as argument
def get_mean(similarity):
	
	temp = dict(similarity)
	items=0
	total = 0

	for key,val in temp.items():

		if(key != 'plane'):
			total += val
			items = items + 1

	print('\n\n\nTOTAL_MEAN : ' + str(total/items))

	return total/items
	


#evaluates squat depth to check if there it can be identified as a squat
def get_min_squat_depth(vid):

	plane = vid.get('plane','error')

	print('\n\n\n')
	print(plane)

	print('\n\n\n MAX lHipKnee: ' + str(max(vid['lHipKnee'])))
	print('\n\n\n MAX rHipKnee: ' + str(max(vid['rHipKnee'])))
	print('\n\nMIN lHipKnee:'+str(min(vid['lHipKnee'])))
	print('\n\nMIN rHipKnee:'+str(min(vid['rHipKnee'])))
	
	if(plane=='error'):
		return False


	elif((plane == 'left') and ((max(vid['lHipKnee']) > 0 ) or min(vid['lHipKnee']) < MIN_SQUAT_DEPTH)):

		print('\n\n\n MAX lHipKnee: ' + str(max(vid['lHipKnee'])))
		print('\n\n\n MIN lHipKnee: ' + str(min(vid['lHipKnee'])))
		return True


	elif((plane == 'right') and ( max(vid['rHipKnee']) > 0 or min(vid['rHipKnee']) < MIN_SQUAT_DEPTH  )):
		return True


	elif((plane == 'front') and ( max(vid['lHipKnee']) > 0 or (min(vid['lHipKnee']) < MIN_SQUAT_DEPTH and max(vid['rHipKnee'])>FRONT_PLANE_RIGHT_MIN_DEPTH) )):

		print('\n\nMAX cHiprKnee:'+str(max(vid['cHiprKnee'])))
		print('\n\nMAX cHiplKnee:'+str(max(vid['cHiplKnee'])))
		print('\n\nMIN cHiplKnee:'+str(min(vid['cHiplKnee'])))
		print('\n\nMIN cHiprKnee:'+str(min(vid['cHiprKnee'])))
		return True
	else:
		return False






# vid -> dictionary containing the keypoint positions
# results -> a name reference to the dictionary with the results to give feedback to user
# i 
#
def getFeedBack(vid,results,similarity):
	

	if(results['exercise']=='squat'):
		
		squatRes = ServerReadOutput.checkSquat(vid,vid['plane'],results)

		#results['depth'] = squatRes['depth']


	if(results['exercise'] == 'kbswing'):

		kbRes = ServerReadOutput.checkKbSwing(similarity,results,vid['plane'],vid)
		

def plotFeatures(model,vid):

	for key in model.keys():
		


		if(key=='plane'):
			continue

		if(vid.get(key,None)==None):
			continue
			print('Key ' + key +' not found in video!\n\n')

		plt.figure()
		plt.title(key)
		plt.plot(model[key],label='model')
		plt.plot(vid[key],label='video')
		plt.legend()
		plt.xlabel('tNorm')
		plt.ylabel('Degrees')
		plt.show()
				


			
			
			
			

				
		

		
			
			



if __name__ == "__main__":
	
	print(sys.argv)
	compareVideos(ServerReadOutput.readOutputs(sys.argv[1]))