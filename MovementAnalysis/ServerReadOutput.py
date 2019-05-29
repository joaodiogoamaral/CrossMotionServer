


import json
import os
import sys
import numpy
import processOutputs 
import math
import matplotlib.pyplot as plt
import storeModel



n2DKeypoints = 25
CONFIDENCE_THRESHOLD = 0.3
MAX_SPINE_ANGLE = -30
AMP=1000
extractedFeatures = []
validSquat = False


#outputDir = sys.argv[1]




#xCords = []
#yCords = []
#conf = []
#for loop to iterate through each json file in the directory
#input is the name of the folder from which the results should be read from
def readOutputs(outputDir):



	#pose keypoints2D are in format (x,y,c) with c being the confidence degree



	#initialize a matrix to contain all the frames
	#keypointMatrix = []

		# Result for BODY_25 (25 body parts consisting of COCO + foot)
		# const std::map<unsigned int, std::string> POSE_BODY_25_BODY_PARTS {
		#     {0,  "Nose"},
		#     {1,  "Neck"},
		#     {2,  "RShoulder"},
		#     {3,  "RElbow"},
		#    {4,  "RWrist"},
		#     {5,  "LShoulder"},
		#     {6,  "LElbow"},
		#     {7,  "LWrist"},
		#     {8,  "MidHip"},
		#     {9,  "RHip"},
		#     {10, "RKnee"},
		#     {11, "RAnkle"},
		#     {12, "LHip"},
		#     {13, "LKnee"},
		#     {14, "LAnkle"},
		#     {15, "REye"},
		#     {16, "LEye"},
		#     {17, "REar"},
		#     {18, "LEar"},
		#     {19, "LBigToe"},
		#     {20, "LSmallToe"},
		#     {21, "LHeel"},
		#     {22, "RBigToe"},
		#     {23, "RSmallToe"},
		#     {24, "RHeel"},
		#     {25, "Background"}

		#     {25, "Background"}

	keypointMatrix = {
	'nose':[],
	'neck':[],
	'rShoulder' : [],
	'rElbow' : [],
	'rWrist' : [],
	'lShoulder' : [],
	'lElbow' : [],
	'lWrist' : [],
	'midHip' : [],
	'rHip' : [],
	'rKnee' : [],
	'rAnkle' : [],
	'lHip' : [],
	'lKnee' : [],
	'lAnkle' : [],
	'rEye' : [],
	'lEye' : [],
	'rEar' : [],
	'lEar' : [],
	'lBigToe': [],
	'lSmallToe' : [],
	'lHeel' : [],
	'rBigToe' : [],
	'rRSmallToe': [],
	'RHeel' : []}


	#
	


	print(outputDir)
	jsonFiles = [posJson for posJson in os.listdir(outputDir) if posJson.endswith('.json')]

	print('\nNumber of frames in video:'+str(len(jsonFiles))+'\n')


	jsonFiles.sort()

	for idx,js in enumerate(jsonFiles) :
		with open(os.path.join(outputDir,js)) as jsonFrame:
			jsonContent = json.load(jsonFrame)

			if len(jsonContent['people'])==0:
				print('\nFrame' + str(idx) +'discarded \n')
				continue

		
			keypoints = jsonContent['people'][0]['pose_keypoints_2d']
			xCords=keypoints[0:len(keypoints):3]
			yCords=keypoints[1:len(keypoints):3]
			conf=keypoints[2:len(keypoints):3]

			keypointMatrix['nose'].append((xCords[0],yCords[0],conf[0]))
			keypointMatrix['neck'].append((xCords[1],yCords[1],conf[1]))
			keypointMatrix['rShoulder'].append((xCords[2],yCords[2],conf[2]))
			keypointMatrix['rElbow'].append((xCords[3],yCords[3],conf[3]))
			keypointMatrix['rWrist'].append((xCords[4],yCords[4],conf[4]))
			keypointMatrix['lShoulder'].append((xCords[5],yCords[5],conf[5]))
			keypointMatrix['lElbow'].append((xCords[6],yCords[6],conf[6]))
			keypointMatrix['lWrist'].append((xCords[7],yCords[7],conf[7]))
			keypointMatrix['midHip'].append((xCords[8],yCords[8],conf[8]))
			keypointMatrix['rHip'].append((xCords[9],yCords[9],conf[9]))
			keypointMatrix['rKnee'].append((xCords[10],yCords[10],conf[10]))
			keypointMatrix['rAnkle'].append((xCords[11],yCords[11],conf[11]))
			keypointMatrix['lHip'].append((xCords[12],yCords[12],conf[12]))
			keypointMatrix['lKnee'].append((xCords[13],yCords[13],conf[13]))
			keypointMatrix['lAnkle'].append((xCords[14],yCords[14],conf[14]))
			keypointMatrix['rEye'].append((xCords[15],yCords[15],conf[15]))
			keypointMatrix['lEye'].append((xCords[16],yCords[16],conf[16]))
			keypointMatrix['rEar'].append((xCords[17],yCords[17],conf[17]))
			keypointMatrix['lEar'].append((xCords[18],yCords[18],conf[18]))
			keypointMatrix['lBigToe'].append((xCords[19],yCords[19],conf[19]))
			keypointMatrix['lSmallToe'].append((xCords[20],yCords[20],conf[20]))
			keypointMatrix['lHeel'].append((xCords[21],yCords[21],conf[21]))
			keypointMatrix['rBigToe'].append((xCords[22],yCords[22],conf[22]))
			keypointMatrix['rRSmallToe'].append((xCords[23],yCords[23],conf[23]))
			keypointMatrix['RHeel'].append((xCords[24],yCords[24],conf[24]))

	
	angles = getFeatures(processOutputs.getCoherentMatrix(keypointMatrix))		
	#plotRawData(keypointMatrix['lHip'][1],keypointMatrix['lKnee'][1])		
			
	
	return angles
	#processOutputs.processOutputs(keypointMatrix)

