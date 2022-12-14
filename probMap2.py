from tkinter import *
from tkinter import ttk
from math import sqrt
from array import *
import random

def createGrid(c, r, content, contentTruth):
	root = Tk()
	root.title('Grid')
	root.geometry("800x700")

	# Create A Main frame
	main_frame = Frame(root)
	main_frame.pack(fill=BOTH,expand=1)

	# Create Frame for X Scrollbar
	sec = Frame(main_frame)
	sec.pack(fill=X,side=BOTTOM)

	# Create A Canvas
	my_canvas = Canvas(main_frame)
	my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

	# Add A Scrollbars to Canvas
	x_scrollbar = ttk.Scrollbar(sec,orient=HORIZONTAL,command=my_canvas.xview)
	x_scrollbar.pack(side=BOTTOM,fill=X)
	y_scrollbar = ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
	y_scrollbar.pack(side=RIGHT,fill=Y)

	# Configure the canvas
	my_canvas.configure(xscrollcommand=x_scrollbar.set)
	my_canvas.configure(yscrollcommand=y_scrollbar.set)
	my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(ALL))) 

	# Create Another Frame INSIDE the Canvas
	second_frame = Frame(my_canvas)

	# Add that New Frame a Window In The Canvas
	my_canvas.create_window((0,0),window= second_frame, anchor="nw")


	#-------------------------------------------------------------------------------------------
	#Drawing the Grid (sqaures, vertices, start)
	gridT = [] #grid indicating square type
	gridP = [] #grid that shows each square's probability at previous iteration
	gridCP = [[0]*r for i in range(c)] #grid that shows each square's probability at current iteration = P(X = C|E = T)
	gridF1 = [[0]*r for i in range(c)] #grid that shows P(X = C|E = T) filtering
	gridF2 = [[0]*r for i in range(c)] #grid that shows P(X != C|E = T) filtering
	probN = 0 #probability of agent in normal block
	probH = 0 #probability of agent in highway block
	probT = 0 #probability of agent in "hard to traverse"
	blockedCount = 0 #total num of blocked blocks
	prevDir = ' ' #direction of previous step

	draw(c, r, content, contentTruth, gridT, my_canvas)
	
	#counting blocked squares
	i = 2
	for x in range(0, c):
		for y in range(0, r):
			cx, cy, b, h, t = content[i].split()
			b = b.strip()
			if b == '1': #square is blocked
				blockedCount = blockedCount + 1
			i = i + 1

	i = 2
	for co in range(0, c):
		tmp_arrT = []
		tmp_arrP = []
		for ro in range(0, r):
			cx, cy, b, h, t = content[i].split()
			if b == '1': #if bool == 1, then square is blocked
				tmp_arrT.append('B')
				tmp_arrP.append(0)
			elif h == '1':
				tmp_arrT.append('H')
				tmp_arrP.append(1/(r*c - blockedCount))
				probH = probH + 1/(r*c-blockedCount) #adding up probability of initiating on H
			elif t == '1':
				tmp_arrT.append('T')
				tmp_arrP.append(1/(r*c - blockedCount))
				probT = probT + 1/(r*c-blockedCount)
			else:
				tmp_arrT.append('N')
				tmp_arrP.append(1/(r*c - blockedCount))
				probN = probN + 1/(r*c-blockedCount)
			i = i + 1
		gridT.append(tmp_arrT)
		gridP.append(tmp_arrP)
	skip = 0
	for i in range(100):
		trux, truy = contentTruth[2+i].split()
		trux = int(trux)
		truy = int(truy)
		x1 = (trux * 50)
		y1 = (truy * 50)
		x2 = x1 + 20
		y2 = y1 + 20
		my_canvas.create_oval(x1, y1, x2, y2, fill='blue')
		direction = contentTruth[3+100+i].rstrip()
		#print(direction)
		blockType = contentTruth[4+100+100+i].rstrip()
		#print(blockType)
		typeProb = 0	
		if blockType == 'N':
			typeProb = probN
		if blockType == 'H':
			typeProb = probH
		if blockType == 'T':
			typeProb = probT
		total = 0
		for x in range(c):
			for y in range(r):
				#use prediction formula when moving in the same direction as last step
				if prevDir == direction:
					ansArr = predictCalc(x, y, r, c, direction, blockType, typeProb, gridF1[x][y], gridF2[x][y], gridT, gridP)
					gridF1[x][y] = ansArr[0]
					gridF2[x][y] = ansArr[1]
					gridCP[x][y] = ansArr[2]
				else:	
					ansArr = filterCal(x, y, r, c, direction, blockType, typeProb, gridT, gridP)
					gridCP[x][y] = ansArr[0]
					gridF1[x][y] = ansArr[0]
					gridF2[x][y] = ansArr[1]
				total = total + gridCP[x][y]
		for x in range(c):
			for y in range(r):
				gridCP[x][y] = gridCP[x][y]/total #normalizing
				gridP[x][y] = gridCP[x][y]
		#update type probabilities with values from the new probability map
		probArr = resetTypeProb(c, r, gridT, gridP)
		probN = probArr[0]
		probH = probArr[1]
		probT = probArr[2]
		prevDir = direction
		for x in range(c):
			for y in range(r):
				x1 = (x * 50 + 20)
				y1 = (y * 50 + 20)
				text = my_canvas.create_text(x1 + 25, y1 + 15, font=("Helvetica", 10), text=round(gridP[x][y], 3), tags="text")
		if i != 99:
			if skip == 0:
				inNum = input('Enter the number of steps you want to proceed with')
				skip = int(inNum) - 1
			else:#still need to skip more steps
				skip = skip - 1
			my_canvas.delete('all')
			draw(c, r, content, contentTruth, gridT, my_canvas)
	root.resizable(True, True)
	root.mainloop()

