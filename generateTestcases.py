# A program that generates a certain number of testecases

import random

class block:
	def __init__(self, position, blk):
		if blk == 1:
			self.blocked = True
		else:
			self.blocked = False

		self.x = position[0]
		self.y = position[1]
		self.vertices = [(position[0], position[1]), (position[0], position[1] + 1), (position[0] + 1, position[1]), (position[0] + 1, position[1] + 1)]

def createTest(n):

	#randanly select a grid size
	row = 50	
	col = 100	

	# create file
	f = open(f'testcase{n}.txt', "x")

	# generate start, goal, and size of the grid
	listR = [*range(1, row+1, 1)]
	listC = [*range(1, col+1, 1)]
	listB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] # 10% chance of being blocked
	listH = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1] # 20% chance of being highway
	listT = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1] # 20% chance of being "hard to traverse"

	f.write(str(random.choice(listC)) + " " + str(random.choice(listR)) + "\n")
	f.write(str(random.choice(listC)) + " " + str(random.choice(listR)) + "\n")
	f.write(str(col) + " " + str(row) + "\n")

	# generate block status
	for tempC in range(1, col+1):	
		for tempR in range(1, row+1):
			intH = random.choice(listH)
			if intH == 0: #to avoid block from having more than 1 type
				intT = random.choice(listT)
			else:
				intT = 0
			if intH == 0 and intT == 0: #to avoid block from having more than 1 type
				intB = random.choice(listB)
			else:
				intB = 0
			temp_block = block([tempR, tempC], intB)
			blk_lst.append(temp_block)
			f.write(str(tempC) + " " + str(tempR) + " " + str(intB) + " " + str(intH) + " " + str(intT) + "\n")

	# close the file
	f.close()


def main():
	nTestcases = input('Enter the number of testcases to generate: ')
	for i in range(int(nTestcases)):
		print(f'Generating testcase {i}')
		createTest(i)

main();
