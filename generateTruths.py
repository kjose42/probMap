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
	#i represents the current grid square, used to check square's boolean var
	i = 2
	for x in range(0, c):
		tmp_arrT = []
		for y in range(0, r):
			cx, cy, b, h, t = content[i].split()
			x1 = ((int(cx)-1) * 50 + 25)
			y1 = ((int(cy)-1) * 50 + 25)
			x2 = (y1 + 50)
			y2 = (x1 + 50)
			b = b.strip()
			my_canvas.create_rectangle(x1,y1,y2,x2)
			if b == '1': #square is blocked
				tmp_arrT.append('B')
				my_canvas.create_rectangle(x1,y1,y2,x2,fill='gray')
			if h == '1': #square is highway
				tmp_arrT.append('H')
				my_canvas.create_rectangle(x1,y1,y2,x2,fill='yellow')
			if t == '1': #square is "hard to traverse"
				tmp_arrT.append('T')
				my_canvas.create_rectangle(x1,y1,y2,x2,fill='purple')
			if b == '0' and h == '0' and t == '0':
				tmp_arrT.append('N')
			i = i + 1
			my_canvas.create_rectangle(x1,y1,y2,x2)
		gridT.append(tmp_arrT)

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

	for i in range(100):
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
		for inc in range(100): #generating ground truth states
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
			if gridT[curx - 1][cury - 1] == 'B' or movef == 1: #checking if its trying to move to a blocked block
				curx = oldx
				cury = oldy
			moveArr.append(moveChar)
			f.write(str(curx) + " " + str(cury) + "\n")
		
			actualType = 'N'
			otherTypes = ['H', 'T']
			if gridT[curx - 1][cury - 1] == 'H':
				actualType = 'H'
				otherTypes = ['N', 'T']
			if gridT[curx - 1][cury - 1] == 'T':
				actualType = 'T'
				otherTypes = ['N', 'H']
			senseFail1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] #5% chance of failing and sensing other type
			senseFail2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] 
			senseF1 = random.choice(senseFail1)
			senseF2 = random.choice(senseFail2)
			if senseF1 == 1:
				sensorArr.append(otherTypes[0])
			elif senseF2 == 1:
				sensorArr.append(otherTypes[1])
			else:
				sensorArr.append(actualType)
					
		

		#generating actions
		f.write("a:\n")
		for inc in range(100):
			f.write(moveArr[inc] + "\n")

		#generating sensor readings
		f.write("e:\n")
		for inc in range(100):
			f.write(sensorArr[inc] + "\n")

		f.close()

	root.resizable(True, True)
	root.mainloop()

def main():
	textnum = input('Enter the number of the testcase that you want to run: ')
	testFile = open(f'testcase{textnum}.txt', "r")
	content = testFile.readlines()
	col, row = content[1].split()
	createGrid(int(col), int(row), content, textnum)
main();
