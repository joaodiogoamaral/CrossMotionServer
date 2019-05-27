

import processOutputs
import ServerReadOutput
import os,os.path
import sys
import numpy
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import math

from sklearn.feature_extraction.text import TfidfVectorizer



#import file
import json
import os

from numpy import dot
from numpy.linalg import norm
from scipy import spatial


MODEL_FOLDER = os.path.dirname(os.path.realpath(__file__))+'/models/'
SIMILARITY_TRESHOLD = 0.5

#array of directories
def compareVideos(featureDict):



	plane = featureDict['plane']

	results = {}

	foundMatch = False
	
	print('compareVideos:\n\n\n\n\n\n')

	#print(featureDict.keys())

	for i in os.listdir(MODEL_FOLDER): #iterate through movements

		
		directory=os.path.join(os.getcwd(),MODEL_FOLDER,i+'/',plane)


		print(directory)


		for j in os.listdir(directory): #iterate through planes inside a given movement
			
			
			
			with open(os.path.join(directory,j)) as jsonFile:
				

				model = json.load(jsonFile)
				vid = dict(featureDict)
				similarity = compareFeatures(model,vid)

				if(min( similarity, key = similarity.get) > SIMILARITY_TRESHOLD):
					
					#print("foundMatch!!!")
					
					foundMatch = True

					results['exercise'] = i

					getFeedBack(featureDict,results,similarity)

					break
				
				else:
					
					continue
		
		if(foundMatch == True):
			break

	if(foundMatch==False):
		results['exercise'] = 'NOK'

	print(results)

	return results

	

	

def compareFeatures(model,vid):

	#pop plane
	
	print(vid.keys())
	print(model.keys())

	model.pop('plane')
	vid.pop('plane')

	sim = {}

	for key,val in vid.items():

		#print('Comparing key -- ' + key )
		sim[key] = getSimilarity([model[key]],[vid[key]])

	
	print('Similarity matrix: \n')
	print(sim)

	return sim	
		

			#print('\nCorrelation coefficient between videos ' + str(i) + 'and' + str(j) + ':	' + str(numpy.corrcoef(angleMatrix[i],angleMatrix[j])))

			#print('\nMinimum of CosineSimilarity between videos \n'+ str(i) + 'and' + str(j) + ':	' + str(min(sim)))
			#print('\nMaximum of CosineSimilarity between videos \n'+ str(i) + 'and' + str(j) + ':	' + str(max(sim)))


#the input is two numeric vectors to get the similarity
def getSimilarity(a,b):

	cosSim=cosine_similarity(a,b)

	


	return cosSim[0][0]


# vid -> dictionary containing the keypoint positions
# results -> a name reference to the dictionary with the results to give feedback to user
# i 
#
def getFeedBack(vid,results,similarity):
	

	if(results['exercise']=='squat'):
		
		squatRes = ServerReadOutput.checkSquat(vid,vid['plane'],results)

		#results['depth'] = squatRes['depth']

		



			







if __name__ == "__main__":
	
	print(sys.argv)
	compareVideos(ServerReadOutput.readOutputs(sys.argv[1]))