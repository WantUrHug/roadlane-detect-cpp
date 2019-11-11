import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Wheel():

	def __init__(self, log, radius, start_t, end_t):

		self.radius = radius

		self.ts, self.xs, self.ys, _ = self._read_components(log)
		anglex = self._angles_gen_v2()
		#plt.plot(anglex)
		#plt.show()
		self.new_ts, self.new_anglex = self._data_justify(anglex, start_t, end_t)

		self.dis = self._cal_dis_v2()
		self._cal_total_dis()

	def _read_components(self, log):

		with open(log, encoding = "utf-8") as file:
			
			a = file.readlines()
			xs = []
			ys = []
			zs = []
			ts = []
			#pprint(len(a))
			for b in a[1:]:
				b = b.split(",")
				#print(b)
				x = float(b[0])
				y = float(b[1])
				z = float(b[2])
				ts.append(self._strptime(b[6][:-2]))
				xs.append(x)
				ys.append(y)
				zs.append(z)
	
		return ts, xs, ys, zs	
	
	def _angles_gen_v2(self):
		#只返回一个x轴的数值
		res = []

		g = 0.98
		bias = 0.1
		for i in range(len(self.xs)):
			x = self.xs[i]
			y = self.ys[i]
			if x > 0:
				if y > 0:
					phi = np.arctan(x/y)*180/np.pi
	
					if x**2+y**2 < 1 + bias:
						res.append(270 + phi)
					elif x**2+y**2 >= 1 + bias:
						val = np.arcsin(1/np.sqrt(x**2+y**2))*180/np.pi
						angle = val - phi
						if 0 < angle < 90:
							res.append(360 - angle)
						else:
							angle = (180 - val) - phi
							res.append(360 - angle)
					else:
						res.append(phi + 270)
				elif y < 0:
					y = -y
					phi = np.arctan(x/y)*180/np.pi
					if x**2+y**2 < 1 + bias:
						res.append(90 - phi)
					else:	
						val = np.arcsin(g/np.sqrt(x**2+y**2))*180/np.pi
						angle = val - phi
						if 0 < angle < 90:
							res.append(angle)
						else:
							angle = (180 - val) - phi
							res.append(angle)
				else:#y = 0
					res.append(0)
			elif x < 0:
				x = -x
				if y > 0:
					phi = np.arctan(x/y)*180/np.pi
					if x**2+y**2 < 1 + bias:
						res.append(270 -  phi)
					else:
						val = np.arcsin(g/np.sqrt(x**2+y**2))*180/np.pi
						angle = val - phi
						if 0 < angle < 90:
							res.append(180 + angle)
						else:
							angle = (180 - val) - phi
							res.append(180 + angle)
				elif y < 0:
					y = -y
					phi = np.arctan(x/y)*180/np.pi
					if x**2+y**2 < 1+ bias:
						res.append(90 + phi)
					else:
						val = np.arcsin(g/np.sqrt(x**2+y**2))*180/np.pi
						angle = val - phi
						if 0 < angle < 90:
							res.append(180 - angle)
						else:
							angle = (180 - val) - phi
							res.append(180 - angle)
				else:
					res.append(180)
			else:#x = 0
				if y >= 0:
					res.append(270)
				else:
					res.append(90)
		return res

	def _strptime(self, string):

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

	def _cal_second(self, t):

		return t["day"]*24*60*60+t["hour"]*60*60+t["min"]*60+t["second"]+t["ms"]/1000

	def _data_justify(self, xs, start_t, end_t, endswith = 0):
		'''
		车轮板的数据频率没有手机那么快，每秒最多就是4-5次，有时甚至只有1次或者0次，所以在插值
		的结果选择上暂时定为4.
		和后续的处理上都需要好好想想如何处理.
		参数中值得注意的是 endswith，表明实际上将在持续的时间后补上多长的时间.
		'''
		
		new_ts = []
		if (start_t["hour"] == end_t["hour"]) and (start_t["day"] == end_t["day"]):
			pass
		else:
			raise ValueError("Not in same hour.")
		start_m = start_t["min"]
		end_m = end_t["min"]
		cm = start_m
		for minute in range(start_m, end_m + 1):
			if cm == start_m:
				if start_m == end_m:
					for second in range(start_t["second"], end_t["second"] + 1):
							for ms in range(0, 1000, 250):
								new_ts.append(build_t(start_t["year"], start_t["month"], start_t["day"], start_t["hour"], minute, second, ms))
				else:
					for second in range(start_t["second"], 60):
							for ms in range(0, 1000, 250):
								new_ts.append(build_t(start_t["year"], start_t["month"], start_t["day"], start_t["hour"], minute, second, ms))
			elif cm == end_m:
				for second in range(0, end_t["second"] + 1):
					for ms in range(0, 1000, 250):
						new_ts.append(build_t(start_t["year"], start_t["month"], start_t["day"], start_t["hour"], minute, second, ms))
			else:
				for second in range(0, 60):
					for ms in range(0, 1000, 250):
						new_ts.append(build_t(start_t["year"], start_t["month"], start_t["day"], start_t["hour"], minute, second, ms))
			cm += 1
	
		#num = len(ts)
		result_x = []
		#result_y = []
	
		ind = 0
		max_ind = len(self.ts)
	
		for i in new_ts:
			ideal = self._cal_second(i)
			#print("a")
			
			while ind + 1 < max_ind:
				flag1 = self._cal_second(self.ts[ind])
				flag2 = self._cal_second(self.ts[ind + 1])
				if flag1 < ideal and flag2 >= ideal:
				
					dx = xs[ind + 1] - xs[ind]
					if dx > 270:
						if flag2 - ideal > ideal - flag1:
							avg_x = (xs[ind] + 360)*(flag2 - ideal)/(flag2 - flag1) + xs[ind + 1]*(ideal - flag1)/(flag2 - flag1)
						else:
							avg_x = xs[ind]*(flag2 - ideal)/(flag2 - flag1) + (xs[ind + 1] - 360)*(ideal - flag1)/(flag2 - flag1)
					elif dx < -270:
						if flag2 - ideal > ideal - flag1:
							avg_x = (xs[ind] - 360)*(flag2 - ideal)/(flag2 - flag1) + xs[ind + 1]*(ideal - flag1)/(flag2 - flag1)
						else:
							avg_x = xs[ind]*(flag2 - ideal)/(flag2 - flag1) + (xs[ind + 1] + 360)*(ideal - flag1)/(flag2 - flag1)
					else:
						avg_x = xs[ind]*(flag2 - ideal)/(flag2 - flag1) + xs[ind + 1]*(ideal - flag1)/(flag2 - flag1)
		
					result_x.append(avg_x)
					#result_y.append(avg_y)
					#ind += 1
					#print("s")
					break
				else:
					ind += 1
					#print("f")
	
		return new_ts, result_x

	def _cal_dis_v2(self):

		rs = []
		num = len(self.new_anglex) - 1
		factor = self.radius*2*3.14/360

		for i in range(num):

			dif = self.new_anglex[i+1] - self.new_anglex[i]
			if dif > 180:
				dif -= 360
			elif dif < -180:
				dif += 360
			rs.append(dif*factor)

		return rs 

	def _cal_total_dis(self):

		self.total_dis = [0]
		for i in self.dis:
			self.total_dis.append(i+self.total_dis[-1])

	def plot(self):

		print(len(self.total_dis))
		plt.plot(self.total_dis)
		plt.show()

