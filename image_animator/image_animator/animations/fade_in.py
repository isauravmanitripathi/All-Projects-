from manim import * # type: ignore
import os 


class FadeInAnimation(Scene):
	def __init__(self, image_path, **kwargs):
		self.image_path = image_path
		super().__init__(**kwargs)
		
	def construct(self):
		# construct the animation
		# Load the image 
		image = ImageMobject(self.image_path)
		image.scale(2)
		
		self.play(FadeIn(image))
		self.wait(1)