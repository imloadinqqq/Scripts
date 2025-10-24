
import simpleaudio as sa
from pathlib import Path

done = Path(__file__).resolve().parent / "done.wav"
print("Playing:", done)

try:
    wave = sa.WaveObject.from_wave_file(str(done))
    play = wave.play()
    play.wait_done()
    print("✅ Sound played successfully.")
except Exception as e:
    print("⚠️ Error:", e)
