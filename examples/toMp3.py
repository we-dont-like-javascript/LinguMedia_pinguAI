from pydub import AudioSegment
import io

# PCM data parameters
sample_rate = 44100  # Sample rate in Hz
channels = 1         # Mono audio
sample_width = 4     # 32-bit float = 4 bytes per sample

# Assume `pcm_data` is a variable that holds your raw PCM bytes
# If you read PCM data from a file, do it like this:
with open("sonic.pcm", "rb") as pcm_file:
    pcm_data = pcm_file.read()

# Use BytesIO to treat raw PCM data as a file-like object
pcm_io = io.BytesIO(pcm_data)

# Convert raw PCM to an AudioSegment
audio_segment = AudioSegment.from_raw(
    pcm_io,
    sample_width=sample_width,
    frame_rate=sample_rate,
    channels=channels
)

# Export the AudioSegment to an MP3 file
audio_segment.export("output.mp3", format="mp3")

print("MP3 file created successfully.")
