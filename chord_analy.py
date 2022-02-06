import audiosegment as aus
import matplotlib.pyplot as plt
import numpy as np

src = "test.m4a"

max_val_time = dict()
seg = aus.from_file(src)
f, time, amp = seg.spectrogram(window_length_s=0.03, overlap=0.5)
amp = 10 * np.log10(amp + 1e-9) # convert to db

# amp: rows freq, cols t; 
amp_t = amp.transpose()
for t, vals in enumerate(amp_t):
  t_int = time[t]
  max_val_time[t_int] = (f[freq_i], a_val) for freq_i, a_val in enumerate(vals)
  print(max_val_time[t_int])
  # sort by a_val in t : (freq, a_val)
  max_val_time[t_int] = sorted(max_val_time[t_int], key = lambda x: x[1])

print(max_val_time)
plt.pcolormesh(time, f, amp)
plt.xlabel("Time in Seconds")
plt.ylabel("Frequency in Hz")
plt.show()