def draw(c, r, content, contentTruth, gridT, my_canvas):
	#i represents the current grid square, used to check square's boolean var
	i = 2
	for x in range(0, c):
		for y in range(0, r):
			cx, cy, b, h, t = content[i].split()
			x1 = ((int(cx)-1) * 50 + 25)
			y1 = ((int(cy)-1) * 50 + 25)
			x2 = (y1 + 50)
			y2 = (x1 + 50)
			b = b.strip()
			my_canvas.create_rectangle(x1,y1,y2,x2)
			if b == '1': #square is blocked
				my_canvas.create_rectangle(x1,y1,y2,x2,fill='gray')
			if h == '1': #square is highway
				my_canvas.create_rectangle(x1,y1,y2,x2,fill='yellow')
			if t == '1': #square is "hard to traverse"
				my_canvas.create_rectangle(x1,y1,y2,x2,fill='purple')
			i = i + 1
			my_canvas.create_rectangle(x1,y1,y2,x2)
	
	#labelling x axis
	for x in range(0, c):
		text = my_canvas.create_text(x * 50 + 50, 10, text=x+1, tags="text")
		# my_canvas.update()

	#labelling y axis
	for y in range(0, r):
		text = my_canvas.create_text(10, y * 50 + 50, text=y+1, tags="text")

#update type probabilities with values from the new probability map
def resetTypeProb(c, r, gridT, gridP):
	probArr = []
	probN = 0
	probH = 0
	probT = 0
	for x in range(c):
		for y in range(r):
			if gridT[x][y] == 'N':
				probN = probN + gridP[x][y]
			if gridT[x][y] == 'H':
				probH = probH + gridP[x][y]
			if gridT[x][y] == 'T':
				probT = probT + gridP[x][y]
	probArr.append(probN)
	probArr.append(probH)
	probArr.append(probT)
	return probArr

