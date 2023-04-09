import whisper
import pyaudio
import wave
import subprocess
from answer_window import answer_window, auto_close_window
import time
import logging
import os

script_path = (os.path.dirname(os.path.realpath(__file__)))


logging.basicConfig(level=logging.DEBUG, filename='voice_gpt_log.log',
                    format='%(asctime)s %(name)s \
                        %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "audio.wav"
params = []
AI_IMAGE = script_path + '/data/ai-black.png'

 # Set up PyAudio
audio_f = pyaudio.PyAudio()
stream = audio_f.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                      frames_per_buffer=CHUNK)


def listen_write(RECORD_SECONDS):
    """
    Write you voice query in file
    """
    say("im_listen.txt")
    logger.debug('Say "I litening before start recording')

    time.sleep(1)
    stream = audio_f.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio_f.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    logger.debug('Audio file is writed')


def decode(MODEL):
    """Speech To Text via openai whisper"""
    notify_send("Whisper working")
    logger.debug("Start decode voice via whisper")
    model = whisper.load_model(MODEL)
    audio = whisper.load_audio("audio.wav")
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(fp16=False, language='ru')
    result = whisper.decode(model, mel, options)
    logger.debug("End decode file in whisper")
    auto_close_window(result.text)
    return result.text


def notify_send(text):
    cmd = ['notify-send', f'"{text}"', '-i', AI_IMAGE, '-t', '800']
    subprocess.call(cmd, shell=False)
    return True


def write_file_result(result):
    with open("result.txt", 'w') as f:
        logging.debug("Text anser from GPT writed in file")
        f.write(result)


def say(file):
    cmd = ['festival', '--tts', '--language', 'russian', file]
    subprocess.Popen(cmd, shell=False)
    logger.debug(f"Festival say from {file}")


time.sleep(1)
listen_write(5)
question = decode(MODEL="medium")
print(question)
notify_send("ChatGPT Processing")
logger.debug("Start query to chatGPT")
cmd = f'echo "{question}" | chatgpt'
result = subprocess.check_output(cmd, shell=True)
answer = result.decode('utf8')
logger.debug("GPT is got answer")
write_file_result(answer)
answer_window(answer)
logger.debug('End the program iteration')
