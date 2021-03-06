#swaps every pedal press event with the note event occurring immediatley after in the track, fixing the pedal problems in VSTs like Kontakt Pianos and Pianoteq

from mido import MidiFile
import sys

if len(sys.argv) is not 2:
    print("usage: python3 pedalfix.py <file>")
    sys.exit()

debug = False

print("processing...")

save_str = sys.argv[1]
index = save_str.rindex("\\") + 1
if index > 0:
    save_str = save_str[:index] + "pf_" + save_str[index:]
else:
    save_str = "pf_" + sys.argv[1]

mid = MidiFile(sys.argv[1])

temp_time = 0
skip_toggle = False

for i, track in enumerate(mid.tracks):
    index = 0
    for msg in track:
        b = msg.bytes()
		# if bytes in msg indicate pedal (64) and pressed (127)
        if b[1] is 64 and b[2] is 127 and skip_toggle is False: 
            # swap with the next msg in midi file, meaning note
            next_msg = track[index + 1] # get next message
            prev_msg = msg
            msg = next_msg # set current slot to next msg
            temp_time = msg.time
            msg.time = prev_msg.time
            skip_toggle = True
        elif skip_toggle is True:
            skip_toggle = False    
            msg = prev_msg    
            msg.time = temp_time
        if debug is True:
            print(msg)
        index = index + 1

print("done.")

print("Saved as \"" + save_str + "\"")
mid.save(save_str)
