# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import re
import logging
import time
import datetime

import pydub # https://github.com/jiaaro/pydub
from google.cloud import storage
from google.cloud.exceptions import NotFound
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from .path import Path, TempPath
from .utils import Time, String


logger = logging.getLogger(__name__)


class SpeechPath(Path):
    regex = re.compile(r"\.(?:mp3|wav|flac)$", re.I)

    def is_type(self):
        return True if self.regex.search(self) else False


class Speech(object):
    """Wrapper around Google's speech api

    https://cloud.google.com/speech
    https://cloud.google.com/speech/docs/reference/libraries#client-libraries-usage-python
    https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/speech/
    https://cloud.google.com/speech/support
    https://cloud.google.com/speech/docs/best-practices
    """

    TIMEOUT = 10800

    @property
    def text(self):
        return self._text

    @property
    def lines(self):
        return self.text.splitlines(False)

    @property
    def words(self):
        return self._words

    def __init__(self, path, lang):
        self.path = path
        self.lang = lang

    def _convert(self, path, start, stop):
        audio_format = "ogg"
        # https://github.com/jiaaro/pydub/blob/master/pydub/audio_segment.py
        audio = pydub.AudioSegment.from_file(path)
        if bool(start) or bool(stop):
            start = Time(start)
            stop = Time(stop)
            if start and not stop:
                logger.info("Starting audio at {}".format(start))
                audio = audio[start.total_ms:]
            elif stop and not start:
                logger.info("Stoping audio at {}".format(stop))
                audio = audio[:stop.total_ms:]
            else:
                logger.info("Slicing audio {} - {}".format(start, stop))
                audio = audio[start.total_ms:stop.total_ms]

            tp = TempPath(
                "{}-{}-{}".format(
                    path.name,
                    start.total_seconds,
                    stop.total_seconds
                ),
                audio_format
            )

        else:
            tp = TempPath(path.name, audio_format)

        logger.info("Converting {} to {} at {}".format(path, audio_format, tp))

        # https://cloud.google.com/speech/docs/basics#audio-encodings
        # https://superuser.com/questions/516806/how-to-encode-audio-with-opus-codec
        #audio.export(tp, format=audio_format, codec="opus", parameters=["-strict", "-2"])
        ogg_audio = pydub.AudioSegment.from_file(
            audio.export(tp, format=audio_format, codec="libopus", parameters=["-ac", "1"])
        )

        return tp, ogg_audio

    def _upload(self, path):
        # https://cloud.google.com/python/getting-started/using-cloud-storage
        # https://github.com/GoogleCloudPlatform/google-cloud-python/
        # https://cloud.google.com/storage/docs/object-basics
        # https://googlecloudplatform.github.io/google-cloud-python/latest/storage/client.html
        storage_client = storage.Client()
        bucket_name = storage_client.project
        logger.info("Uploading {} to Google cloud storage bucket {}".format(path, bucket_name))

        try:
            bucket = storage_client.get_bucket(bucket_name)

        except NotFound:
            bucket = storage_client.create_bucket(bucket_name)

        filename = path.safename
        blob = bucket.blob(filename)
        blob.upload_from_string(path.contents(), path.mimetype)
        #public_url = blob.public_url
        # super convenient google doesn't bother with a .uri property for a
        # thing that seems to be pretty commonly needed
        # https://stackoverflow.com/a/25373496/5006
        uri = "gs://{}/{}".format(bucket_name, blob.name)
        logger.info("Google cloud storage uri {}".format(uri))
        return uri, blob

    def _transcribe(self, uri, audio):
        client = speech.SpeechClient()

        # NOTE -- according to https://cloud.google.com/speech/quotas  we are
        # limited to ~180 Minutes
        recog = types.RecognitionAudio(uri=uri)
        # https://cloud.google.com/speech/reference/rest/v1/RecognitionConfig
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=audio.frame_rate,
            language_code=self.lang,
            enable_word_time_offsets=True
        )

        # https://cloud.google.com/speech/docs/async-recognize
        # https://googlecloudplatform.github.io/google-cloud-python/latest/speech/index.html#asynchronous-recognition
        operation = client.long_running_recognize(config, recog)

        start = time.time()
        logger.info('Beginning transcription')
        response = operation.result(timeout=self.TIMEOUT)
        stop = time.time()
        logger.info("Transcription finished in {}".format(Time(stop - start)))
        return response

    def scan(self, start=0, stop=0):
        path = self.path
        path, audio = self._convert(path, start, stop)
        uri, blob = self._upload(path)
        self.response = self._transcribe(uri, audio)
        logger.info("Deleting file from Google cloud storage {}".format(uri))
        blob.delete() # https://cloud.google.com/storage/docs/object-basics
        return self.response

    def __iter__(self):
        for result in self.response.results:
            alternative = result.alternatives[0]
            text = String(alternative.transcript).flow()

            # https://cloud.google.com/speech/docs/async-time-offsets
            word_info = alternative.words[0]
            # TODO -- we have a nanos property also, do we care about
            # nanoseconds?
            start_time = Time(word_info.start_time.seconds)
            yield start_time, text

#         for result in response.results:
#             # The first alternative is the most likely one for this portion.
#             print(result.alternatives[0].transcript)
#             #print('Confidence: {}'.format(result.alternatives[0].confidence))

