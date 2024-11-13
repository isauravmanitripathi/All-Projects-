import os 
import uuid 

def generate_unique_filename(base_name, directory, extension='.mp4'):
	"""
	base name -> the original name of the file 
	directory -> The folder where the final file will be saved 
	extension -> to make sure it is a video file 
	
	Return 
	-> the full path of the unique file   
	"""
	unqiue_id = uuid.uuid4().hex
	filename = f"{base_name}_{unqiue_id}{extension}"
	return os.path.join(directory, filename)


def validate_image(image_path):
	if not os.path.isfile(image_path):
		raise FileExistsError(f"Image File '{image_path}' does not exist!")
	
	supported_formats = ('.png' ,'.jpg' , '.jpeg')
	if not image_path.lower().endswith(supported_formats):
		raise ValueError(f"Unsupported image format. Supported formats{supported_formats}")