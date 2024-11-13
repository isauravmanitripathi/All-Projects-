import whisper
import sys
from collections import defaultdict

def round_to_second(timestamp):
    """Round a timestamp to the nearest second"""
    return int(round(timestamp))

def transcribe_by_second(audio_path):
    try:
        # Load the model
        print("Loading Whisper model...")
        model = whisper.load_model("base")
        
        # Transcribe the audio
        print("Transcribing audio...")
        result = model.transcribe(audio_path, verbose=False)
        
        # Create a dictionary to store words by second
        words_by_second = defaultdict(list)
        
        # Process each segment
        for segment in result["segments"]:
            # Get start and end times for the segment
            start_sec = round_to_second(segment["start"])
            end_sec = round_to_second(segment["end"])
            text = segment["text"].strip()
            
            # If the segment spans multiple seconds, try to distribute words across seconds
            if start_sec != end_sec:
                words = text.split()
                total_duration = end_sec - start_sec
                words_per_second = len(words) / total_duration
                
                for i, word in enumerate(words):
                    # Estimate which second this word belongs to
                    word_second = start_sec + int(i / words_per_second)
                    if word_second <= end_sec:
                        words_by_second[word_second].append(word)
            else:
                # If segment is within one second, add all text to that second
                words_by_second[start_sec].append(text)
        
        # Print results chronologically
        max_second = max(words_by_second.keys())
        
        print("\nTranscription by second:")
        print("------------------------")
        
        for second in range(max_second + 1):
            if second in words_by_second:
                minute = second // 60
                sec = second % 60
                timestamp = f"{minute:02d}:{sec:02d}"
                words = " ".join(words_by_second[second])
                print(f"{timestamp} | {words}")
            else:
                minute = second // 60
                sec = second % 60
                timestamp = f"{minute:02d}:{sec:02d}"
                print(f"{timestamp} | ...")

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
    transcribe_by_second(audio_path)

if __name__ == "__main__":
    main()