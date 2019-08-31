

import processOutputs
import ReadOutput
import ServerReadOutput
import ServerCompareVideos
import os,os.path,json
import sys
import numpy
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import math

from sklearn.feature_extraction.text import TfidfVectorizer


from ServerCompareVideos import MODEL_FOLDER
from numpy import dot
from numpy.linalg import norm
from scipy import spatial
#array of directories
def compareVideos(args):

	planes = []
	vidMatrix = []
	angleMatrix = []
	validMatrix = []

	for i in args:

		#print(i)
		
		[rawFt,normFeat]= ServerReadOutput.readOutputs(i)

		angleMatrix.append(normFeat)
		

		
	#plotAngles(angleMatrix,args,features)
	compareWithModels(normFeat)
	#print(validMatrix)

def compareWithModels(normFeat):


	maxVals = {
		'lHipKnee' : -1 ,
		'rHipKnee' : -1 ,
		'lKneeAnkle' : -1,
		'rKneeAnkle' : -1
	}
	minVals = {
		'lHipKnee' : 1 ,
		'rHipKnee' : 1 ,
		'lKneeAnkle' : 1,
		'rKneeAnkle' : 1
	}

	plane=normFeat['plane']

	vid=dict(normFeat)

	for i in os.listdir(MODEL_FOLDER): #iterate through movements

		
			directory=os.path.join(os.getcwd(),MODEL_FOLDER,i+'/',plane)


			for j in os.listdir(directory): #iterate through models inside a given movement
			
				
				if(i == 'squat'):
				
				

				
					#print('\n\nCOMPARING SQUATS\n\n')
					with open(os.path.join(directory,j)) as jsonFile:
					

						model = json.load(jsonFile)
					
					#plotFeatures(model,vid)


						similarity = ServerCompareVideos.compareFeatures(model,vid)
					
						for key,val in maxVals.items():

							if(similarity.get(key,None)!= None):

								if(similarity[key]>maxVals[key]):
									maxVals[key]=similarity[key]

								if(similarity[key]<minVals[key]):
									minVals[key]=similarity[key]

						#print(similarity)
			


				elif(i=='kbswing'):
				
				

					
					with open(os.path.join(directory,j)) as jsonFile:
					

						model = json.load(jsonFile)
					#vid = dict(featureDict)
						similarity = ServerCompareVideos.compareFeatures(model,vid)

						for key,val in maxVals.items():

							if(similarity.get(key,None)!= None):

								if(similarity[key]>maxVals[key]):
									maxVals[key]=similarity[key]

								if(similarity[key]<minVals[key]):
									minVals[key]=similarity[key]

						#print(similarity)
					#plotFeatures(model,vid)

						



				else:
					continue #irrelevant folder 


		

			print('\n\nCOMPARING' + i +'\n\n')
			print('KEY     |    MIN     |     MAX     |' )
			for key,val in maxVals.items():

				print('-----------------------------------------')
				print(key + '  |    ' +str(minVals[key]))+'    |     '+str(maxVals[key])
				print('-----------------------------------------')
				minVals[key] = 1
				maxVals[key] = -1

def plotAngles(angles,titles,features):

	
	
	
	
	
	
	for j,feature in enumerate(angles[0]):
	
		plt.figure(1)
		plt.title(features[j])
		for i,vid in enumerate(angles):
		
			plt.plot(vid[j],label=titles[i])
		
		plt.legend()		
		plt.show()
			
		

		
		
		

		

		






#the input is two numeric vectors to get the similarity
def getSimilarity(a,b):

	#print(len(x1))
	#print(len(x2))
	#if(len(x1) > len (x2)):
	#	a=numpy.pad(x2,(0,len(x1)-len(x2)),'constant') 
	#	b=x1
	#else:
	#	a=x2
	#	b=numpy.pad(x1,(0,len(x2)-len(x1)),'constant') 
	
	#a = numpy.array(a)
	#b = numpy.array(b)
	#cosSim = dot(a, b)/(norm(a)*norm(b)) 
	
	#print(cosine_similarity([a[0]],[b[0]]))
	#print(cosine_similarity([a[0]],[b[1]]))
	#print(cosine_similarity([a[1]],[b[0]]))
	#print(cosine_similarity([a[1]],[b[1]]))



	cosSim=cosine_similarity(a,b)



	return numpy.diagonal(cosSim)


def getSimilarityMatrix(keypointMatrix):


	for i in xrange(len(keypointMatrix)):
		if(i<len(keypointMatrix)):
			for x in xrange(i+1,len(keypointMatrix)):
				print('Vertical similarity between videos '+str(i+1)+' and '+str(x+1)+':'+str(getSimilarity(keypointMatrix[i][1],keypointMatrix[x][1])))
				print('Horizontal similarity between videos '+str(i+1)+' and '+str(x+1)+':'+str(getSimilarity(keypointMatrix[i][0],keypointMatrix[x][0])))
				correlationY=numpy.correlate(keypointMatrix[i][1],keypointMatrix[x][1])
				print('correlation matrix')
				print(correlationY)

#inputs for this function are the keypoint positions (array of nVideos size in format [x,y,t]) of a certain joint and the title for the graph
def plotMovements(keypoint,keypointName):

	plt.figure(1)
	plt.title(keypointName+'Y positions')
	#first plot y position
	for idx,i in enumerate(keypoint):
		plt.plot(i[2],i[1],label='video'+str(idx))
	plt.legend()
	plt.show()	
	plt.clf()


	#plot x position
	plt.title(keypointName+'X positions')
	for idx,i in enumerate(keypoint):
		plt.plot(i[2],i[0],label='video'+str(idx))
	plt.legend()
	plt.show()	




	





if __name__ == "__main__":
	
	print(sys.argv)
	compareVideos([sys.argv[x] for x,value in enumerate(sys.argv) if x > 0 ])