
## audacity-py-multitone

This is a first working implementation of scripting using the new mod-script-pipe in Audacity 3.4.2.
It expects Python 3 and utilizes a Jinja2 template. Edit the JSON configuration as desired.
All tones in each "mixed track" configuration are written to an audio file ('.ogg' in this case).

#### simple notes:
Audacity should be open and blank (no tracks).
The existing Jinja2 template creates each of a duration of frequencies,
then combines/mixes them into a single track, writes this to
a file containing the name in JSON as _tone_data.mixed_track_
and then deletes the track from the window.
