import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1) # 1x1 grid system, plot number 1

def animate(i): # call this at every snapshot
	graph_data = open('file.txt', 'r').read()
	lines = graph_data.split('\n')
	x = []
	y = []
	for line in lines:
		if len(line) > 1:
			x_add, y_add = line.split(',');
			x.append(x_add)
			y.append(y_add)

	ax1.clear() # this is pretty computationally light
	ax1.plot(x, y) # drawing stuff is computationally heavy

# animation is what we imported above
# args of FuncAnimation: figure, function, interval
	# figure is the matplotlib figure we are using
	# animate is the function we are calling regularly
	# interval is the number of milliseconds 
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
	
