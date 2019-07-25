import json
import os
import ServerReadOutput
import sys
MODEL_FOLDER='models/'


#this function receives the features matrix, plane and exercise name as arguments
def storeMovement(features,exercise):

	side=features['plane']
	
	directory=os.path.join(os.getcwd(),MODEL_FOLDER,exercise+'/',side+'/')
	


	n_models = len(os.listdir(directory))


	modelName = directory+exercise+'_'+side+str(n_models+1)+'.json'

	print('\nwriting model file:\n'+modelName+'\n')


	print(features.keys())

	

	with open(modelName,'w') as outfile:
		json.dump(features,outfile)





def getFeaturesAndStore(args):



	features = ServerReadOutput.readOutputs(args[1])

	storeMovement(features,args[2]) #args[2]= exercise



if __name__ == '__main__':

	getFeaturesAndStore(sys.argv)

