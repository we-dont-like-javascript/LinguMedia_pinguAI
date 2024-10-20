import reflex as rx

from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)

def stats(
    word_type: str = "Noun",
    word: str = "Pizza",
    description: str = "Description here",
    start_timestamp: str = "00.00",
    end_timestamp: str = "03:24",
    icon: str = "lightbulb",
    badge_color: LiteralAccentColor = "yellow",
) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(tag=icon, size=34),
                    color_scheme=badge_color,
                    radius="full",
                    padding="0.7rem",
                ),
                rx.vstack(
                    rx.heading(
                        f"{word}",
                        size="6",
                        weight="bold",
                    ),
                    rx.hstack(
                        rx.text(
                        word_type, size="1", weight="medium"
                        ),
                        rx.text(
                            f"| {start_timestamp} - {end_timestamp}", size="1", weight="medium" 
                        ),
                        spacing="1"
                    ),
                    
                    spacing="1",
                    height="100%",
                    align_items="start",
                    width="100%",
                ),
                height="100%",
                spacing="4",
                align="center",
                width="100%",
            ),
            rx.hstack(
                rx.text(
                    f"{description}",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                align="center",
                width="100%",
            ),
            spacing="3",
        ),
        size="4",
        width="95%",
        max_width="21rem",
        margin="auto",
        padding="20px",
    )
    
# Function to generate multiple stats from a list of data
def generate_stats(data_list: list[dict]) -> rx.Component:
    """Generate multiple stats using rx.foreach to handle dynamic generation."""
    
    return rx.vstack(
        rx.foreach(  # Use rx.foreach to dynamically create components
            data_list, 
            lambda item: stats(  # For each item, generate a single stat card
                word_type=item["word_type"],
                word=item["word"],
                description=item["description"],
                start_timestamp="0:00",
                end_timestamp="03:24",
                icon="lightbulb",
                badge_color="yellow"
            )
        ),
        spacing="20px",  # Adjust spacing between each stat card
        width="100%",  # Full width of container
        align_items="center",  # Center all the stats
    )