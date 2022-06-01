# M1 0
# M2 -4
# M3 +5
# M4 +8

import numpy as np
from math import cos, sin, pi, floor
import matplotlib.pyplot as plt

o2, o3, o4 = -4, 5, 8

class Segment:
	def __init__(self, length, angle, mina, maxa, start=None):
		self.length = length
		self.angle = angle
		self.min = mina
		self.max = maxa
		self.start = start

	def setAngle(self, angle):
		self.angle = angle

		# Correct possible out of boundaries errors
		if(self.angle < self.min):
			self.angle = self.min
		if(self.angle > self.max):
			self.angle = self.max

	def rotate(self, rotation):
		self.setAngle(self.angle + rotation)

class Braccio:
	def __init__(self, shoulderAngle, elbowAngle, wristAngle):
		self.base = np.radians(90)
		self.segments = {
			"shoulder": Segment(13, np.radians(shoulderAngle), np.radians(15), np.radians(165), np.array([0, 0])),
			"elbow": Segment(12.5, np.radians(elbowAngle - 90), np.radians(0 - 90), np.radians(180 - 90)),
			"wrist": Segment(19.5, np.radians(wristAngle - 90), np.radians(0 - 90), np.radians(180 - 90))
		}

		self.ends = {
			"shoulder": self.getShoulderEnd,
			"elbow": self.getElbowEnd,
			"wrist": self.getWristEnd
		}

		self.starts = {
			"shoulder": self.getShoulderStart,
			"elbow": self.getElbowStart,
			"wrist": self.getWristStart
		}

	def getShoulderStart(self):
		return self.segments["shoulder"].start

	def getShoulderEnd(self):
		shoulderStart = self.segments["shoulder"].start
		shoulderLength = self.segments["shoulder"].length
		shoulderAngle = self.segments["shoulder"].angle

		end = np.array([shoulderStart[0] + shoulderLength * cos(shoulderAngle), shoulderStart[1] + shoulderLength * sin(shoulderAngle)])

		return end

	def getElbowEnd(self):
		shoulderAngle = self.segments["shoulder"].angle
		shoulderEnd = self.getShoulderEnd()

		elbowLength = self.segments["elbow"].length
		elbowAngle = self.segments["elbow"].angle

		end = np.array([shoulderEnd[0] + elbowLength * cos(shoulderAngle + elbowAngle), shoulderEnd[1] + elbowLength * sin(shoulderAngle + elbowAngle)])

		return end

	def getWristEnd(self):
		shoulderAngle = self.segments["shoulder"].angle
		
		elbowAngle = self.segments["elbow"].angle
		elbowEnd = self.getElbowEnd()

		wristStart = self.segments["wrist"].start
		wristLength = self.segments["wrist"].length
		wristAngle = self.segments["wrist"].angle

		end = np.array([elbowEnd[0] + wristLength * cos(shoulderAngle + elbowAngle + wristAngle), elbowEnd[1] + wristLength * sin(shoulderAngle + elbowAngle + wristAngle)])

		return end

	def getShoulderStart(self):
		return self.segments["shoulder"].start

	def getElbowStart(self):
		return self.getShoulderEnd()

	def getWristStart(self):
		return self.getElbowEnd()

	def setAngles(self, shoulderAngle, elbowAngle, wristAngle):
		self.segments["shoulder"].setAngle(np.radians(shoulderAngle))
		self.segments["elbow"].setAngle(np.radians(elbowAngle - 90))
		self.segments["wrist"].setAngle(np.radians(wristAngle - 90))

	def flip(self):
		shoulder = self.segments["shoulder"]
		elbow = self.segments["elbow"]
		wrist = self.segments["wrist"]

		shoulder.rotate(2 * (np.radians(90) - shoulder.angle))
		elbow.rotate(2 * (np.radians(0) - elbow.angle))
		wrist.rotate(2 * (np.radians(0) - wrist.angle))