def checkSquat(features,plane,results):

	

	if(plane == 'left'):

		#CHECK SQUAT DEPTH

		if(max(features['lHipKnee'])>0):

			results['depth'] = 'OK'
		else:
			results['depth'] = 'NOK'


		#CHECK BACK ALIGNMENT

		if(max(features['lShoulderHip'])<MAX_SPINE_ANGLE):
			
			results['spine'] = 'OK'
		
		else:

			results['spine'] = 'NOK'
		

	elif(plane == 'right'):


		print('MAX ANGLE HIP:' + str(max(features['rHipKnee'])))
		
		if(max(features['rHipKnee'])>0):

			results['depth'] = 'OK'
		else:
			results['depth'] = 'NOK'


		if(max(features['rShoulderHip'])<MAX_SPINE_ANGLE):
			
			results['spine'] = 'OK'
		
		else:

			results['spine'] = 'NOK'


	else: #front plane

		if(max(features['cHiplKnee'])>0 and max(features['cHiprKnee'])>0):

			results['depth'] = 'OK'
		
		elif(max(features['cHiplKnee'])>0 or max(features['cHiprKnee'])>0):

			results['depth'] = 'NOK'
			results['simetry'] = 'NOK'
		
		else:
			
			results['depth'] = 'NOK'	



	return results
	
	

