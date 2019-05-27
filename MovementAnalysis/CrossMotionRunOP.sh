#!/bin/bash




SCRIPT_DIR=$(pwd)

OUTPUT_DIR="$(pwd)/output/"

PYTHON_DIR="/home/ieeta/JoaoAmaral_Crossfit/CrossMotionServer/MovementAnalysis/"

SERVER_DATA_ROOT="/home/ieeta/JoaoAmaral_Crossfit/CrossMotionServer/ServerData"

OPENPOSE_DIR="/home/ieeta/JoaoAmaral_Crossfit/openpose/"


FLAG=$1 	#flag can be --compare(compare 2 vids), --store (store a model) , or --check(to check a certain video among the models)




#RUN OPEN POSE
#KEYPOINT SCALE:
# 0 to scale it to the original source resolution; 
# 1 to scale it to the net output size (set with net_resolution); 
# 2 to scale it to the final output size (set with resolution);
# 3 to scale it in the range [0,1], where (0,0) would be the top-left corner of the image, and (1,1) the bottom-right one; 
# 4 for range [-1,1], where (-1,-1) would be the top-left corner of the image, and (1,1) the bottom-right one. 


runOpenPose()
{
	cd $OPENPOSE_DIR

	#./build/examples/openpose/openpose.bin  --render_pose 0 --video $1 --write_json $2 --keypoint_scale 3 #--display 0

	#with video
	CMD=$(ffprobe -loglevel error -select_streams v:0 -show_entries stream_tags=rotate -of default=nw=1:nk=1 -i "$1")


	

	if [[ "$CMD" -eq "90" ]]; then
		echo "Video is rotated"

		./build/examples/openpose/openpose.bin --write_video $3 --number_people_max 1 --video $1 --write_json $2 --keypoint_scale 4 --frame_rotate 270

	else
		./build/examples/openpose/openpose.bin --write_video $3 --number_people_max 1 --video $1 --write_json $2 --keypoint_scale 4 #--frame_rotate 270 #--disable_blending true
	fi
	cd $SCRIPT_DIR
}


#execute python program to process outputs










