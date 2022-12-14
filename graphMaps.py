import matplotlib.pyplot as plt

file1 = open('testcase0.txt', 'r')
count = 0

probability_list = []
num_list = []
  
while True:
    count += 1
  
    # Get next line from file
    line = file1.readline()
  
    # if line is empty
    # end of file is reached
    if not line:
        break
    
    num = float(line)
    probability_list.append(num)
    num_list.append(count)
    print(num)
  
file1.close()

plt.plot(num_list, probability_list)
plt.title('Error Graph')
plt.xlabel('Number of Readings')
plt.ylabel('Magnitude of Error')
plt.show()