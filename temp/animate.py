from manim import *

class moveimage(Scene):
	def construct(self):
		# loading the image 
		image = ImageMobject("assets/test.jpg")
		image.scale(0.5)
		image.move_to(ORIGIN)
		
		self.play(FadeIn(image))
		self.wait(1)
		

		self.play(image.animate.shift(LEFT * 4), run_time=3) 
		self.wait(1)
		
		# self.wait(3)
		
		self.play(FadeOut(image))
		self.wait(1)