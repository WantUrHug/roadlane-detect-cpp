import numpy as np
import turtle, time
from pprint import pprint
import matplotlib.animation as animation
import matplotlib.pyplot as plt

def read_angles(log):
	
	dif = []
	with open(log, encoding = "utf-8") as file:
		
		a = file.readlines()
		xs = []
		ys = []
		ts = []
		#pprint(len(a))
		for b in a[1:]:
			b = b.split(",")
			#print(b)
			x = float(b[3])
			y = float(b[4])
			ts.append(strptime(b[6][:-2]))
			xs.append(x)
			ys.append(x)
	return ts, xs, ys

def data_justify(ts, xs, ys):

	#freq = 20
	interv_m = 6
	start_m = 41
	#tot = 20*4*60
	new_ts = []
	for minute in range(start_m, start_m + interv_m):
		for second in range(0, 60):
			for ms in range(0, 1000, 50):
				new_ts.append(build_t(2019, 11, 4, 19, minute, second, ms))
	num = len(ts)
	result_x = []
	result_y = []

	start_m = 12
	start_s, start_ms = 0, 0

	ind = 0
	max_ind = len(ts)

	for i in new_ts:
		ideal = cal_second(i)
		#print("a")
		
		while ind + 1 < max_ind:
			flag1 = cal_second(ts[ind])
			flag2 = cal_second(ts[ind + 1])
			if flag1 < ideal and flag2 >= ideal:
			
				dx = xs[ind + 1] - xs[ind]
				if dx > 180:
					if flag2 - ideal > ideal - flag1:
						avg_x = (xs[ind] + 360)*(flag2 - ideal)/(flag2 - flag1) + xs[ind + 1]*(ideal - flag1)/(flag2 - flag1)
					else:
						avg_x = xs[ind]*(flag2 - ideal)/(flag2 - flag1) + (xs[ind + 1] - 360)*(ideal - flag1)/(flag2 - flag1)
				elif dx < -180:
					if flag2 - ideal > ideal - flag1:
						avg_x = (xs[ind] - 360)*(flag2 - ideal)/(flag2 - flag1) + xs[ind + 1]*(ideal - flag1)/(flag2 - flag1)
					else:
						avg_x = xs[ind]*(flag2 - ideal)/(flag2 - flag1) + (xs[ind + 1] + 360)*(ideal - flag1)/(flag2 - flag1)
				else:
					avg_x = xs[ind]*(flag2 - ideal)/(flag2 - flag1) + xs[ind + 1]*(ideal - flag1)/(flag2 - flag1)
	
				dy = ys[ind + 1] - ys[ind]
				if dy > 180:
					if flag2 - ideal > ideal - flag1:
						avg_y = (ys[ind] + 360)*(flag2 - ideal)/(flag2 - flag1) + ys[ind + 1]*(ideal - flag1)/(flag2 - flag1)
					else:
						avg_y = ys[ind]*(flag2 - ideal)/(flag2 - flag1) + (ys[ind + 1] - 360)*(ideal - flag1)/(flag2 - flag1)
				elif dy < -180:
					if flag2 - ideal > ideal - flag1:
						avg_y = (ys[ind] - 360)*(flag2 - ideal)/(flag2 - flag1) + ys[ind + 1]*(ideal - flag1)/(flag2 - flag1)
					else:
						avg_y = ys[ind]*(flag2 - ideal)/(flag2 - flag1) + (ys[ind + 1] + 360)*(ideal - flag1)/(flag2 - flag1)
				else:
					avg_y = ys[ind]*(flag2 - ideal)/(flag2 - flag1) + ys[ind + 1]*(ideal - flag1)/(flag2 - flag1)
				
				result_x.append(avg_x)
				result_y.append(avg_y)
				#ind += 1
				#print("s")
				break
			else:
				ind += 1
				#print("f")

	return new_ts, result_x, result_y

def cal_second(t):

	return t["min"]*60+t["second"]+t["ms"]/1000

def build_t(year, month, day, hour, minute, second, ms):

	t = {}
	t["year"] = year
	t["month"] = month
	t["day"] = day
	t["hour"] = hour
	t["min"] = minute
	t["second"] = second
	t["ms"] = ms

	return t

def cal_dif_angle(dif_x, dif_y):

	if dif_x > 180:
		dif_x = dif_x - 360
	elif dif_x < -180:
		dif_x = 360 + dif_x

	if dif_y > 180:
		dif_y = dif_y - 360
	elif dif_y < -180:
		dif_y = 360 + dif_y

	return (dif_y + dif_x)/2

def strptime(string):

	a = string.split()
	b = a[0].split("-")
	result = {}
	result["year"] = int(b[0])
	result["month"] = int(b[1])
	result["day"] = int(b[2])

	c = a[1].split(":")
	result["hour"] = int(c[0])
	result["min"] = int(c[1])

	d = c[2].split(".")
	result["second"] = int(d[0])
	result["ms"] = int(d[1].split(";")[0])

	return result