class Track():

	def __init__(self, left, right, axle):

		self.ldis = left.dis
		self.rdis = right.dis
		self.rdis = [-i for i in self.rdis]
		self.axle = axle

		self._set_fig()

	def _set_fig(self):

		#self.fig, self.ax = plt.subplots(figsize = (12.8, 7.2))
		self.fig, self.ax = plt.subplots(figsize = (6, 6))
		x_major_locator = plt.MultipleLocator(200)
		y_major_locator = plt.MultipleLocator(200)
		self.ax.xaxis.set_major_locator(x_major_locator)
		self.ax.yaxis.set_major_locator(y_major_locator)
		self.xdata, self.ydata = [0], [0]

		self.ln,  = plt.plot([], [], "ro", animated = True, ms = 1)
		#self.angle = -70*np.pi/180
		self.angle = -90*np.pi/180
		#self._draw_boundary()

		self.epsilon = 0.1
		self.being_stop = False

		self.stop_x = self.xdata[-1]
		self.stop_y = self.ydata[-1]

		self.cnt = 0

	def _draw_boundary(self):
		y = self.ydata[0]- 1000
		plt.plot([0, 114, 114, 776, 776, -775, -775, -114, -114, 0], [-0-y, -0-y, -551-y, -551-y, -1173-y, -1173-y, -551-y, -551-y, 0-y, 0-y], "yellow")

	def init(self):

		self.ax.set_xlim(-500, 500)
		self.ax.set_ylim(-600, 400)
		return self.ln, 

	def update(self, frame):

		lmove, rmove = self.ldis[frame], self.rdis[frame]
		#if self.cnt == 43*20:
		#	self.angle = 145*np.pi/180
		#if self.cnt == 95*20:
		#	self.angle = -55*np.pi/180
		#if self.cnt == 120*20:
		#	self.angle = -15*np.pi/180
		dif_angle = -(lmove - rmove)/self.axle
		
		self.angle += dif_angle/2

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
						#print(self.xdata[-1], self.ydata[-1])
						pass
				except:
					#print("too early.")
					pass
			dis = 0
			#dif_angle = -dif_angle

		if dis and self.being_stop:
			self.being_stop = False

		self.xdata.append(self.xdata[-1] + 2.2*dis*np.cos(self.angle))
		self.ydata.append(self.ydata[-1] + 2.2*dis*np.sin(self.angle))	
		self.ln.set_data(self.xdata, self.ydata)
		self.angle += dif_angle/2

		self.cnt += 1

		return self.ln,

	def show(self, save = False):
		anim = animation.FuncAnimation(self.fig, self.update, frames = range(len(self.ldis)), interval = 1, init_func = self.init, blit = True, repeat = False)
		#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
		if save:
			anim.save('test_animation.mp4', fps = 20, writer ='ffmpeg')
		try:
			plt.show()
		except AttributeError:
			print("exit.")





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

if __name__ == "__main__":
	start_t = build_t(2019, 11, 11, 15, 51, 0, 0)
	end_t = build_t(2019, 11, 11, 15, 54, 59, 0)
	left = Wheel("input2.txt", 4.6, start_t, end_t)
	right = Wheel("input1.txt", 4.6, start_t, end_t)
	#left.plot()
	track = Track(left, right, 20)
	track.show()