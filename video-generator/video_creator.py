from moviepy.editor import *
import os

class VideoCreator:
    def __init__(self, data, subtitle_prefs):
        self.data = data
        self.subtitle_prefs = subtitle_prefs
        self.video_size = (1920, 1080)
    
    def create_video(self, output_path):
        """Create the video with all components"""
        try:
            print("Starting video creation...")
            
            # Get audio
            audio_path = self.data["metadata"]["audio_file"]
            print(f"Loading audio: {audio_path}")
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Create image clips
            print("Creating image clips...")
            image_clips = self._create_image_clips(duration)
            
            # Create subtitle clips if wanted
            subtitle_clips = []
            if self.subtitle_prefs and self.subtitle_prefs.get('show_subtitles'):
                print("Creating subtitle clips...")
                subtitle_clips = self._create_subtitle_clips()
                print(f"Created {len(subtitle_clips)} subtitle clips")
            
            # If no images, create black background
            if not image_clips:
                print("No images found, creating black background...")
                bg_clip = ColorClip(self.video_size, color=(0,0,0)).set_duration(duration)
                image_clips.append(bg_clip)
            
            # Combine everything
            print("Compositing final video...")
            # First create the base video with images
            base_video = CompositeVideoClip(image_clips)
            
            # If we have subtitles, add them as overlays
            if subtitle_clips:
                final_video = CompositeVideoClip([base_video] + subtitle_clips)
            else:
                final_video = base_video
            
            # Set the audio
            final_video = final_video.set_audio(audio)
            
            # Write video file
            print(f"Writing video to: {output_path}")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                audio_bitrate='192k'
            )
            
            # Cleanup
            print("Cleaning up resources...")
            self._cleanup_clips(final_video, audio, image_clips + subtitle_clips)
            print("Video creation completed!")
            
        except Exception as e:
            raise Exception(f"Error creating video: {str(e)}")
    
    def _create_image_clips(self, duration):
        """Create clips for images"""
        image_clips = []
        current_image = None
        current_start = 0
        
        for second, segment in sorted(self.data["segments"].items(), key=lambda x: int(x[0])):
            second = int(second)
            
            if "image_path" in segment and os.path.exists(segment["image_path"]):
                if current_image is not None:
                    img_clip = (ImageClip(current_image)
                              .set_start(current_start)
                              .set_duration(second - current_start)
                              .resize(height=self.video_size[1])
                              .set_position('center'))
                    image_clips.append(img_clip)
                
                current_image = segment["image_path"]
                current_start = second
        
        # Add final image if exists
        if current_image is not None:
            img_clip = (ImageClip(current_image)
                       .set_start(current_start)
                       .set_duration(duration - current_start)
                       .resize(height=self.video_size[1])
                       .set_position('center'))
            image_clips.append(img_clip)
        
        return image_clips
    
    def _create_subtitle_clips(self):
        """Create subtitle clips"""
        subtitle_clips = []
        
        # Sort segments by time
        sorted_segments = sorted(self.data["segments"].items(), key=lambda x: int(x[0]))
        
        for second, segment in sorted_segments:
            if segment["text"].strip():
                second = int(second)
                
                # Calculate position
                if self.subtitle_prefs['position'] == 'bottom':
                    y_pos = self.video_size[1] - self.subtitle_prefs['margin']
                    position = ('center', y_pos)
                else:
                    position = ('center', 'center')
                
                try:
                    txt_clip = (TextClip(
                        segment["text"],
                        fontsize=self.subtitle_prefs['fontsize'],
                        color='white',
                        stroke_color='black',
                        stroke_width=2,
                        font='Arial',
                        size=(self.video_size[0], None),  # Allow height to be automatic
                        method='caption'
                    )
                    .set_start(second)
                    .set_duration(1)
                    .set_position(position))
                    
                    subtitle_clips.append(txt_clip)
                    
                except Exception as e:
                    print(f"Warning: Could not create subtitle for text: {segment['text']}")
                    print(f"Error: {str(e)}")
                    continue
        
        return subtitle_clips
    
    def _cleanup_clips(self, final_video, audio, clips):
        """Clean up all clips"""
        try:
            final_video.close()
            audio.close()
            for clip in clips:
                clip.close()
        except Exception as e:
            print(f"Warning: Error during cleanup: {str(e)}")