

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


from processOutputs import N_PTS


#import file
import json
import os

from numpy import dot
from numpy.linalg import norm
from scipy import spatial
import storeModel


MODEL_FOLDER = os.path.dirname(os.path.realpath(__file__))+'/models/'
SIMILARITY_TRESHOLD = 0.5




def checkReps(rawFeatures,featureDict):

	print('\n\n\n\n\nCheckREPS')

	result = []



	for key,val in featureDict.items():
		if(key == 'plane'):
			continue
		print('KEY:' + key)
		#print(processOutputs.autocorr(val))
	
	for key,val in featureDict.items():




		if(key=='plane'):
			continue
		
		print('LENGTH:' + str(len(val)) + '\n\n\n\n\n')	
    
    	
    # Some other interpolation based on neighboring points might be better.
    # Spline, cubic, whatever
	key2analyze = ''
	if(featureDict['plane'] == 'right' or featureDict['plane'] == 'front'):
		key2analyze='rHipKnee'
	else:
		key2analyze='lHipKnee'
		

	nReps = processOutputs.autocorr(featureDict[key2analyze])



	if(len(nReps) == 0 ):
		result.append(featureDict)
		return result

	print('NREPS: ' + str(nReps))

	foundMatch = False


	
	repStart = 0
	
	for idx in xrange(0,len(nReps)+1):


		print('\n\nREPNO:' + str(idx)+ '\n\n\n\n')

		rep2Compare = {} # empty dict

		for key,val in featureDict.items():


			print('REPSTART='+str(repStart)+'\n')

			if(key == 'plane'):
				rep2Compare['plane'] = val 
				continue
			print('KEY: ' + key + str(len(val)))

			#print(len(val[repStarts[idx]:repStarts[idx+1]]))


			if(idx < (len(nReps))):
				rep2Compare[key] = processOutputs.normalize(val[repStart:nReps[idx]])
			else:
				rep2Compare[key] = processOutputs.normalize(val[repStart:])


			
			print(len(rep2Compare[key]))
			#ServerReadOutput.plotRawData(rep2Compare[key])
		if(idx < len(nReps)):
			repStart = nReps[idx]	
			




		result.append(rep2Compare)



	return result

		
		
			






#array of directories
def compareVideos(rawFeatureDict,featureDict):

	


	reps = checkReps(rawFeatureDict,featureDict)

	if(len(reps) == 0):
		
		return []
	
	ret = []

	plane = featureDict['plane']



	for rep in reps:

		vid = dict(rep)
	

		results = {}




		foundMatch = False
	


		print('compareVideos:\n\n')

		#print(featureDict.keys())
		modelsCompared = 0
	

		#checkReps(vid)
		#exit(0)

		maxMean = 0
		exercise = ''
		for i in os.listdir(MODEL_FOLDER): #iterate through movements

		
			directory=os.path.join(os.getcwd(),MODEL_FOLDER,i+'/',plane)


			print(directory)


			if(foundMatch == True):
				break


			for j in os.listdir(directory): #iterate through models inside a given movement
			
				
				if(i == 'squat'):
				
				

				
					print('\n\nCOMPARING SQUATS\n\n')
					with open(os.path.join(directory,j)) as jsonFile:
					

						model = json.load(jsonFile)
					
					#plotFeatures(model,vid)


						similarity = compareFeatures(model,vid)
					
					
						if(evaluate_squat(similarity,plane)):
						

						
							print("SQUAT: foundMatch!!!"+ j)
						
							foundMatch = True

							results['exercise'] = i

							returnStat= getFeedBack(rep,results,similarity)


							break
						
						else:
						
							continue
			
			


				elif(i=='kbswing'):
				
				

					print('\n\nCOMPARING KBSWINGS\n\n')
					with open(os.path.join(directory,j)) as jsonFile:
					

						model = json.load(jsonFile)
					#vid = dict(featureDict)
						similarity = compareFeatures(model,vid)


						minim = min( similarity, key = similarity.get)
					#plotFeatures(model,vid)

						if(evaluate_kb(similarity,plane)):



							print("KB: foundMatch!!!"+ j)

							results['exercise'] = i
						
						
							foundMatch = True

						

							getFeedBack(rep,results,similarity)

							#if(results['depth'] == 'OK'):
							#	storeModel.storeMovement()


							break
					
						else:
						
							continue



				else:
					continue #irrelevant folder 


			


		if(foundMatch==False):
			results['exercise'] = 'NOK'

		

		ret.append(results)


	#print('exercise:' + exercise)
	#print(maxMean)


	print('NREPS BEFORE COMPARISON:' +  str(len(reps)))

	return ret