def drawArm(braccio, target=[0, 0]):
	shoulderStart = braccio.getShoulderStart()
	shoulderEnd = braccio.getShoulderEnd()

	# print("\nShoulder: ", shoulderStart, shoulderEnd)

	elbowStart = shoulderEnd
	elbowEnd = braccio.getElbowEnd()

	# print("Elbow: ", elbowStart, elbowEnd)

	wristStart = elbowEnd
	wristEnd = braccio.getWristEnd()

	# print("Wrist: ", wristStart, wristEnd)

	fig = plt.figure()
	plt.ylim(-50, 50)
	plt.xlim(-50, 50)

	plt.plot([shoulderStart[0], shoulderEnd[0]], [shoulderStart[1], shoulderEnd[1]], "r")
	plt.plot([elbowStart[0], elbowEnd[0]], [elbowStart[1], elbowEnd[1]], "y")
	plt.plot([wristStart[0], wristEnd[0]], [wristStart[1], wristEnd[1]], "b")
	plt.plot(target[0], target[1], "b", marker="o")

	plt.show()

def angleFromVector(endEffector, target, origin = np.array([0, 0])):
	a = endEffector - origin
	b = target - origin

	normA = np.sqrt(a[0]**2 + a[1]**2)
	normB = np.sqrt(b[0]**2 + b[1]**2)

	tmp = np.dot(a, b) / (normA * normB)
	angle = np.arccos(tmp)

	if np.cross(a, b) < 0:
		angle = -angle

	if angle > 180:
		angle = angle - 360

	return angle

def ccd(braccio, target, iterations=10000, precision=0.1):
	error = precision + 1
	endEffector = None
	i = 0
	while error > precision and i < iterations:
		for name, seg in reversed(braccio.segments.items()):
			origin = braccio.starts[name]()
			endEffector = braccio.getWristEnd()

			rotation = angleFromVector(endEffector, target, origin)

			seg.rotate(rotation)
			# drawArm(braccio, target)

		error = np.sqrt((endEffector[0] - target[0])**2 + (endEffector[1] - target[1])**2)
		i += 1


def newtonMethod(braccio, target, iterations=500):
	epsilon = [1, 1]

	shoulderAngle = braccio.segments["shoulder"].angle
	elbowAngle = braccio.segments["elbow"].angle
	wristAngle = braccio.segments["wrist"].angle
	theta = [shoulderAngle, elbowAngle, wristAngle]

	shoulderLength = braccio.segments["shoulder"].length
	elbowLength = braccio.segments["elbow"].length
	wristLength = braccio.segments["wrist"].length

	for i in range(iterations):
		guess = braccio.getWristEnd()
		error = np.array((target[0] - guess[0], target[1] - guess[1]))

		jacobian = np.array((
			[-np.sin(theta[0])*shoulderLength, -np.sin(theta[1])*elbowLength, -np.sin(theta[2])*wristLength], 
			[np.cos(theta[0])*shoulderLength, np.cos(theta[1])*elbowLength, np.cos(theta[2])*wristLength]
		))

		inv = np.linalg.pinv(jacobian)
		theta += np.dot(inv, error)

		if np.abs(target[0] - guess[0]) < epsilon[0] and np.abs(target[1] - guess[1]) < epsilon[1]:
			return theta

	return theta

def baseRotation(braccio, x, z):
	a = np.array([x, z])
	b = np.array([1, 0])

	angle = angleFromVector(a, b)

	return np.cos(angle) * x - np.sin(angle) * z, angle

def ik(braccio, target):
	x, y, z = target

	# if x > 0:
	# 	# x, baseAngle = baseRotation(braccio, x, z)
	# 	ccd(braccio, np.array([-x, y], dtype="float64"))
	# 	braccio.flip()
	# 	# braccio.base += baseAngle
	# else:
	# 	# x, baseAngle = baseRotation(braccio, x, z)
	# 	ccd(braccio, np.array([x, y], dtype="float64"))
	# 	# braccio.base += baseAngle
	ccd(braccio, np.array([x, y], dtype="float64"))

	drawArm(braccio, [x, y])

def test():
	angles = []
	braccio = Braccio(90, 90, 90)
	target = np.array([15, 12, 0], dtype="float64")
	ik(braccio, target)
	angles.append([floor(np.degrees(braccio.base)) ,floor(np.degrees(braccio.segments["shoulder"].angle)), floor(90-np.degrees(braccio.segments["elbow"].angle)+5), floor(90-np.degrees(braccio.segments["wrist"].angle))])

	# print(f"Braccio.ServoMovement(20, {angle[0]}, {165-angle[1]+o2}, {angle[2]+o3}, {angle[3]+o4}, 90, 73);")
	for angle in angles:
		print(f"Braccio.ServoMovement(20, {angle[0]}, {165-angle[1]+o2}, {angle[2]+o3}, {angle[3]+o4}, 90, 73);")


test()