
#includes

from scipy.interpolate import interpolate,interp1d,splev,splrep,CubicSpline
import matplotlib.pyplot as plt
import numpy as np
import peakutils as pk 
import scipy
import peakutils

CONFIDENCE_THRESHOLD = 0.5
INTERPOLATION_ORDER = 10

N_PTS = 10000 #Number of points for time vectors


def autocorr(x):

	print('AUTOCORR')
	y = np.correlate(x-np.mean(x), x-np.mean(x), mode='full')
	print(y)
	indices = peakutils.indexes(y)

	print(indices)


	print(len(indices)/2)
	#result = peaks(np.correlate(x, x, mode='full'))

	return len(indices)/2 - 1
    #return result[result.size/2:]



# this functions extracts items (tuples) from the dictionary entries when the respective confidence is below a treshold.
# Besides, if a certain tupple contains an empty value, delete it too

def getCoherentMatrix(keypointMatrix):
		#this loop discards frames where the keypoint could not be identified with a certain confidence
	for i in keypointMatrix.keys():
		keypointMatrix[i] = [x for x in keypointMatrix[i] if checkFrameConfidenceOk(x)]


	return keypointMatrix

def checkFrameConfidenceOk(keypointFrame):
	
	if(keypointFrame[2]<CONFIDENCE_THRESHOLD):
		return False
	return True




#function that extracts the plane from which the video was filmed
#returns a string: "front", "lSide", "rSide", "error" , the last one for cases where the  
def getPlane(keypointMatrix):
	
	

	if( len(keypointMatrix['lEar']) > 0 and len(keypointMatrix['rEar']) > 0):
		
		print(len(keypointMatrix['rEar']) )

		if(len(keypointMatrix['nose'])!=0):
			return "front"
		else:
			return "back"

	elif  len(keypointMatrix['lEar']) > 0:
		return "left"
	elif len(keypointMatrix['rEar']) > 0:
		return "right"
	else:
		return "error"





	return False;



	

def normalize(vector):




	time = np.linspace(0,len(vector),num=N_PTS)
	#print(len(time))
	tInt = np.linspace(0,len(vector),num=len(vector))
		#xrange(len(vector))

	#print(tInt)
	#using polyfit
	#Coeffs = np.poly1d(np.polyfit(tInt,vector,INTERPOLATION_ORDER))
	#Coeffs=np.poly1d(vector)
	#return Coeffs(time)

	#using splines
	#Coeffs = splrep(tInt,vector,s=50,k=3)

	#return splev(time,Coeffs,der=0)

	Coeffs = interp1d(tInt,vector)
	return Coeffs(time)

	
#input to this function is a list of tupples for a certain keypoint
def extractEquationsNorm(keypointPositions):
	


	#debug info
	print('length of Positions Vector for interpolation:'+ str(len(keypointPositions)))
	

	time = np.linspace(0,len(keypointPositions),N_PTS)
	tInt = xrange(len(keypointPositions)) #time vector for interpolation
	intOrder = INTERPOLATION_ORDER
	y = []
	x = []
	for i in keypointPositions:
		
		y.append(i[1])
		x.append(i[0])

	print('\n\n\n')	

	while True:
		
		try:    
			yCoeffs = np.poly1d(np.polyfit(tInt,y,intOrder))
			xCoeffs = np.poly1d(np.polyfit(tInt,x,intOrder))
			break	
		except np.RankWarning:
			intOrder=intOrder-1
			continue
	#print(intOrder)


	return [xCoeffs(time),yCoeffs(time),time]



#this function receives a vector with the angles between two certain keypoints 
# and normalizes it to N_POINTS
def normalizeAngles(angles):

	tInt = xrange(len(angles))
	time = np.linspace(0,len(angles),N_PTS)
	intOrder = INTERPOLATION_ORDER

	while True:
		try:    
			angleCoeff = np.poly1d(np.polyfit(tInt,angles,intOrder))

			break	
		except np.RankWarning:
			intOrder=intOrder-1
			continue
		print(intOrder)

	return angleCoeff(time)











