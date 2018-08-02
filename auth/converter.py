import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd
import math
import cmath
import sys
import os

fs = 44100
data = []
segments = []
real_part = []
imag_part = []
final = []
print('whats your name');
NAME = input();

def read():
	# print('rec')
	# n_data = sd.rec(2 * fs, samplerate=fs, channels=1)
	# sd.wait()
	# print('play')
	# sd.play(n_data, fs)
	# sd.wait()
	# # print(n_data.shape)
	n_data = sf.read(NAME + '_voice.wav') # if use this, use n_data[0]
	n_data = n_data[0]
	# n_data = []
	# for i in range(0, fs * 2):
	# 	n_data.append(math.sin(10 * 2 * math.pi * i / fs) + 0.5 * math.sin(5 * 2 * math.pi * i / fs))
	# plt.plot(n_data)
	# plt.show()
	# sf.write(NAME + '_voice.wav', n_data, samplerate=fs);
	global data 
	data = [0 for i in range(0, len(n_data))]
	# print(data)
	for i in range(0, len(data)):
		data[i] = n_data[i]

def normalize(val):
	mx = -100
	for it in val:
		mx = max(mx, abs(it))
	for i in range(0, len(val)):
		val[i] /= mx

def hemming(id):
	pass
	for i in range(0, LEN):
		segments[id][i] *= 0.53836 - 0.46164 * math.cos(2 * math.pi * i / LEN)


def fft(A):
	if len(A) == 1:
		return A
	n =	len(A)
	a, b = [], []
	for i in range(0, n):
		if (i % 2 == 0):
			a.append(A[i])
		else:
			b.append(A[i])
	a = fft(a)
	b = fft(b)
	pw = complex(1)
	w = complex(math.cos(2 * math.pi / n), math.sin(2 * math.pi / n))	
	for i in range(0, n // 2):
		A[i] = a[i] + pw * b[i]
		A[i + n // 2] = a[i] - pw * b[i]
		pw *= w
	return A
	

def convert(id):
	hemming(id)
	segments[id] = fft(segments[id])

read()
normalize(data)
LEN = fs // 5
for i in range(0, len(data), LEN // 2):
	if i + LEN >= len(data):
		break
	segments.append(data[i:i + LEN])
	convert(len(segments) - 1)

for i in range(0, LEN):
	sr = 0
	si = 0
	for j in range(0, len(segments)):
		sr += segments[j][i].real
		si += segments[j][i].imag
	sr /= len(segments)
	si /= len(segments)
	real_part.append(sr)
	imag_part.append(si)
normalize(real_part)
normalize(imag_part)
# plt.plot(data)
plt.plot(real_part, 'b')
# plt.plot(imag_part[0: 30], 'r')
plt.savefig(NAME + '_fft.png')
plt.show()