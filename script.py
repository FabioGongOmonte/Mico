from moviepy.editor import VideoFileClip, vfx, clips_array
from audio_offset_finder.audio_offset_finder import find_offset_between_files
import proglog
from io import BytesIO
from werkzeug.utils import secure_filename

def mico_videos(bot_location, top_location, mirror_bot=True, mirror_top=False):
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
    final_clip = final_clip.subclip(t_end = bottom.duration)
    

    final_clip.resize(width = bottom.w + bottom.w).write_videofile("mico_video.mp4", logger=proglog.TqdmProgressBarLogger(print_messages=False))
    final_clip.close()
    top.close()
    bottom.close()
    
def mico_sync(bot_location, top_location):

    bottom = VideoFileClip(bot_location)
        
    top = VideoFileClip(top_location)

    #Sync the music

    results = find_offset_between_files(bot_location, top_location)
    offset = abs(results["time_offset"])

    bottom = bottom.subclip(t_start = offset)

    final_clip = bottom.set_audio(top.audio)
    final_clip = final_clip.subclip(t_end = bottom.duration)
    
    final_clip.write_videofile("mico_video.mp4", logger=proglog.TqdmProgressBarLogger(print_messages=False))
    final_clip.close()
    top.close()
    bottom.close()