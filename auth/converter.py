import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd
import math
import cmath

fs = 44100
data = []
segments = []
final = []

def read():
	# print('rec')
	# n_data = sd.rec(2 * fs, samplerate=fs, channels=1)
	# sd.wait()
	# print('play')
	# sd.play(n_data, fs)
	# sd.wait()
	n_data = sf.read('kostya_voice.wav')
	global data 
	data = [0 for i in range(0, len(n_data[0]))]
	# print(n_data)
	for i in range(0, len(data)):
		data[i] = n_data[0][i]

def normalize():
	mx = -100
	for it in data:
		mx = max(mx, it)
	for it in data:
		it /= mx

def hemming(id):
	for i in range(0, LEN):
		segments[id][i] *= 0.53836 - 0.46164 * math.cos(2 * math.pi * i / LEN)


def fft(id, inv):
	res = []
	cntdots = 1000
	for i in range(0, cntdots):
		s = complex(0, 0)
		for j in range(0, LEN):
			s += segments[id][j] * cmath.exp(-2j * math.pi * i * j / LEN)
		res.append(s.real)
	return res
	

def convert(id):
	hemming(id)
	segments[id] = fft(id, 0)

read()
normalize()

LEN = fs // 10
print(LEN)
print(len(data))
for i in range(LEN, len(data), LEN // 2):
	if i + LEN >= len(data):
		break
	segments.append(data[i:i + LEN])
	convert(len(segments) - 1)

for i in range(0, len(segments[0])):
	sr = 0
	for j in range(0, len(segments)):
		sr += segments[j][i]
	sr /= len(segments)
	final.append(sr)
plt.plot(final)
plt.show()