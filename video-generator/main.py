import os
from json_processor import JsonProcessor
from subtitle_handler import SubtitleHandler
from video_creator import VideoCreator

def setup_result_directory():
    """Create Result directory if it doesn't exist"""
    if not os.path.exists("Result"):
        os.makedirs("Result")
        print("Created Result directory")

def main():
    setup_result_directory()
    
    # Get JSON file path
    while True:
        json_path = input("Enter the path to your JSON file: ").strip()
        if os.path.exists(json_path):
            break
        print("File not found. Please enter a valid path.")
    
    # Get output filename
    output_name = input("Enter the output video name (without .mp4): ").strip()
    output_path = os.path.join("Result", f"{output_name}.mp4")
    
    # Initialize components
    json_processor = JsonProcessor(json_path)
    subtitle_handler = SubtitleHandler()
    
    # Process JSON and get data
    data = json_processor.process()
    
    # Get subtitle preferences
    subtitle_prefs = subtitle_handler.get_preferences()
    
    # Create video
    video_creator = VideoCreator(data, subtitle_prefs)
    video_creator.create_video(output_path)

if __name__ == "__main__":
    main()