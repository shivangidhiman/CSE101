import matplotlib.pyplot as plt
from math import *

plt.ion()

#function to plot the required shape 
class Transformer(object):
	
	def __init__(self,shape,xCordinates,yCordinates):
		self.shape=shape
		self.xCordinates=xCordinates
		self.yCordinates=yCordinates

	def plot(self,a=1,b=1,majorAxis=1,minorAxis=1,angle=1):
		plt.plot(self.xCordinates,self.yCordinates)
		plt.axis("scaled")

#to plot a polygon
		if(self.shape=="polygon"):
			xCordinates=self.xCordinates[:]
			xCordinates.pop()
			xCordinates=[round(x,2) for x in xCordinates]
			yCordinates=self.yCordinates[:]
			yCordinates.pop()
			yCordinates=[round(x,2) for x in yCordinates]
			print(*xCordinates,sep=" ")
			print(*yCordinates,sep=" ")

#to plot a disc
		elif(self.shape=="disc"):
			print(round(a,2),round(b,2),round(majorAxis,2),round(minorAxis,2),angle)

		plt.pause(2)

#to exit the program
	def closeplot(self):
		plt.close()

#function to multiply two matrices
	def multiply(self,mat_A,mat_B):
		temp=[]

		for x in range(3):
			sum=0
			for y in range(3):
				sum+=mat_A[y][x]*mat_B[y]
			temp.append(sum)

		return(temp[0],temp[1])

#function to translate a disc
	def translation(self,dx,dy,a=1,b=1):
		mat_A=[[1,0,0],[0,1,0],[dx,dy,1]]

		for x in range(len(self.xCordinates)):
			self.xCordinates[x],self.yCordinates[x]=self.multiply(mat_A,[self.xCordinates[x],self.yCordinates[x],1])

		#to multiply the matrices
		if(self.shape=="disc"):
			a,b=self.multiply(mat_A,[a,b,1])

		return a,b

#functon used for scaling a disc
	def scale(self,sx,sy,majorAxis=1,minorAxis=1):
		mat_A=[[sx,0,0],[0,sy,0],[0,0,1]]
		
		for x in range(len(self.xCordinates)):
			self.xCordinates[x],self.yCordinates[x]=self.multiply(mat_A,[self.xCordinates[x],self.yCordinates[x],1])

		if(self.shape=="disc"):
			majorAxis,minorAxis=self.multiply(mat_A,[majorAxis,minorAxis,1])
			print(majorAxis,minorAxis)

		return majorAxis,minorAxis

#function for rotating a disc
	def rotate(self,theta,angle=1,a=1,b=1):
		if(self.shape=="disc"):
			angle+= theta
			for x in range(len(self.xCordinates)):
				self.xCordinates[x],self.yCordinates[x]=self.xCordinates[x]-a,self.yCordinates[x]-b

		theta=radians(theta)

		mat_A=[[cos(theta),sin(theta),0],[-sin(theta),cos(theta),0],[0,0,1]]
		
		for x in range(len(self.xCordinates)):
			self.xCordinates[x],self.yCordinates[x]=self.multiply(mat_A,[self.xCordinates[x],self.yCordinates[x],1])

		if(self.shape=="disc"):
			a,b=self.multiply(mat_A,[a,b,1])
			for x in range(len(self.xCordinates)):
				self.xCordinates[x],self.yCordinates[x]=self.xCordinates[x]+a,self.yCordinates[x]+b

		return angle,a,b


class Polygon(object):

	def driver(self):

		xCordinates=list(map(int,input("x-coordinates of the polygon (eg: 1 -1 -1 1): ").split()))
		xCordinates+=[xCordinates[0]]
		yCordinates=list(map(int,input("y-coordinates of the polygon (eg: 1 1 -1 -1): ").split()))
		yCordinates+=[yCordinates[0]]

		poly=Transformer("polygon",xCordinates,yCordinates)
		poly.plot()

		print('\nEnter queries of the form:')
		print('S x y')
		print('R theta')
		print('S dx dy')
		print("'quit' to exit\n")

		while(True):
			choice=input().split()

			#to exit
			if(choice[0]=="quit"):
				poly.closeplot()
				break

			#to rotate
			elif (choice[0]=='R'):
				poly.rotate(float(choice[1]))

			#to translate
			elif (choice[0]=='T'):
				poly.translation(float(choice[1]),float(choice[2]))

			#to scale
			elif (choice[0]=='S'):
				poly.scale(float(choice[1]),float(choice[2]))

			else:
				print("Invalid Input")

			poly.plot()

class Disc(object):

	def driver(self):
		a,b,r=map(int,input("Enter a, b, r such that disc of radius r is centred at (a,b): ").split())
		angle=(2*3.1416/2000)
		x=0

		xCordinates=[]
		yCordinates=[]

		while(x<=2*3.1416):
			xCordinates.append(r*cos(x)+a)
			yCordinates.append(r*sin(x)+b)
			x+=angle

		majorAxis=r
		minorAxis=r
		angle=0

		disc=Transformer("disc",xCordinates,yCordinates)
		disc.plot(a,b,majorAxis,minorAxis,angle)

		print('\nEnter queries of the form:')
		print('S x y')
		print('R theta')
		print('S dx dy')
		print("'quit' to exit\n")

		while(True):
			choice=input().split()

			#to quit
			if(choice[0]=="quit"):
				disc.closeplot()
				break

			#to rotate
			elif (choice[0]=='R'):
				angle,a,b=disc.rotate(float(choice[1]),angle,a,b)

			#to translate
			elif (choice[0]=='T'):
				a,b=disc.translation(float(choice[1]),float(choice[2]),a,b)

			#to scale
			elif (choice[0]=='S'):
				majorAxis,minorAxis=disc.scale(float(choice[1]),float(choice[2]),majorAxis,minorAxis)

			else:
				print("Invalid Input")

			disc.plot(a,b,majorAxis,minorAxis,angle)


if __name__ == '__main__':
	
	shape=input("Shape (disc/polygon): ")
	
	if(shape=="polygon"):
		A=Polygon()
		A.driver()

	elif(shape=="disc"):
		A=Disc()
		A.driver()

	else:
		print("Error")








