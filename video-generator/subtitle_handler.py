class SubtitleHandler:
    def __init__(self):
        self.FONT_SIZES = {
            'small': 40,
            'big': 70
        }
    
    def get_preferences(self):
        """Get subtitle preferences from user"""
        # Ask if subtitles are wanted
        while True:
            want_subtitles = input("Do you want subtitles in the video? (y/n): ").lower().strip()
            if want_subtitles in ['y', 'n']:
                break
            print("Please enter 'y' or 'n'")
        
        if want_subtitles == 'n':
            return {
                'show_subtitles': False
            }
        
        # Get position preference
        while True:
            position = input("Where do you want the subtitles? (center/bottom): ").lower().strip()
            if position in ['center', 'bottom']:
                break
            print("Please enter 'center' or 'bottom'")
        
        # Get size preference
        while True:
            size = input("What size do you want the subtitles? (small/big): ").lower().strip()
            if size in ['small', 'big']:
                break
            print("Please enter 'small' or 'big'")
        
        return {
            'show_subtitles': True,
            'fontsize': self.FONT_SIZES[size],
            'position': position,
            'margin': 100 if position == 'bottom' else 0  # 100 pixels from bottom
        }