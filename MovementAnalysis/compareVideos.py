

import processOutputs
import ReadOutput
import os,os.path
import sys
import numpy
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import math

from sklearn.feature_extraction.text import TfidfVectorizer



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
		
		[vidAngle,vidPos]= ReadOutput.readOutputs(i)

		plane = processOutputs.getPlane(vidPos)
		

		angleMatrix.append(vidAngle)
		validMatrix.append(ReadOutput.checkSquat(vidAngle,ReadOutput.getExtractedFeatures(),plane))

	
	

	
	features=ReadOutput.getExtractedFeatures()
	
	plotAngles(angleMatrix,args,features)
	compareAngles(angleMatrix,features,validMatrix)
	print(validMatrix)

def compareAngles(angleMatrix,features,results):

	

	for i,elem in enumerate(angleMatrix):
		

		for j in xrange(i+1,len(angleMatrix)):

			sim = getSimilarity(angleMatrix[i],angleMatrix[j])

			#print('\nVid' + str(i) + 'and' + str(j) + ':	\n'),
			#print('Valid Squat:'+ str(results[i])+','+str(results[j])),
			#print(features),
			#print('\n'+str(sim))

		
		

			#print('\nCorrelation coefficient between videos ' + str(i) + 'and' + str(j) + ':	' + str(numpy.corrcoef(angleMatrix[i],angleMatrix[j])))

			#print('\nMinimum of CosineSimilarity between videos \n'+ str(i) + 'and' + str(j) + ':	' + str(min(sim)))
			#print('\nMaximum of CosineSimilarity between videos \n'+ str(i) + 'and' + str(j) + ':	' + str(max(sim)))

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