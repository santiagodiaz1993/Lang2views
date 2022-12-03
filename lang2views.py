#!/usr/bin/env python
# coding=utf-8

# what functions are the most important right now?
# 1. Create the scripts
# 2. Auto translate the script
# 2. Edit script (time )

# so we want to create a video object that contains:
# 1. The video
# 2. The audio
# 3. The script
# 4. The title
# 5. The description
# 6. The voice over
# 7. The number of voices


# what do we have to do to create the video object
# 1. Download the video
# 2. Download the script

import whisper
from stable_whisper import modify_model
from stable_whisper import load_model
import json
import whisper
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import pytube


# using whisper to get word timings
# https://github.com/openai/whisper/discussions/3
# https://github.com/openai/whisper/discussions/435


class Video:
    def __init__(self):
        link = "https://www.youtube.com/watch?v=K7BVDfXdgOY&t=474s&ab_channel=KurtCaz"

        yt = YouTube(link)

        stream = yt.streams.first()

        stream.download("~/Documents/lang2views_project/videos")

        caption = yt.captions.get_by_language_code("en")
        print(caption.generate_srt_captions())

        # how to get the script
        # YouTubeTranscriptApi.get_transcript("K7BVDfXdgOY")

        # how to know what scripts languages are avaliable
        # transcript_list = YouTubeTranscriptApi.list_transcripts("K7BVDfXdgOY")

        # how to get the description
        self.description = yt.description
        print(yt.description)

        # how to get the title
        self.title = yt.title
        print(yt.title)

        model = whisper.load_model("base")
        assert model.transcribe("dot.mp3").get("segments")

        model = load_model("base")
        # modified model should run just like the regular model but with additional hyperparameters and extra data in results
        results = model.transcribe("dot.mp3")
        stab_segments = results["segments"]
        first_segment_word_timestamps = stab_segments[1]["whole_word_timestamps"]

        print(stab_segments[0])
        for i in range(0, len(stab_segments)):
            print(stab_segments[i]["whole_word_timestamps"])

        # we need a function that creates the scenes
        # for this we need to go word by word and see the exact time at which
        # each word is recorded. For this we can make a dictionary with the
        # list of words and their time. Then look for the gaps and make the
        # scenes every 20-30 seconds. The time range can be a setting
        #


kurts_video = Video()
