

def keyframe(filepath):
	# Playing video from file:
	import cv2
	import numpy as np
	import os
	import time

	print ("filepath:", filepath)
	
	cap = cv2.VideoCapture(filepath)
	try:
		if not os.path.exists('images'):
			os.makedirs('images')
	except OSError:
		print('Error')
   
    
	# Find the number of frames
	video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) -1

	print ("Number of frames:     ", video_length)

	number= cap.get(cv2.CAP_PROP_FPS)
	
	print ("Number of frames/sec: ",number)

	count = 0
	sum2=0
	print ("Converting video..\n")
	non_zero_count=[]
	ret, prev_frame = cap.read()
	prev_frame1 = cv2.cvtColor(prev_frame,cv2.COLOR_RGB2GRAY)
	#chans = cv2.split(prev_frame)
	prev_frame1 = cv2.calcHist([prev_frame1], [0], None, [256], [0, 256])

	#prev_frame = cv2.calcHist([prev_frame], [0, 1, 2],None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
	name1= './images/frame' + str(count) + '.jpg'
	cv2.imwrite(name1,prev_frame)
	time_start = time.time()
	while ret:
        # Extract the frame
        	ret, frame = cap.read()
        	frame1 = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        #chans = cv2.split(prev_frame)
        #prev_frame = cv2.convertScaleAbs(canny_image)
        	frame1= cv2.calcHist([frame1], [0], None, [256], [0, 256])
        #frame = cv2.calcHist([frame], [0, 1, 2],None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        # Write the results back to output location.
        	diff = cv2.absdiff(frame1, prev_frame1)
       		x=count+1
        	a=np.count_nonzero(diff)
        	non_zero_count.append(np.count_nonzero(diff))
        	print (a)
        	prev_frame1=frame1
        # Saves image of the current frame in jpg file
        	name1 = './images/frame' + str(count) + '.jpg'
        # print ('Creating...' + name)
        	cv2.imwrite(name1, frame)
        	print("frame %d written \n"%count )
        # To stop duplicate images
        	count += 1
        	if (count > (video_length-1)):
            # Log the time again
            		time_end = time.time()
            # Release the feed
            		cap.release()
            		cv2.destroyAllWindows()
            # Print stats
            		sum1=sum(non_zero_count)
            		print ("Absolute difference sum:  %d" %sum1 )
            		mean=float(sum1)/count
            		print ("Mean is : %f" %mean)
            		x=count
            		while x:
                		sum2+=(non_zero_count[x-1]-mean)**2
                		x-=1
            		deviation=sum2/count
            		deviation= deviation**0.5
            		print("Deviation is : %f" %deviation)
            		threshold=deviation+mean
            		print ("Threshold is : %f" %threshold)
            		print ("Done extracting frames.\n%d frames extracted" % count)
            		print ("It took %d seconds for conversion." % (time_end-time_start))
            		break


	cap=cv2.VideoCapture(filepath)    
	try:
		if not os.path.exists('keyframes'):
			os.makedirs('keyframes')
	except OSError:
		print ('Error: Creating directory of data')
	video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
	count = 0
	
	ret, prev_frame = cap.read()
	prev_frame1 = cv2.cvtColor(prev_frame,cv2.COLOR_RGB2GRAY)
	#chans = cv2.split(prev_frame)
	y=1
	calculate=0
	prev_frame1 = cv2.calcHist([prev_frame1], [0], None, [256], [0, 256])
	while ret:
		ret, frame = cap.read()
		if ret:
			frame1 = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		else:
			break

		#frame1 = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		frame1 = cv2.calcHist([frame1], [0], None, [256], [0, 256])
		diff = cv2.absdiff(frame1, prev_frame1)
		diff = np.count_nonzero(diff)
		prev_frame1=frame1
		if diff>threshold:
			name2 = './keyframes/frame' + str(count) + '.jpg'
			if count<int(number)*y:
				if calculate==0:
					calculate=1
					cv2.imwrite(name2, frame)
					print("keyframe %d written \n"%count )
		count += 1
		if (count==int(number)*y):
			y+=1
			calculate=0
			if (count > (video_length-1)):
				time_end = time.time()
				cap.release()
				cv2.destroyAllWindows()
				print ("Done extracting frames.\n%d frames extracted" % count)
				print ("It took %d seconds for conversion." % (time_end-time_start))
				break
	return

