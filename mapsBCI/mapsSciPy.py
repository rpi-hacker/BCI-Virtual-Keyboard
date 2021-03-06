# particle filter simulation
# last edit: 12/14
# to run:
#	>> python
#	>> import mapsSciPy
##########################################----------QUESTIONS----------------############
# 
########################################----------BUGS------------------------###############
#
#########################################---------CURRENTLY WORKING ON--------###############
#

import time
from pylab import *

def createRoom(sz):
	"""
	This function intializes a grid representing a room
	Args: room size as array(height,width)
	Rtn: figure, room grid
	"""
	room = zeros( (sz[0], sz[1]),bool)
	room[:,0]=1
	room[:,-1]=1
	room[0,:]=1
	room[-1,:]=1
	f = figure(1)								#create plot window
	f.set_visible(0)							#hide
	clf()										#clear window
	# Show room map
	imshow(room, interpolation="nearest")
	f.set_visible(1)							
	draw()
	return f,room

def test():
	sz = array([[30,40]])
	room = zeros( (sz[0,0], sz[0,1]),bool )
	room[:,0]=1
	room[:,-1]=1
	room[0,:]=1
	room[-1,:]=1

	roboLoc = (15,16)

	pt = rand(50,2) * sz 
	while 1:
	  ## Graphics
	  f = figure(1)
	  f.set_visible(0)
	  clf()
	  # Show room map
	  imshow(room, interpolation="nearest")
	  # Show robot
	  plot([roboLoc[0]],[roboLoc[1]],'sr')
	  # Show particles
	  plot( pt[:,1],pt[:,0], 'oy')
	  # Set image size
	  axis([0,sz[0,1],0,sz[0,0]])
	  # Make changes visible
	  f.set_visible(1)
	  draw()
	  time.sleep(0.1)
	  ## Update particles
	  pt += randn(50,2)*0.2 + sz
	  pt %= sz


def randRoboLoc(sz,rm):
	"""
	This function initializes the position of the robot randomly in a given room.	
	args: room dims, room grid
	rtns: robo coords
	"""
	x = randint(1,sz[1])
	y = randint(1,sz[0])
	if rm[y,x]:									#test for legitimate coords					
		return randRoboLoc(sz,rm)
	return [x,y]


def createRobo(sz,fig,room):
	"""
	This function plots a point on a grid which represents a robot in a room
	Args: room dims[width,height], figure number, room coords (array[width x height])
	Rtns: [x,y] coords of the robot
	"""
	roboLoc = randRoboLoc(sz,room)
	fig.set_visible(0)
	clf()
	imshow(room, interpolation="nearest")
	plot([roboLoc[0]],[roboLoc[1]],'sr')
	axis([0,sz[1],0,sz[0]])
	fig.set_visible(1)
	draw()
	return roboLoc


def sampleUniform(dims,num):
	"""
	This function returns random samples from a uniform distribution
	Args: room dims[width,height], number of samples
	Rtns: array[numsamples x 2] of uniformly drawn samples from 0-width and 0-height
	"""
	locx = uniform(1,dims[0],num)				#samples from uniform distr (low,high,size)
	locy = uniform(1,dims[1],num)			
	return [locx,locy]


def GPS(loc,sigma,ns):
	"""
	This function returns a normal distribution simulating a noisy GPS position estimate
	Args: location[x,y], error, num samples
	Rtns: [normal(locx,sigma),normal(locy,sigma)]
	"""
	nx = normal(loc[0],sigma,ns)
	ny = normal(loc[1],sigma,ns)
	return [nx,ny]



def calcExp(smpl,ev):
	"""
	This function 
	Args: xy coord representing possible robot postition, sensor reading
	Rtns: 
	"""
	mnx = mean(ev[0])
	mny = mean(ev[1])
	sdx = std(ev[0])
	sdy = std(ev[1])
	xnum = (smpl[0] - mnx)**2				#numerators
	ynum = (smpl[1] - mny)**2
	exp_x = xnum / sdx**2
	exp_y = ynum / sdy**2
	
	if exp_x > 3 or exp_y > 3:
		print "too far: ", smpl
		return []
	else:
		#print "close enough:", smpl
		return exp(1)**[(0 - exp_x),(0 - exp_y)]
	
	



def filter(evidence,num,sz):
	"""
	This function uses sensor evidence to estimate the postion of the robot
	Args: sensor reading, number of particles, room size
	"""
	new = []									#new samples
	weights = []								#weights
	smx = 0										#sum of weights
	smy = 0
	n = 0										#num times to replicate new particles
	while new == []:
		print "sampling"
		samples = sampleUniform(sz,num)			#get location samples
		samples = array(samples)
		for i in range(0,num):
			sample = samples[:,i]
			exp = calcExp(sample,evidence)
			if exp != []:
				new.append(sample)
				weights.append(exp)
		if weights != []:
			weights = array(weights)
			smx = sum(weights[:,0],axis=0)
			smy = sum(weights[:,1],axis=0)
		print "close enough",new
		if smx > smy:	
			n = floor(weights[:,0] * num * (1/smx))
		else:
			n = floor(weights[:,0] * num * (1/smy))



def start():
	N = 100										#number of particles
	sz = array([30,40])							#room dimensions
	sigmaGps = 2								#gps noise
	fig,room = createRoom(sz)
	rloc = createRobo(sz,fig,room)
	gps = GPS(rloc,sigmaGps,N)					#get distribution of gps readings			
	filter(gps,N,sz)							#particle filter


##########################------------main----------------############
start()
  
