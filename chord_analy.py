import audiosegment as aus
import matplotlib.pyplot as plt
import numpy as np
import heapq

src = "test.m4a"

num_samples = 10
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'B#', 'B']
placed = dict()


def set_note_oct():
    note_oct = []
    for i in range(3, 5):
        for note in notes:
            note_oct += [(note, i)]
    note_oct.reverse()
    return note_oct


def conv_note(notes):
    for note in notes:
        placed[note] = "O" if len(note) == 1 else "O#"


def plotter(note_oct):
    it = iter(note_oct)
    for note in it:
        print("  " + placed.get(note, "  ") + "  |")
        if note == ('G', 4):
            print("~~" + placed.get(next(it), "~~") + "~~|")
        else:
            print("--" + placed.get(next(it), "--") + "--|")


def plot(notes, note_oct):
    conv_note(notes)
    plotter(note_oct)


def freq_to_note(freq):
    steps = round(12*np.log2(freq/261.63))
    # (note name, octave)
    return (notes[steps % 12], 4+steps//12, steps)


def not_in_range(st1, st2, eps, num):
    return not (st1-eps <= num <= st1+eps or st2-eps <= num <= st2+eps)


def main():
    note_oct = set_note_oct()
    print("n", note_oct)
    max_val_time = dict()
    seg = aus.from_file(src)
    # f, time, amp = seg.spectrogram(window_length_s=0.03, overlap=0.5)
    f, time, amp = seg.spectrogram(window_length_s=1, overlap=0.5)
    amp = 10 * np.log10(amp + 1e-9)  # convert to db

    # amp: rows freq, cols t;
    amp_t = amp.transpose()

    for t, vals in enumerate(amp_t):
        t_int = time[t]
        # use neg. value for max heap
        max_val_time[t_int] = [(-v, f[freq]) for freq, v in enumerate(vals)]
        # sort by a_val in t : (freq, a_val)
        heapq.heapify(max_val_time[t_int])

    for t in time:
        top_freq = []
        for _ in range(num_samples):
            n_val, f = heapq.heappop(max_val_time[t])
            top_freq.append(freq_to_note(f))

        # remove all elements within one note of two strongest values
        st1, st2 = top_freq[0], top_freq[1]
        top_freq = [st1, st2] + \
            list(filter(lambda a: not_in_range(
                st1[2], st2[2], 1, a[2]), top_freq))
        # max_val_time[t] = ((x[0], x[1]) for x in top_freq)
        max_val_time[t] = [(x[0], x[1]) for x in top_freq]
        print(t, ": ", max_val_time[t], "\n")

        print(note_oct)
        plot(max_val_time[t], note_oct)
        break


# print(max_val_time)

# plt.pcolormesh(time, f, amp)
# plt.xlabel("Time in Seconds")
# plt.ylabel("Frequency in Hz")
# plt.show()

if __name__ == "__main__":
    main()