def evaluate_squat(similarity,plane):


	temp={}

	if(plane == 'left'):
		temp['lKneeAnkle'] = similarity['lKneeAnkle']
		temp['lHipKnee'] = similarity['lHipKnee']
		temp['lShoulderHip'] = similarity['lShoulderHip']
		temp['lShoulderlElbow'] = similarity['lShoulderlElbow']
		minKey = min(temp,key=temp.get)
		if(temp['lKneeAnkle'] > 0.6 and temp['lShoulderHip'] > 0.6 and temp[minKey] > -0.4 ):
			return True
		else:
			return False

	elif(plane == 'right'):

		temp['rKneeAnkle'] = similarity['rKneeAnkle']
		temp['rHipKnee'] = similarity['rHipKnee']
		temp['rShoulderHip'] = similarity['rShoulderHip']
		minKey = min(temp,key=temp.get)
		if(temp['rKneeAnkle'] > 0.6 and temp['rShoulderHip'] > 0.6 and temp['rHipKnee'] > -0.4):
			return True
		else:
			return False

	else:#front plane


		temp['rKneeAnkle'] = similarity['rKneeAnkle']
		temp['rHipKnee'] = similarity['rHipKnee']
		
		temp['lKneeAnkle'] = similarity['lKneeAnkle']
		temp['lHipKnee'] = similarity['lHipKnee']
		temp['cHiprKnee'] = similarity['cHiprKnee']
		temp['cHiplKnee'] = similarity['cHiplKnee']
		minKey = min(temp,key=temp.get)

		print(temp)


		if(	temp['lKneeAnkle'] > 0.6 and temp['rKneeAnkle'] > 0.6 and temp['rHipKnee'] > 0.6 ):
			return True
		else:
			return False




def evaluate_kb(similarity,plane):


	temp={}

	if(plane == 'left'):
		temp['lKneeAnkle'] = similarity['lKneeAnkle']
		temp['lHipKnee'] = similarity['lHipKnee']
		#temp['lShoulderHip'] = similarity['lShoulderHip']
		minKey = min(temp,key=temp.get)
		if(temp[minKey] > 0.5):
			return True
		else:
			return False

	elif(plane == 'right'):

		temp['rKneeAnkle'] = similarity['rKneeAnkle']
		temp['rHipKnee'] = similarity['rHipKnee']
		#temp['rShoulderHip'] = similarity['rShoulderHip']
		minKey = min(temp,key=temp.get)
		if(temp[minKey] > 0.5 ):
			return True
		else:
			return False

	else:#front plane


		temp['rKneeAnkle'] = similarity['rKneeAnkle']
		
		temp['lKneeAnkle'] = similarity['lKneeAnkle']
		temp['lHipKnee'] = similarity['lHipKnee']
		temp['rHipKnee'] = similarity['rHipKnee']

		
		#temp['cHiplKnee'] = similarity['cHiplKnee']

		minKey = min(temp,key=temp.get)


		if( temp[minKey] > 0.5):
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
	
	#print(vid.keys())
	#print(model.keys())
	


	#model.pop('plane')
	#vid.pop('plane')

	sim = {}

	for key,val in vid.items():

		if(key=='plane'):
			continue

		#check if key exists and is in the farther plane
		if(model.get(key,None) == None):
			#print('Key '+key +'not found in model!\n')

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
		#print(sim[key])
		
	#print('Similarity matrix: \n')
	#for key,val in sim.items():

	#	if(key == 'lKneeAnkle' or key == 'rKneeAnkle' or key == 'lHipKnee' or key == 'rHipKnee'):
	#		print('---------------------------------------------')
	#		print(key + '	|	' + str(val))
	#		print('---------------------------------------------')
	return sim	
		

			#print('\nCorrelation coefficient between videos ' + str(i) + 'and' + str(j) + ':	' + str(numpy.corrcoef(angleMatrix[i],angleMatrix[j])))

			#print('\nMinimum of CosineSimilarity between videos \n'+ str(i) + 'and' + str(j) + ':	' + str(min(sim)))
			#print('\nMaximum of CosineSimilarity between videos \n'+ str(i) + 'and' + str(j) + ':	' + str(max(sim)))


#the input is two numeric vectors to get the similarity
def getSimilarity(a,b):



	coef=numpy.corrcoef(a,b)

	#print('COEF')
	#print(coef)




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

		#if(squatRes['depth'] == 'OK' and squatRes.get('spine',None) == 'OK'):
			#print("Storing")
			#print(squatRes)
			#storeModel.storeMovement(vid,'squat')

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

	#[rawFeatures,features] = ServerReadOutput.readOutputs(sys.argv[1])

	#print(rawFeatures)


	#compareVideos(rawFeatures,features)

	
