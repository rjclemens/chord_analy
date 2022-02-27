import audiosegment as aus
import matplotlib.pyplot as plt
import numpy as np
import heapq

src = "test.m4a"

num_samples = 10
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def freq_to_note(freq):
  steps = round(12*np.log2(freq/261.63))
  # (note name, octave)
  return (notes[steps % 12], 4+steps//12)

max_val_time = dict()
seg = aus.from_file(src)
# f, time, amp = seg.spectrogram(window_length_s=0.03, overlap=0.5)
f, time, amp = seg.spectrogram(window_length_s=1, overlap=0.5)
amp = 10 * np.log10(amp + 1e-9) # convert to db

# amp: rows freq, cols t; 
amp_t = amp.transpose()

for t, vals in enumerate(amp_t):
  t_int = time[t]
  # use neg. value for max heap
  max_val_time[t_int] = [(-v, f[freq]) for freq, v in enumerate(vals)]
  # print(max_val_time[t_int])
  # sort by a_val in t : (freq, a_val)
  heapq.heapify(max_val_time[t_int])

# print(max_val_time)

count=0
for t in time:
  top_freq = []
  for _ in range(num_samples):
    n_val, f = heapq.heappop(max_val_time[t])
    top_freq.append(freq_to_note(f))
    # print(top_freq)
  max_val_time[t] = top_freq
  print(t, ": ", max_val_time[t], "\n")
  count += 1
  if count==10: break

# print(max_val_time)

plt.pcolormesh(time, f, amp)
plt.xlabel("Time in Seconds")
plt.ylabel("Frequency in Hz")
# plt.show()