def filterCal(x, y, r, c, direction, blockType, typeProb, gridT, gridP):
	ansArr = []
	if gridT[x][y] == 'B':
		ansArr.append(0.0)
		ansArr.append(0.0)
		return ansArr
	#{prevx, prevy} represents agent coords before moving into {x,y}
	#prevx or prevy will stay as -1 if out of bounds
	prevx = -1
	prevy = -1
	if direction == 'U':
		prevx = x
		if y != r-1:
			prevy = y + 1
	if direction == 'L':
		prevy = y
		if x != c-1:
			prevx = x + 1
	if direction == 'D':
		prevx = x
		if y != 0:
			prevy = y - 1
	if direction == 'R':
		prevy = y
		if x != 0:
			prevx = x - 1
	#{nextx, nexty} represents agent coords after moving from {x,y}
	#nextx or nexty will stay as -1 if out of bounds
	nextx = -1
	nexty = -1
	if direction == 'U':
		nextx = x
		if y != 0:
			nexty = y - 1
	if direction == 'L':
		nexty = y
		if x != 0:
			nextx = x - 1
	if direction == 'D':
		nextx = x
		if y != r-1:
			nexty = y + 1
	if direction == 'R':
		nexty = y
		if x != c-1:
			nextx = x + 1
	prevProb = 0
	calc1 = 0
	if prevx != -1 and prevy != -1: 
		prevProb = gridP[prevx][prevy]
	if nextx != -1 and nexty != -1:
		if gridT[nextx][nexty] == 'B':
			calc1 = 1*(gridP[x][y]) + .9*(prevProb)*(1-gridP[x][y])
		else:
			#if movement isnt blocked, .1 chance to stay
			calc1 = .1*(gridP[x][y]) + .9*(prevProb)*(1-gridP[x][y])
	else:
		calc1 = 1*(gridP[x][y]) + .9*(prevProb)*(1-gridP[x][y])
	#T represents block type, C represents {x,y})
	#given the agent is at {x,y}, calc1 is the probability of correct reading
	#= P(E = T|X = C)
	#given agent is at {x,y}, chance of reading is correct = P(E = T|X = C)
	if gridT[x][y] == blockType:
		calc1 = calc1 * .9
	else:
		calc1 = calc1 * .05
	#given agent is at {x,y}, chance of reading is correct = P(E = T|X = C)

	#given agent was prev not at {x,y}, chance of agent currently not at {x,y} = P(X1 != D|X0 != D)
	moveProb = 0 #calculating prob of agent moving and P(X1 != C|X0 != C) = True
	moveProb = .9*(1 - gridP[prevx][prevy] - gridP[x][y])
	stayProb = 0 #calculating prob of agent staying and P(X1 != C|X0 != C) = True
	stayProb = .1*(1 - gridP[x][y])
	#given agent was prev not at {x,y}, chance of agent currently not at {x,y} = P(X1 != D|X0 != D)
		
	#given agent is not at {x,y}, chance of reading is correct = P(E = T|X != C)
	#typeProb = chance of agent in right block type
	if gridT[x][y] == blockType:
		calc2 = .9*(typeProb-gridP[x][y]) + .05*(1-typeProb)
	else:
		calc2 = .9*typeProb + .05*(1-typeProb-gridP[x][y])
	#given agent is not at {x,y}, chance of reading is correct = P(E = T|X != C)

	#nextProb represents (X1 != C|X0 = C)
	#(X1 != C|X0 = C) means that agent moves from {x,y}
	nextProb = 0
	if nextx != -1 and nexty != -1: #case of out of bounds next position
		if gridT[nextx][nexty] == 'B':
			nextProb = 0
		else:
			nextProb = 1
	calc2 = calc2*(.9*nextProb*gridP[x][y] + (moveProb + stayProb)*(1-gridP[x][y]))
	#isolating 'a' variable
	a = 1/(calc1 + calc2)
	ansCalc1 = a*calc1 
	ansCalc2 = a*calc2
	ansArr.append(ansCalc1)#<- filtering equation answer = P(X = C|E = T)
	ansArr.append(ansCalc2)#<- filtering for P(X != C|E = T)
	return ansArr

def predictCalc(x, y, r, c, direction, blockType, typeProb, filter1, filter2, gridT, gridP):
	ansArr = []
	if gridT[x][y] == 'B':
		ansArr.append(0.0)
		ansArr.append(0.0)
		ansArr.append(0.0)
		return ansArr
	#{prevx, prevy} represents agent coords before moving into {x,y}
	#prevx or prevy will stay as -1 if out of bounds
	prevx = -1
	prevy = -1
	if direction == 'U':
		prevx = x
		if y != r-1:
			prevy = y + 1
	if direction == 'L':
		prevy = y
		if x != c-1:
			prevx = x + 1
	if direction == 'D':
		prevx = x
		if y != 0:
			prevy = y - 1
	if direction == 'R':
		prevy = y
		if x != 0:
			prevx = x - 1
	#{nextx, nexty} represents agent coords after moving from {x,y}
	#nextx or nexty will stay as -1 if out of bounds
	nextx = -1
	nexty = -1
	if direction == 'U':
		nextx = x
		if y != 0:
			nexty = y - 1
	if direction == 'L':
		nexty = y
		if x != 0:
			nextx = x - 1
	if direction == 'D':
		nextx = x
		if y != r-1:
			nexty = y + 1
	if direction == 'R':
		nexty = y
		if x != c-1:
			nextx = x + 1
	prevProb = 0
	#calc1 = probability of agent starting at {x,y} and staying there
	calc1 = 0
	#calc2 = probability of agent not starting at {x,y} and moving to {x,y}
	calc2 = 0
	if prevx != -1 and prevy != -1: 
		prevProb = gridP[prevx][prevy]
	if nextx != -1 and nexty != -1:
		if gridT[nextx][nexty] == 'B':
			calc1 = 1
		else:
			#if movement isnt blocked, .1 chance to stay
			calc1 = .1
	else:
		calc1 = 1
	calc2 = .9*(prevProb)
	ans = calc1*filter1 + calc2*filter2
	filterArr = filterCal(x, y, r, c, direction, blockType, typeProb, gridT, gridP)
	ansArr.append(filterArr[0])
	ansArr.append(filterArr[1])
	ansArr.append(ans)#<- answer for prediction equation
	return ansArr

def main():
	textNum = input('Enter the number of the testcase that you want to run: ')
	testFile = open(f'testcase{textNum}.txt', "r")
	content = testFile.readlines()
	col, row = content[1].split()
	textNum2 = input('Enter the number of the ground truth file that you want to run: ')
	testFile2 = open(f'InfoFile{textNum2}ForMap{textNum}.txt', "r")
	contentTruth = testFile2.readlines()
	createGrid(int(col), int(row), content, contentTruth)
	#createProb(int(col), int(row), context, textnum)
main();
