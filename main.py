from moviepy.editor import VideoFileClip, vfx, clips_array
from audio_offset_finder.audio_offset_finder import find_offset_between_files
import os

def path(test_file):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), test_file))

bottom_name = "bottom.mp4"
top_name = "top.mp4"

mirror_top = False
mirror_bot = False

if mirror_bot:
    bottom = VideoFileClip(bottom_name).resize(0.5).fx(vfx.mirror_x) # mirror the video
else:
    bottom = VideoFileClip(bottom_name).resize(0.5)
    
if mirror_top:
    top = VideoFileClip(top_name).resize(0.5).fx(vfx.mirror_x)
else:
    top = VideoFileClip(top_name).resize(0.5)

#Sync the music

results = find_offset_between_files(path("bottom.mp4"), path("top.mp4"))
offset = abs(results["time_offset"])

bottom = bottom.subclip(t_start = offset)

final_clip = clips_array([[top],
                          [bottom]])
audio_top = top.audio

final_clip = final_clip.set_audio(audio_top)
final_clip = final_clip.subclip(t_end = 10)

final_clip.resize(width = bottom.w + bottom.w).write_videofile("my_video.mp4")

