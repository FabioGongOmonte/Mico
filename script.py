from moviepy.editor import VideoFileClip, vfx, clips_array
from audio_offset_finder.audio_offset_finder import find_offset_between_files
from io import BytesIO
from tempfile import NamedTemporaryFile

def mico_videos(bot_location, top_location, mirror_bot=False, mirror_top=False):
    if mirror_bot:
        bottom = VideoFileClip(bot_location).resize(0.5).fx(vfx.mirror_x) # mirror the video
    else:
        bottom = VideoFileClip(bot_location).resize(0.5)
        
    if mirror_top:
        top = VideoFileClip(top_location).resize(0.5).fx(vfx.mirror_x)
    else:
        top = VideoFileClip(top_location).resize(0.5)

    #Sync the music

    results = find_offset_between_files(bot_location, top_location)
    offset = abs(results["time_offset"])

    bottom = bottom.subclip(t_start = offset)

    final_clip = clips_array([[top],
                            [bottom]])
    audio_top = top.audio

    final_clip = final_clip.set_audio(audio_top)
    final_clip = final_clip.subclip(t_end = 10)
    
    final_clip.resize(width = bottom.w + bottom.w).write_videofile("mico_video.mp4")