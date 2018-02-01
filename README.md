# Transcribe

1. _verb_ - To convert a representation of language to another representation.
2. _noun_ - Command line application to extract plain text from images and audio files, written in Python.

## OCR

To extract the text from an image:

    $ transcribe ocr /path/to/image.jpg


## Speech

To extract the text from an audio file:

    $ transcribe speech /path/to/audio.mp3


## Installation

### Google Cloud setup

Transcribe uses Google's cloud services to perform the text extraction, that means you have to setup a Google cloud project. Below is roughly how I did that...

I went to [The console](https://console.cloud.google.com)

Selected _Project_ in the top left corner (to the right of _Google Cloud Platform_) and then create a new project, wait a bit for it to create the project and switch to it (this took like 20 seconds while I was trying to figure out what the heck was going on). Then activate the vision and speech apis (I think storage is automatically activated) and then select Credentials, and create an api key. [More auth info here](https://cloud.google.com/vision/docs/common/auth).

Turns out I also needed to [create a service json file](https://cloud.google.com/storage/docs/authentication#generating-a-private-key). To do this I needed to go to [the dashboard for the project](https://console.cloud.google.com/apis/credentials?project=vision-157908) and then click __Create credentials__ and choose __Service account key__.

Then add this to your `.bash_profile` or something similar:

```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"
```

### ffmpeg

If you're on a Mac and you use Homebrew, you can install ffmpeg like:

    $ brew install --with-opus ffmpeg

If you're not on a Mac or don't use Homebrew you're on your own.


### Transcribe

Install using pip:

    $ pip install transcribe

or the latest and greatest:

    $ pip install "git+https://github.com/Jaymon/transcribe#egg=transcribe"

