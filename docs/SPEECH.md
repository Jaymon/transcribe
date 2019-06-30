# Speech Command

Running `transcribe speech` should result in something like:


```
$ transcribe speech "/path/to/sound_file.mp3" --stop="00:01:00"
[I] Stopping audio at 0:01:00
[I] Converting /path/to/sound_file.mp3 to ogg at /tmp/sound_file.ogg
[I] Uploading /tmp/sound_file.ogg to Google cloud storage bucket NAME-NNNNNN
[I] Google cloud storage uri gs://NAME-NNNNNN/sound_file.ogg
[I] Beginning transcription
[I] Transcription finished in 0:00:33
[I] Deleting file from Google cloud storage gs://NAME-NNNNNN/sound_file.ogg
0:00:00        here is some text from the sound_file that was transcribed ...
0:00:19        some more text ...
...
```

It prints the transcript to stdout, so you can redirect it to a file to save it:

```
$ transcribe speech sound_file.mp3 > transcription.txt
```