clearOutput() 
	{
		if [ ! -z "$(ls -a $OUTPUT_DIR)" ]
		then
			printf "\nCleaning previous output data...\n"
			rm -rf output/*
		fi
	}

checkVideoExists ()
	{
		echo "$1"
		if [ ! -f $1 ]
		then
			printf "Could not find video!!! \n"
			exit 1
		fi 
	}




#test input arguments

case "$1" in

	--compare)
		ARG=""
		if [ "$#" -lt 2 ]; then
    		echo "USAGE: ./CrossMotionOP.sh --compare <PathToVideo1> <PathToVideo1> ... (as many as you want to compare)\n"
    		exit 1
		fi
		rm -rf temp  
		mkdir temp #temporary directory to store json files with 

		for ((i=2;i<=$#;i++)); 
		do
			mkdir temp/vid$((i-1))
			VIDEO_RELATIVE_PATH=${!i}
			echo $VIDEO_RELATIVE_PATH

			VIDEO_ABS_PATH="$(pwd)/$VIDEO_RELATIVE_PATH"
			checkVideoExists $VIDEO_ABS_PATH
			OUTPUT_DIR="$(pwd)/temp/vid$((i-1))"
			runOpenPose $VIDEO_ABS_PATH $OUTPUT_DIR
			ARG="$ARG $OUTPUT_DIR"
		done

		
		

		
		

		echo $ARG

		cd $PYTHON_DIR

		python ./compareVideos.py $ARG 

		#



		exit 0
		;;

	--store)
		
		if [ "$#" -ne 3 ]; then
    		echo "USAGE: ./CrossMotionOP.sh --store <PathToVideo> <exercise>\n"
    		exit 1
		fi

		VIDEO_RELATIVE_PATH=$2
		EXERCISE=$3

		mkdir models_output
		rm -rf models_output/*
		

		OUTPUT_DIR="$(pwd)/models_output"
		
		
		VIDEO_ABS_PATH="$(pwd)/$VIDEO_RELATIVE_PATH"
		checkVideoExists $VIDEO_ABS_PATH

		runOpenPose $VIDEO_ABS_PATH $OUTPUT_DIR



		python storeModel.py $OUTPUT_DIR #$EXERCISE


		;;










	--check)
		


		VIDEO_NAME=${2%.*} #REMOVE FILE EXTENSON
		VIDEO_FILE=$2
		USERNAME=$3	
		VIDEO_ABS_PATH=$SERVER_DATA_ROOT/UploadedVideos/$USERNAME/$VIDEO_FILE

		#echo "ARGS FOR CHECKING::$2 $3"

		if [ ! -d "$SERVER_DATA_ROOT/OpenPoseOutput/" ]; then

			mkdir "$SERVER_DATA_ROOT/OpenPoseOutput/"
			
			
		fi

		if [ ! -d "$SERVER_DATA_ROOT/ProcessedVideos/" ]; then

			mkdir "$SERVER_DATA_ROOT/ProcessedVideos/"
			
			
		fi


		

		#if the directory for this user does not exist
		if [ ! -d "$SERVER_DATA_ROOT/OpenPoseOutput/$USERNAME" ]; then

			mkdir "$SERVER_DATA_ROOT/OpenPoseOutput/$USERNAME"
			
			
		fi

		if [ ! -d "$SERVER_DATA_ROOT/ProcessedVideos/$USERNAME" ]; then

			mkdir "$SERVER_DATA_ROOT/ProcessedVideos/$USERNAME"
			
			
		fi


		OUTPUT_DIR="$SERVER_DATA_ROOT/OpenPoseOutput/$USERNAME/$VIDEO_NAME/"

		mkdir "$SERVER_DATA_ROOT/ProcessedVideos/$USERNAME/$VIDEO_NAME/"

		PROCESSED_VIDEO_PATH="$SERVER_DATA_ROOT/ProcessedVideos/$USERNAME/$VIDEO_NAME/$VIDEO_NAME.avi"

		mkdir "$OUTPUT_DIR"
		
		#echo "OUTPUT_DIR: $OUTPUT_DIR"
		
		cd $PYTHON_DIR		
	

		#echo "$(pwd) VIDEO_ABS_PATH=$VIDEO_ABS_PATH"
		checkVideoExists $VIDEO_ABS_PATH

		
		echo "\n\n\n\n\n ------------------RUNNING OP---------------\n\n\n\n\n"
		
		echo "\n\n\n\n\n OUTPUT_DIR -----  $OUTPUT_DIR  ---------------\n\n\n\n\n"

		runOpenPose $VIDEO_ABS_PATH $OUTPUT_DIR $PROCESSED_VIDEO_PATH

		#convert output to MP4

		ffmpeg -i $PROCESSED_VIDEO_PATH "$SERVER_DATA_ROOT/ProcessedVideos/$USERNAME/$VIDEO_NAME/$VIDEO_NAME.mp4"

		rm $PROCESSED_VIDEO_PATH
		

		
		

		#echo $ARG

		#cd $PYTHON_DIR

		#python ./ServerCompareVideos.py

		#



		exit 0 ;;


esac

#if [ "$#" -ne 1 ]; then
 #   echo "Illegal number of parameters"
#fi


#VIDEO_RELATIVE_PATH=$1

#if [ -z "$VIDEO_RELATIVE_PATH" ]
#then
#	printf "USAGE: ./CrossMotionOP.sh <PathToVideo> \n"
#	exit
#fi



#OUTPUT_DIR="$(pwd)/output/"

#check if output directory is empty and clean outputs







VIDEO_ABS_PATH="$(pwd)/$VIDEO_RELATIVE_PATH"







