from moviepy.editor import VideoFileClip, vfx, clips_array

bottom = VideoFileClip("bottom.mp4") # import the video that will be at the bottom
mirrored_bottom = bottom.resize(0.5).fx(vfx.mirror_x) # mirror the video

top = VideoFileClip("top.mp4").resize(0.5)      # import the video that will be at the top

#find some way to sync both audios and delete the audio of bottom

final_clip = clips_array([[top],
                          [mirrored_bottom]])
audio_top = top.audio

final_clip = final_clip.set_audio(audio_top)

final_clip.resize(width=1920).write_videofile("my_video.mp4")

