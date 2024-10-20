import reflex as rx

class State(rx.State):
    """The app state, managing backend operations and interactions."""
    
    video_url: str = ""  # Default URL

    # Function to update the video URL
    def set_video_url(self, new_url):
        self.video_url = new_url
    
    @rx.var
    def stats_data(self) -> list[dict]:
        """Retrieve data for the stats from the database or an external API."""
        # Example static data (in practice, pull from a DB or API)
        return [
            {
                "word_type": "Noun",
                "word": "Pizza",
                "description": "A delicious flatbread topped with tomato sauce and cheese.",
                "icon": "utensils",
                "badge_color": "red",
            },
            {
                "word_type": "Verb",
                "word": "Run",
                "description": "Move at a speed faster than a walk.",
                "icon": "running",
                "badge_color": "green",
            },
            {
                "word_type": "Adjective",
                "word": "Bright",
                "description": "Giving off or reflecting light.",
                "icon": "sun",
                "badge_color": "yellow",
            },
        ]

    def fetch_data_from_db(self):
        """Fetch data from a database and update the state."""
        # Implement database logic here
        pass