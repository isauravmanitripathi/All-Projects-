import json
import os
from typing import Dict, List

def read_markers(json_file: str = "transcription_markers.json"):
    try:
        # Read the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract segments from new JSON structure
        segments = data["segments"]
        
        # Show metadata
        print("\nAudio file:", data["metadata"]["audio_file"])
        print(f"Duration: {data['metadata']['total_duration']} seconds")
        print("Processed on:", data["metadata"]["processed_date"])
        
        # Get all unique markers (excluding None)
        markers = set()
        for entry in segments.values():
            if entry["marker"] is not None:
                markers.add(entry["marker"])
        
        total_markers = len(markers)
        print(f"\nTotal number of markers: {total_markers}")
        print(f"Marker range: 1 to {max(markers)}\n")
        
        while True:
            # Get user input
            user_input = input("\nEnter a marker number to view (or 'q' to quit): ").strip()
            
            if user_input.lower() == 'q':
                break
            
            try:
                marker_num = int(user_input)
                
                # Find all entries with this marker
                found_entries = []
                for second, entry in segments.items():
                    if entry["marker"] == marker_num:
                        found_entries.append(entry)
                
                if found_entries:
                    print(f"\nFound entries for marker {marker_num}:")
                    print("-" * 50)
                    for entry in found_entries:
                        print(f"Time: {entry['timestamp']} | {entry['text']}")
                        if "image_path" in entry:
                            print(f"Associated image: {entry['image_path']}")
                    print("-" * 50)
                    
                    # Ask if user wants to add an image
                    add_image = input("\nWould you like to add an image to this marker? (y/n): ").strip().lower()
                    
                    if add_image == 'y':
                        image_path = input("Enter the path to the image: ").strip()
                        
                        # Verify the image path exists
                        if os.path.exists(image_path):
                            # Add image path to all segments with this marker
                            modified = False
                            for second, entry in segments.items():
                                if entry["marker"] == marker_num:
                                    entry["image_path"] = image_path
                                    modified = True
                            
                            if modified:
                                # Save the updated JSON
                                data["segments"] = segments
                                with open(json_file, 'w', encoding='utf-8') as f:
                                    json.dump(data, f, indent=2, ensure_ascii=False)
                                print(f"\nImage path added to marker {marker_num}")
                        else:
                            print("Error: Image file not found")
                else:
                    print(f"No entries found for marker {marker_num}")
                    
            except ValueError:
                print("Please enter a valid number")
                
    except FileNotFoundError:
        print(f"Error: Could not find {json_file}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    read_markers()