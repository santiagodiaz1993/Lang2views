#!/usr/bin/env python
# coding=utf-8

import json
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube, Caption, captions, CaptionQuery
import pytube

link = "https://www.youtube.com/watch?v=O_WbmIIy4vk"
YoutubeVideo = YouTube(link)


print("This is the tile")
print(YoutubeVideo.title)

print("This is the description")
print(YoutubeVideo.description)


# print(YoutubeVideo.caption_tracks)
# YoutubeVideo.download()


# caption1 = Caption(
#     {
#         "baseurl": "http://www.youtube.com",
#         "url": "http://www.youtube.com/watch?v=O_WbmIIy4vk",
#         "name": {"simpleText": "name1"},
#         "languageCode": "en",
#         "vssId": ".en",
#     }
# )

# caption1.download("cap")
# caption1.xml_captions()

# caption1.generate_srt_captions()
#
# CaptionQuery(captions=[caption1])
#
# print(CaptionQuery(captions=[caption1])["en"])
#
# print(
#     caption1.download(
#         "captions", True, "/home/santiago/Documents/lang2views_project/captions"
#     )
# )
# print(caption1.xml_captions())


# def test_float_to_srt_time_format():
#     caption1 = Caption(
#         {
#             "url": "url1",
#             "name": {"simpleText": "name1"},
#             "languageCode": "en",
#             "vssId": ".en",
#         }
#     )
#     print(caption1.download("video"))
#     assert caption1.float_to_srt_time_format(3.89) == "00:00:03,890"
#

# test_float_to_srt_time_format()


print("these are the captions")
for caption in YoutubeVideo.caption_tracks:
    print(caption)

# stream = YouTube.streams.first()
# stream.download("~/Documents/lang2views_project/videos")


# class LocalizedVideo(YoutubeVideo):
#     def __init__(self):
#
#         # how to get the description
#         self.description = yt.description
#         print(yt.description)
#
#         # how to get the title
#         self.title = yt.title
#         print(yt.title)
#
#         # we need a function that creates the scenes
#         # for this we need to go word by word and see the exact time at which
#         # each word is recorded. For this we can make a dictionary with the
#         # list of words and their time. Then look for the gaps and make the
#         # scenes every 20-30 seconds. The time range can be a setting
#         #
#         # how to get the script
#         # YouTubeTranscriptApi.get_transcript("K7BVDfXdgOY")
#
#         # how to know what scripts languages are avaliable
#         # transcript_list = YouTubeTranscriptApi.list_transcripts("K7BVDfXdgOY")
#
#
# # kurts_video = Video()
