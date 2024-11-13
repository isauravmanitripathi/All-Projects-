import json

class JsonProcessor:
    def __init__(self, json_path):
        self.json_path = json_path
    
    def process(self):
        """Read and process the JSON file"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate JSON structure
            self._validate_json(data)
            
            return data
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file")
        except Exception as e:
            raise Exception(f"Error processing JSON: {str(e)}")
    
    def _validate_json(self, data):
        """Validate the JSON structure"""
        required_keys = ["metadata", "segments"]
        if not all(key in data for key in required_keys):
            raise ValueError("Invalid JSON structure: missing required keys")
        
        if "audio_file" not in data["metadata"]:
            raise ValueError("Invalid JSON structure: missing audio file path")