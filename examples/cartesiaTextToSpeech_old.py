import struct
from cartesia import Cartesia
import os
from dotenv import load_dotenv
import wave
import io

load_dotenv()

api_key = os.getenv('CARTESIA_API_KEY')
client = Cartesia(api_key=api_key)

voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"  # Barbershop Man
model_id = "sonic-english"
transcript = "Hello! Welcome to Cartesia"

output_format = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}

# Set up a WebSocket connection.
ws = client.tts.websocket()

# Variable for raw PCM audio bytes
pcm_bytes = io.BytesIO()

# Generate and stream audio.
for output in ws.send(
    model_id=model_id,
    transcript=transcript,
    voice_id=voice_id,
    stream=True,
    output_format=output_format,
):
    buffer = output["audio"]  # buffer contains raw PCM audio bytes
    pcm_bytes.write(buffer)

# Close the connection to release resources
ws.close()

print("== Done Generation ==")

sample_rate = 44100  # Hz
channels = 1  # Mono
sample_width = 4  # 4 bytes for float32
wav_file = "output.wav"

# read out raw pcm bytes
pcm_bytes.seek(0)
pcm_data = pcm_bytes.read()

# Create a WAV file and set its parameters
with wave.open(wav_file, "wb") as wav_f:
    wav_f.setnchannels(channels)  # Mono
    wav_f.setsampwidth(4)  # 32-bit float = 4 bytes per sample
    wav_f.setframerate(sample_rate)  # 44.1 kHz sample rate

    # Convert the raw PCM float32 data into binary frames
    for i in range(0, len(pcm_data), 4):
        # Read 4 bytes (32 bits, little-endian float) and unpack to float
        float_value = struct.unpack('<f', pcm_data[i:i+4])[0]
        # Pack the float as little-endian 32-bit and write to the WAV file
        wav_f.writeframes(struct.pack('<f', float_value))

print(f"WAV file '{wav_file}' created successfully.")

print("WAV file created")
