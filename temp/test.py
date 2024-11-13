from manim import *

class ImageMovingInSShape(Scene):
    def construct(self):
        # Load the image (ensure the image file is in the same directory or provide the full path)
        image = ImageMobject("your_image.png")
        image.scale(0.5)  # Scale down the image for better visibility
        image.move_to(LEFT * 4 + UP * 2)  # Set the starting position

        self.play(FadeIn(image))
        self.wait(1)

        # Define the path for the "S" shape using a series of points
        path_points = [
            LEFT * 4 + UP * 2,
            LEFT * 2 + UP,
            ORIGIN,
            RIGHT * 2 + DOWN,
            RIGHT * 4 + DOWN * 2
        ]

        # Create a path object to move the image along it
        path = VMobject()
        path.set_points_smoothly(path_points)
        self.play(MoveAlongPath(image, path), run_time=4)
        self.wait(1)

        # Fade out the image at the end
        self.play(FadeOut(image))
        self.wait(1)
