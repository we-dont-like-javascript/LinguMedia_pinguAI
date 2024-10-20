import reflex as rx
from rxconfig import config
from LinguMedia_pinguAI.chatbox import stats, generate_stats
from LinguMedia_pinguAI.state import State

def create_select_option(option_value, option_text):
    """Create a select option element with the given value and text."""
    return rx.el.option(option_text, value=option_value)

def create_styling_select():
    """Create a styled select element with predefined options and custom styling."""
    return rx.el.select(
        rx.el.option(
            "Select Language",
            value=True,
            disabled=True,
            selected=True,
        ),
        create_select_option(
            option_value="english", option_text="English"
        ),
        create_select_option(
            option_value="mandarin", option_text="中文"
        ),
        display="block",
        border_width="1px",
        border_color="#985555",
        _focus={
            "border-color": "#3B82F6",
            "outline-style": "none",
            "box-shadow": "var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color)",
            "--ring-color": "#3B82F6",
        },
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="1rem",
        box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        width="25%",
    )

# Function to render the video based on the current state of the URL
def video_display():
    return rx.box(
        # Conditionally display video or text prompt
        rx.cond(
            State.video_url == "",  # If the video URL is empty
            rx.text(
                "Insert any link", 
                style={
                    "color": "#808080", 
                    "fontSize": "20px",
                    "margin":"auto",
                    "textAlign": "center",  # Center the text horizontally
                    "paddingTop": "20px"  # Add space above the text
                }
            ),  # Text prompt when URL is empty
            rx.video(  # Video component if URL is available
                url=State.video_url,
                width="100%",  # Full width within the container
                height="100%",
                margin="auto",
                controls=True,  # Enable video controls (play, pause, etc.)
                style={"borderRadius": "16px"}  # Rounded corners for the video
            ),
        ),
        padding="20px",  # Adjusted padding
        style={
            "width": "100%",  # Ensure it takes full width
            "height": "100%",
            "maxWidth": "800px",  # Set a max width to control the video size
            "margin": "auto",  # Center the video container
        },
    )


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
       rx.color_mode.button(position="top-right"),
        rx.hstack(
            rx.hstack (
                rx.text("Lingu", style={"fontStyle": "italic"}, size="8"),
                rx.text("Media", style={"fontStyle": "bold"}, size="8"),
            ),
        rx.hstack (
            rx.text("My Profile", style={"marginTop": "5px"}),
            rx.button(
                "Sign Up",
                style={
                    "backgroundColor": "#A94B3F",
                    "borderRadius": "8px"
                },
            ),
        ),
        justify="between",
        width = "100%",
        ), # This controls the Heading
        rx.hstack(
            rx.text(
                "Add a video URL to import",
                style={
                    "color": "#808080",
                    "marginTop": "10px"
                    },
                size="2",
            ),
            rx.input(
                placeholder="Type something...",
                size="2",
                style={
                    "borderRadius": "15px",
                    "width": "25%",
                    "height": "43px",
                    "boxShadow": "inset 0 2px 4px rgba(0, 0, 0, 0.2)",
                    "border": "1px solid #ccc"
                },
                on_change=lambda value: State.set_video_url(value),
            ),
            rx.button(
                "Link",
                style={
                    "backgroundColor": "#A94B3F",
                    "borderRadius": "20px",
                    "marginRight": "30px",
                    "width": "10%",
                    "height": "42px"
                    },
                # Handle Link to upload video here
                on_click=lambda: State.set_video_url(State.video_url),
            ),
            create_styling_select(),
            style={
                "paddingTop": "30px",
                "paddingLeft": "20px"
                # This moves the entire stack down
            },
        ), # This controls the Text Input (URL) + Link Button
        rx.hstack(
            rx.box(
                video_display(),
                # Video Box
                style={
                    "border": "2px solid #985555",
                    "borderRadius": "24px",
                    "width": "80%",  # Adjusted to allow space for centering
                    "height": "750px",
                    "backgroundColor": "#FAFAF5",
                    "margin": "auto",  # Ensures auto margin for centering horizontally
                },
                # Centering the box
                display="flex",
                justifyContent="center",  # Centers horizontally
                alignItems="center",  # Centers vertically if the parent container has height
            ),

            rx.box(
                # Chat Box
                generate_stats(State.stats_data), # make it so that it can generate as much data
                padding="15px",
                style={
                "border": "2px solid #985555",
                "borderRadius": "24px",
                "width": "496px",
                "height": "750px",
                "marginTop": "20px",
                "backgroundColor": "#FAFAF5"
                },
            ),
        ),
        rx.logo(),
        style={
            "width": "100%",
        },
        size="4",
    )


app = rx.App()
app.add_page(index)
