import whisper
import datetime
import sys

def format_timestamp(seconds):
    """Convert seconds to VTT timestamp format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{msecs:03d}"

def transcribe_to_vtt(audio_path):
    try:
        # Load the model (will download if not present)
        print("Loading Whisper model...")
        model = whisper.load_model("base")
        
        # Transcribe the audio
        print("Transcribing audio...")
        result = model.transcribe(audio_path, verbose=False)
        
        # Print VTT header
        print("WEBVTT\n")
        
        # Process each segment
        for i, segment in enumerate(result["segments"], 1):
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            
            # Print VTT cue
            print(f"{i}")
            print(f"{start_time} --> {end_time}")
            print(f"{segment['text'].strip()}\n")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    # Get audio path from user
    audio_path = input("Please enter the path to your audio file: ").strip()
    
    if not audio_path:
        print("Error: No audio path provided", file=sys.stderr)
        sys.exit(1)
    
    # Process the audio file
    transcribe_to_vtt(audio_path)

if __name__ == "__main__":
    main()