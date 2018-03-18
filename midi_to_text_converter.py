import midi
import os


# reading the midi file
midi_original = midi.read_midifile("original_song.mid")
chunk_list = []

# prints the original data of the midi file 
print str(midi_original[1])


for i, part in enumerate(midi_original[1]):

  chunk_str = ""

  # data in the text file which contains the tick, channel and the velocity value which is stored in a data array

  if (part.name == "Note On"):
    chunk_str = chunk_str + str(part.tick) + "_" + "no" + "_" + str(part.pitch) + \
                  "_" + str(part.data[0]) + "_" + str(part.data[1])

    chunk_list.append(chunk_str)

  # data in the text file which contains the tick, channel and data value
  elif (part.name == "Control Change"):
    chunk_str = chunk_str + str(part.tick) + "_" + "cc" + "_" + str(part.channel)  + "_" + \
                    str(part.data[0]) + "_" + str(part.data[1])
    chunk_list.append(chunk_str)

# storing all this data in song.txt

f = open('song.txt', 'w')
for j in chunk_list:
  f.write(str(j) + "\n")
f.close()