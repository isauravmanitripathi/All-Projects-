import json
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import os
import sys

def get_subtitle_preferences():
    # Ask if subtitles are wanted
    while True:
        want_subtitles = input("Do you want subtitles in the video? (y/n): ").lower().strip()
        if want_subtitles in ['y', 'n']:
            break
        print("Please enter 'y' or 'n'")
    
    if want_subtitles == 'n':
        return None
    
    # Get position preference
    while True:
        position = input("Where do you want the subtitles? (center/bottom): ").lower().strip()
        if position in ['center', 'bottom']:
            break
        print("Please enter 'center' or 'bottom'")
    
    # Get size preference
    while True:
        size = input("What size do you want the subtitles? (small/big): ").lower().strip()
        if size in ['small', 'big']:
            break
        print("Please enter 'small' or 'big'")
    
    # Convert preferences to actual values
    fontsize = 70 if size == 'big' else 40
    
    if position == 'center':
        position_tuple = ('center', 'center')
    else:
        # Position above bottom
        position_tuple = ('center', 'bottom')
        
    return {
        'fontsize': fontsize,
        'position': position_tuple,
        'bottom_margin': 40 if position == 'bottom' else 0  # Add margin if at bottom
    }

def create_video_from_json(json_file="transcription_markers.json", output_file="output_video.mp4"):
    try:
        # Get subtitle preferences first
        subtitle_prefs = get_subtitle_preferences()
        
        print(f"Reading JSON file: {json_file}")
        # Read the JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Get audio file path from metadata
        audio_path = data["metadata"]["audio_file"]
        print(f"Loading audio: {audio_path}")
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Default video size
        video_size = (1920, 1080)
        
        # Create a list of image clips with their timing
        image_clips = []
        
        # Track current image and its duration
        current_image = None
        current_start = 0
        
        print("Processing images and creating clips...")
        # Go through all segments chronologically
        segments = data["segments"]
        for second, segment in segments.items():
            second = int(second)
            
            # If this segment has an image
            if "image_path" in segment and os.path.exists(segment["image_path"]):
                print(f"Found image at {second}s: {segment['image_path']}")
                # If we have a current image, add it to our clips
                if current_image is not None:
                    img_clip = (ImageClip(current_image)
                              .set_start(current_start)
                              .set_duration(second - current_start)
                              .resize(height=video_size[1])
                              .set_position('center'))
                    image_clips.append(img_clip)
                
                # Update current image
                current_image = segment["image_path"]
                current_start = second
        
        # Add the last image if it exists
        if current_image is not None:
            img_clip = (ImageClip(current_image)
                       .set_start(current_start)
                       .set_duration(duration - current_start)
                       .resize(height=video_size[1])
                       .set_position('center'))
            image_clips.append(img_clip)
        
        # Create subtitles if wanted
        subtitle_clips = []
        if subtitle_prefs is not None:
            print("Creating subtitle clips...")
            for second, segment in segments.items():
                if segment["text"].strip():  # If there's text
                    start_time = int(second)
                    text = segment["text"]
                    
                    # Calculate position
                    position = list(subtitle_prefs['position'])
                    if position[1] == 'bottom':
                        # Create a position slightly above bottom
                        position = ('center', video_size[1] - subtitle_prefs['bottom_margin'])
                    
                    txt_clip = (TextClip(text, 
                                       fontsize=subtitle_prefs['fontsize'], 
                                       color='white', 
                                       stroke_color='black',
                                       stroke_width=2, 
                                       font='Arial', 
                                       size=video_size)
                               .set_start(start_time)
                               .set_duration(1)
                               .set_position(position))
                    subtitle_clips.append(txt_clip)
        
        # If no images were found, create a black background
        if not image_clips:
            print("No images found, creating black background...")
            bg_clip = ColorClip(video_size, color=(0,0,0)).set_duration(duration)
            image_clips.append(bg_clip)
        
        # Combine everything
        print("Compositing video...")
        final_video = CompositeVideoClip(image_clips + subtitle_clips)
        
        # Add the audio
        final_video = final_video.set_audio(audio)
        
        # Write the video file
        print(f"Writing video to {output_file}...")
        final_video.write_videofile(output_file, fps=24, codec='libx264', 
                                  audio_codec='aac', audio_bitrate='192k')
        
        # Clean up
        print("Cleaning up resources...")
        final_video.close()
        audio.close()
        for clip in image_clips + subtitle_clips:
            clip.close()
            
        print("Video creation completed!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py output_filename.mp4")
        sys.exit(1)
    
    output_file = sys.argv[1]
    
    # Verify output file has proper extension
    if not output_file.lower().endswith('.mp4'):
        output_file += '.mp4'
    
    print(f"Starting video creation process...")
    create_video_from_json(output_file=output_file)

if __name__ == "__main__":
    main()