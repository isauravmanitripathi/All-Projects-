import whisper
import sys
import json
from collections import defaultdict
import datetime

def transcribe_with_automatic_markers(audio_path):
    try:
        # Load the model
        print("Loading Whisper model...")
        model = whisper.load_model("base")
        
        # Transcribe the audio
        print("Transcribing audio...")
        result = model.transcribe(audio_path, verbose=False)
        
        # Create dictionaries to store words and markers
        words_by_second = defaultdict(list)
        current_marker = 1
        
        # Process each segment
        for segment in result["segments"]:
            start_sec = int(round(segment["start"]))
            end_sec = int(round(segment["end"]))
            text = segment["text"].strip()
            
            # If the segment spans multiple seconds, try to distribute words across seconds
            if start_sec != end_sec:
                words = text.split()
                total_duration = end_sec - start_sec
                words_per_second = len(words) / total_duration
                
                for i, word in enumerate(words):
                    word_second = start_sec + int(i / words_per_second)
                    if word_second <= end_sec:
                        words_by_second[word_second].append(word)
            else:
                words_by_second[start_sec].append(text)
        
        # Create JSON structure with metadata and automatic markers
        json_data = {
            "metadata": {
                "audio_file": audio_path,
                "total_duration": max(words_by_second.keys()) + 1,
                "processed_date": str(datetime.datetime.now())
            },
            "segments": {}
        }
        
        print("\nTranscription with markers:")
        print("------------------------")
        
        # Process chronologically and add markers
        max_second = max(words_by_second.keys())
        for second in range(max_second + 1):
            timestamp = f"{second // 60:02d}:{second % 60:02d}"
            
            if second in words_by_second:
                text = " ".join(words_by_second[second])
                
                json_data["segments"][str(second)] = {
                    "timestamp": timestamp,
                    "text": text,
                    "marker": current_marker
                }
                print(f"{timestamp} | {text} -> {current_marker}")
                current_marker += 1
            else:
                json_data["segments"][str(second)] = {
                    "timestamp": timestamp,
                    "text": "",
                    "marker": None
                }
        
        # Save to JSON file
        output_file = "transcription_markers.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
            
        print(f"\nMarkers saved to {output_file}")

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
    transcribe_with_automatic_markers(audio_path)

if __name__ == "__main__":
    main()