from tkinter import *
from tkinter import ttk
from math import sqrt
from array import *
import random

class block:
	def __init__(self, position, blockType):
		if blockType == 'B':
			self.blocked = True
		else:
			self.blocked = False
		if blockType == 'H':
			self.highway = True
		else:
			self.highway = False
		if blockType == 'T':
			self.traverse = True
		else:
			self.traverse = False
		if blockType == 'N':
			self.normal = True
		else:
			self.normal = False
		self.x = position[0]
		self.y = position[1]

def createGrid(c, r, content, inNum):
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
	gridCP = [[0]*r for i in range(c)] #grid that shows each square's probability at current iteration
	probN = 0 #probability of agent in normal block
	probH = 0 #probability of agent in highway block
	probT = 0 #probability of agent in "hard to traverse"
	blockedCount = 0 #total num of blocked blocks

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
	
	#labelling x axis
	for x in range(0, c):
		text = my_canvas.create_text(x * 50 + 50, 10, text=x+1, tags="text")
		# my_canvas.update()

	#labelling y axis
	for y in range(0, r):
		text = my_canvas.create_text(10, y * 50 + 50, text=y+1, tags="text")

	# Create a list of block objects
	blk_lst = []
	for i in range(c):
		for j in range(r):
			temp_block = block([i+1, j+1], gridT[i][j])
			blk_lst.append(temp_block)

	for i in range(1):
		f = open(f'InfoFile{i}ForMap{inNum}.txt', "x")
		startx = random.randint(1, c)
		starty = random.randint(1, r)
		while blk_lst[startx*starty - 1].blocked == True: #change coords if starting block is blocked
			startx = random.randint(1, c)
			starty = random.randint(1, r)
		f.write("(x0, y0) = (" + str(startx) + "," + str(starty) + ")\n")
		f.write("(xi, yi):\n")
		curx = startx
		cury = starty
		moveArr = []
		sensorArr = []
		for inc in range(10): #generating ground truth states
			move = random.randint(1, 4) #1 = U, 2 = L, 3 = D, 4 = R
			moveChar = ' '
			oldx = curx
			oldy = cury
			#updating coords
			if move == 1:
				moveChar = 'U'
				if cury != 1:
					cury = cury - 1
			if move == 2:
				moveChar = 'L'
				if curx != 1:
					curx = curx - 1
			if move == 3:
				moveChar = 'D'
				if cury != r:
					cury = cury + 1
			if move == 4:
				moveChar = 'R'
				if curx != c:
					curx = curx + 1
			moveFail = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] # 10% chance of move failing
			movef = random.choice(moveFail)
			#if movef == 1:
				#print("fail")
			if gridT[curx - 1][cury - 1] == 'B' or movef == 1: #checking if its trying to move to a blocked block
				#print("blocked")
				curx = oldx
				cury = oldy
			moveArr.append(moveChar)
			#print("*" + str(curx) + " " + str(cury) + "*")
			f.write("(" + str(curx) + "," + str(cury) + ")\n")
		
			actualType = 'N'
			otherTypes = ['H', 'T']
			if gridT[curx - 1][cury - 1] == 'H':
				actualType = 'H'
				otherTypes = ['N', 'T']
			if gridT[curx - 1][cury - 1] == 'T':
				actualType = 'T'
				otherTypes = ['N', 'H']
			print(actualType)
			senseFail1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] #5% chance of failing and sensing other type
			senseFail2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] 
			senseF1 = random.choice(senseFail1)
			senseF2 = random.choice(senseFail2)
			if senseF1 == 1:
				print("fail1" + otherTypes[0])
				sensorArr.append(otherTypes[0])
			elif senseF2 == 1:
				print("fail2" + otherTypes[1])
				sensorArr.append(otherTypes[1])
			else:
				sensorArr.append(actualType)
					
		

		#generating actions
		f.write("a:\n")
		for inc in range(10):
			f.write(moveArr[inc] + "\n")

		#generating sensor readings
		f.write("e:\n")
		for inc in range(10):
			f.write(sensorArr[inc] + "\n")

		f.close()
		
	textNum = input('Enter the number of the ground truth file that you want to run: ')
	print(textNum)
	testFile = open(f'InfoFile{textNum}ForMap{inNum}.txt', "r")
	content = testFile.readlines()
	for i in range(4):
		direction = content[3+10+i].rstrip()
		print(direction)
		blockType = content[4+10+10+i].rstrip()
		print(blockType)
		typeProb = 0	
		if blockType == 'N':
			typeProb = probN
		if blockType == 'H':
			typeProb = probH
		if blockType == 'T':
			typeProb = probT
		total = 0
		if prevDir == direction:
			print('hey')
		for x in range(c):
			for y in range(r):
				if prevDir == direction:
					ansArr = predictCalc(x, y, r, c, direction, blockType, typeProb, gridF1[x][y], gridF2[x][y], gridT, gridP)
					gridF1[x][y] = ansArr[0]
					gridF2[x][y] = ansArr[1]
					gridCP[x][y] = ansArr[0]
				else:	
					ansArr = filterCal(x, y, r, c, direction, blockType, typeProb, gridT, gridP)
					gridCP[x][y] = ansArr[0]
					gridF1[x][y] = ansArr[0]
					gridF2[x][y] = ansArr[1]
				total = total + gridCP[x][y]
		
		for x in range(c):
			for y in range(r):
				gridCP[x][y] = gridCP[x][y]/total
		gridP = gridCP
		probArr = resetTypeProb(c, r, gridT, gridP)
		probN = probArr[0]
		probH = probArr[1]
		probT = probArr[2]
		print(probN)
		print(probH)
		print(probT)
		prevDir = direction
	for x in range(c):
		for y in range(r):
			x1 = (x * 50 + 20)
			x2 = (x1 + 10)
			y1 = (y * 50 + 20)
			y2 = (y1 + 10)
			text = my_canvas.create_text(x1 + 20, y1 + 12, font=("Helvetica", 10), text=round(gridP[x][y], 3), tags="text")
	print(gridF2[19][9])
	root.resizable(True, True)
	root.mainloop()

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
	ansArr.append(ansCalc1)
	ansArr.append(ansCalc2)
	
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
	ansArr.append(ans)
	return ansArr

def main():
	textnum = input('Enter the number of the testcase that you want to run: ')
	testFile = open(f'testcase{textnum}.txt', "r")
	content = testFile.readlines()
	col, row = content[1].split()
	createGrid(int(col), int(row), content, textnum)
main();