#this function returns a matrix with the relevant angles to infer pose
def getFeatures(keypointMatrix):


		plane = processOutputs.getPlane(keypointMatrix)
		#print(plane)

		normalizedFeatures = {}
		features = {


			'lHipKnee' : [],
			'lKneeAnkle' : [],
			
			'rHipKnee' : [],
			'rKneeAnkle' : [],


			'rShoulderHip' : [],
			'lShoulderHip' : [],
			

			#front plane specific features

			'cHiplKnee' : [],
			'cHiprKnee' : [],

			'lKneelAnkle' : [],
			'rKneerAnkle' : [],

			'cHiplShoulder' : [],
			'cHiprShoulder' : [],


			#kbSwingSpecificFeatures 

			'rElbowrWrist' : [],
			'lElbowlWrist' : [],
			'lShoulderlElbow' : [],
			'rShoulderrElbow' : [],
			'lShoulderWrist' : []

		}

		#print(keypointMatrix['lKnee'])
		#print('\n\n\n\n')
		#print(keypointMatrix['lHip'])

		if(plane == 'left'):

			#NOTE: Usually inverted X for left plane

			features['lHipKnee'] = [getAngle(-keypointMatrix['lHip'][i][0],-keypointMatrix['lKnee'][i][0],keypointMatrix['lHip'][i][1],keypointMatrix['lKnee'][i][1]) for i in xrange(0,min(len(keypointMatrix['lKnee']),len(keypointMatrix['lHip'])))]


			features['lKneeAnkle'] = [getAngle(-keypointMatrix['lKnee'][i][0],-keypointMatrix['lAnkle'][i][0],keypointMatrix['lKnee'][i][1],keypointMatrix['lAnkle'][i][1]) for i in xrange(0,min(len(keypointMatrix['lKnee']),len(keypointMatrix['lAnkle'])))]

			features['lShoulderHip'] = [getAngle(-keypointMatrix['lShoulder'][i][0],-keypointMatrix['lHip'][i][0],keypointMatrix['lShoulder'][i][1],keypointMatrix['lHip'][i][1]) for i in xrange(0,min(len(keypointMatrix['lShoulder']),len(keypointMatrix['lHip'])))]


			#KB Swing specific features (not inverted in the X Axis)
			features['lShoulderlElbow'] = [getAngle(keypointMatrix['lShoulder'][i][0],keypointMatrix['lElbow'][i][0],keypointMatrix['lShoulder'][i][1],keypointMatrix['lElbow'][i][0]) for i in xrange(0,min(len(keypointMatrix['lElbow']),len(keypointMatrix['lShoulder'])))]

			features['lElbowlWrist'] = [getAngle(keypointMatrix['lElbow'][i][0],keypointMatrix['lWrist'][i][0],keypointMatrix['lElbow'][i][1],keypointMatrix['lWrist'][i][0]) for i in xrange(0,min(len(keypointMatrix['lWrist']),len(keypointMatrix['lElbow'])))]

			features['lShoulderWrist'] = [getAngle(keypointMatrix['lShoulder'][i][0],keypointMatrix['lWrist'][i][0],keypointMatrix['lShoulder'][i][1],keypointMatrix['lWrist'][i][0]) for i in xrange(0,min(len(keypointMatrix['lShoulder']),len(keypointMatrix['lWrist'])))]

		elif(plane == 'right'):
			

			#comprehensions

			features['rHipKnee'] = [getAngle(keypointMatrix['rHip'][i][0],keypointMatrix['rKnee'][i][0],keypointMatrix['rHip'][i][1],keypointMatrix['rKnee'][i][1]) for i in xrange(0,min(len(keypointMatrix['rKnee']),len(keypointMatrix['rHip'])))]


			features['rKneeAnkle'] = [getAngle(keypointMatrix['rKnee'][i][0],keypointMatrix['rAnkle'][i][0],keypointMatrix['rKnee'][i][1],keypointMatrix['rAnkle'][i][1]) for i in xrange(0,min(len(keypointMatrix['rKnee']),len(keypointMatrix['rAnkle'])))]

			features['rShoulderHip'] = [getAngle(keypointMatrix['rShoulder'][i][0],keypointMatrix['rHip'][i][0],keypointMatrix['rShoulder'][i][1],keypointMatrix['rHip'][i][1]) for i in xrange(0,min(len(keypointMatrix['rShoulder']),len(keypointMatrix['rHip'])))]

			features['rShoulderrElbow'] = [getAngle(keypointMatrix['rShoulder'][i][0],keypointMatrix['rElbow'][i][0],keypointMatrix['rShoulder'][i][1],keypointMatrix['rElbow'][i][0]) for i in xrange(0,min(len(keypointMatrix['rShoulder']),len(keypointMatrix['rElbow'])))]

			features['rElbowrWrist'] = [getAngle(keypointMatrix['rElbow'][i][0],keypointMatrix['rWrist'][i][0],keypointMatrix['rElbow'][i][1],keypointMatrix['rWrist'][i][0]) for i in xrange(0,min(len(keypointMatrix['rElbow']),len(keypointMatrix['rWrist'])))]

			



		elif(plane == 'front'):
			
			for i,elem in enumerate(keypointMatrix['rKnee']):

				features['cHiplKnee'].append(getAngle(keypointMatrix['midHip'][i][0],keypointMatrix['lKnee'][i][0],keypointMatrix['midHip'][i][1],keypointMatrix['lKnee'][i][1]))
				
				features['cHiprKnee'].append(getAngle(keypointMatrix['midHip'][i][0],keypointMatrix['rKnee'][i][0],keypointMatrix['midHip'][i][1],keypointMatrix['rKnee'][i][1]))


	
		for key,i in features.items():
			
			if(len(i)==0):
				print('\npopping:',key)
				#print(key)
				features.pop(key);
				#normalizedFeatures.pop(key)
			else:
				print(key)
				#normalizedFeatures.append(processOutputs.normalize(i))
				
				#normalizedFeatures[key] = processOutputs.normalize(i)
				normalizedFeatures[key] = processOutputs.normalize(i).tolist()
				
				continue	

		
			
		

		
		
		normalizedFeatures['plane'] = plane
		

		print('readOutputs \n\n\n\n\n\n\n\n\n\n\n')
		print(normalizedFeatures.keys())


		return normalizedFeatures


def getDist(x1,x2):



	return (x1-x2)*AMP



#this function returns the anle of the vector connecting the two points 
def getAngle(x1,x2,y1,y2):

	#print('\nx1:'+str(x1)+'\nx2:'+str(x2)+'\ny1:'+str(y1)+)

	x=(x1-x2)


	y=(y1-y2)

	angle = math.degrees(math.atan2(y,x))


	#angle=angle+360
	#angle = math.degrees(math.atan(y/x))


	
	return angle

def plotRawData(vector):
	
	plt.figure(1)
	plt.plot(vector)
	plt.draw()
	

def getExtractedFeatures():
	return extractedFeatures[0]

	

if __name__ == "__main__":
	readOutputs();
#


