def cal_dis(xs, ys, radius):

	rs = []
	num = len(xs) - 1
	factor = radius*2*3.14/360

	for i in range(num):
		rs.append(cal_dif_angle(xs[i+1] - xs[i], ys[i+1] - ys[i])*factor)

	return rs

def draw(ldis, rdis, axle = 180):
	
	#turtle.setup(2000,2000)
	turtle.pensize(1)
	turtle.speed(4)
	turtle.penup()
	turtle.sety(50)
	turtle.setx(-400)
	turtle.left(90)
	turtle.pendown()

	num = len(ldis)
	skip_num = 30*20
	for i in range(skip_num, num):
		lmove, rmove = ldis[i], rdis[i]
		if lmove > 0 and rmove > 0:
			turtle.color("red")
			degree_dif = (ldis[i] - rdis[i])/3.14
			#center_move = (ldis[i]+rdis[i])/2
			center_move = abs(np.sin(3.14/180*degree_dif/2))*(axle/2 + min(lmove, rmove)/abs(lmove - rmove)*180)*2
		elif lmove < 0 and rmove < 0:
			turtle.color("blue")
			degree_dif = (ldis[i] - rdis[i])/3.14
			center_move = -abs(np.sin(3.14/180*degree_dif/2))*(axle/2 - max(lmove, rmove)/abs(lmove - rmove)*180)*2
		else:
			#一正一负
			turtle.color("black")
			degree_dif = 0
			center_move = 0

		#degree_dif = (ldis[i] - rdis[i])/3.14
		#print(degree_dif)
		turtle.right(degree_dif/2)
		#center_move = np.sin(3.14/180*degree_dif)*()
		#print(center_move)
		turtle.fd(center_move/20)
		turtle.right(degree_dif/2)

	#turtle.done()
	ts = turtle.getscreen()
	ts.getcanvas().postscript(file = "track1.eps")

class draw_and_save():

	def __init__(self, ldis, rdis, axle = 180):
		self.ldis = ldis
		self.rdis = rdis
		self.axle = axle
		self.fig, self.ax = plt.subplots()
		self.xdata, self.ydata = [-400], [-200]
		self.ln,  = plt.plot([], [], "ro", animated = True, ms = 1)
		self.angle = 90*np.pi/180

		self.wait_thresh = 5*20
		self.epsilon = 0.1
		self.being_stop = False

		self.stop_x = self.xdata[-1]
		self.stop_y = self.ydata[-1]

	def init(self):
		self.ax.set_xlim(-1500, 1500)
		self.ax.set_ylim(-1500, 1500)
		return self.ln, 

	def update(self, frame):

		lmove, rmove = self.ldis[frame], self.rdis[frame]
		dif_angle = (lmove - rmove)/self.axle
		
		self.angle -= dif_angle/2

		if lmove > self.epsilon and rmove > self.epsilon:
			#self.ln.set_color("r")
			dis = abs(np.sin(dif_angle/2))*(self.axle/2 + min(abs(lmove), abs(rmove))*self.axle/abs(lmove - rmove))
		elif lmove < -self.epsilon and rmove < -self.epsilon:
			#self.ln.set_color("b")
			dis = -abs(np.sin(dif_angle/2))*(self.axle/2 + min(abs(lmove), abs(rmove))*self.axle/abs(lmove - rmove))
		else:
			if not self.being_stop:
				try:
					if (self.xdata[-1] - self.xdata[-self.wait_thresh])**2 + (self.ydata[-1] - self.ydata[-self.wait_thresh])**2 < self.epsilon**2:
						print(self.xdata[-1], self.ydata[-1])
				except:
					print("too early.")
			dis = 0

		if dis and self.being_stop:
			self.being_stop = False

		self.xdata.append(self.xdata[-1] + dis*np.cos(self.angle))
		self.ydata.append(self.ydata[-1] + dis*np.sin(self.angle))	
		self.ln.set_data(self.xdata, self.ydata)
		self.angle -= dif_angle/2

		return self.ln,

	def show(self):
		anim = animation.FuncAnimation(self.fig, self.update, frames = range(len(self.ldis)), interval = 1, init_func = self.init, blit = True)
		#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
		#anim.save('test_animation.html')
		try:
			plt.show()
		except AttributeError:
			print("exit.")
		#plt.savefig("1.jpg")

def main(left_log, right_log, radius = 35, axle = 166):

	left = read_angles(left_log)
	lafter = data_justify(left[0], left[1], left[2])
	ldis = cal_dis(lafter[1], lafter[2], radius)

	right = read_angles(right_log)
	rafter = data_justify(right[0], right[1], right[2])
	rdis = cal_dis(rafter[1], rafter[2], radius)
	rdis = [-i for i in rdis]

	a = draw_and_save(ldis, rdis, axle)
	a.show()
	#draw(ldis, rdis,axle)

if __name__ == "__main__":
	left_log = "left.log"
	right_log = "right.log"
	
	main(left_log, right_log)



