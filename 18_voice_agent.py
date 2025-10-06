"""
Demo 20: Voice-Enabled Agent
Goal: Build a voice conversation interface with speech-to-text and text-to-speech

Key Teaching Points:
- Speech-to-text integration
- Text-to-speech synthesis
- Voice conversation flow
- Audio processing
"""

import os
from pathlib import Path
from strands import Agent, tool
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()


@tool
def current_time() -> str:
    """Get the current time in a voice-friendly format."""
    now = datetime.now()
    # Format time in 12-hour format with AM/PM for natural speech
    time_str = now.strftime("%I:%M %p")
    # Remove leading zero from hour
    time_str = time_str.lstrip("0")
    return f"The current time is {time_str}."


@tool
def get_weather_info(city: str) -> str:
    """Get weather information for voice response."""
    # Simplified for voice - more concise responses
    return f"The weather in {city} is currently sunny and 72 degrees Fahrenheit."


@tool
def set_reminder(task: str, time: str) -> str:
    """Set a voice reminder."""
    return f"Okay, I've set a reminder for {task} at {time}."


@tool
def answer_question(question: str) -> str:
    """Answer general knowledge questions for voice interaction."""
    responses = {
        "date": f"Today is {datetime.now().strftime('%B %d, %Y')}.",
        "hello": "Hello! How can I help you today?",
        "thanks": "You're welcome! Is there anything else I can help with?"
    }

    for key, response in responses.items():
        if key in question.lower():
            return response

    return "I'm not sure about that. Could you rephrase your question?"


# Voice-optimized agent
voice_agent = Agent(
    tools=[current_time, get_weather_info, set_reminder, answer_question],
    system_prompt="""You are a voice assistant. Your responses will be spoken aloud.

Voice response guidelines:
1. Keep responses SHORT and CONVERSATIONAL (1-3 sentences max)
2. Avoid special characters, markdown, or formatting
3. Use natural spoken language
4. Spell out numbers and abbreviations
5. Don't say "here's a list" - just state items naturally
6. Be friendly and personable

Example good responses:
- "The weather in Seattle is sunny and seventy two degrees"
- "I've set your reminder for the meeting at 3 PM"
- "Sure, I can help with that"

Example bad responses (too wordy):
- "Here is the weather information: Temperature: 72°F, Conditions: Sunny..."
"""
)


def text_to_speech_demo(text: str) -> str:
    """
    Simulate text-to-speech. In production, use services like:
    - AWS Polly
    - Google Cloud Text-to-Speech
    - Azure Speech Services
    - elevenlabs
    """
    print(f"\n🔊 [SPEAKING]: {text}\n")
    return text


def speech_to_text_demo(audio_description: str) -> str:
    """
    Simulate speech-to-text. In production, use services like:
    - AWS Transcribe
    - Google Cloud Speech-to-Text
    - Azure Speech Services
    """
    print(f"\n🎤 [LISTENING]: {audio_description}\n")
    return audio_description


def voice_conversation(user_speech: str):
    """Simulate a voice conversation."""
    # Step 1: Speech to text (simulated)
    user_text = speech_to_text_demo(user_speech)

    # Step 2: Get agent response
    agent_response = voice_agent(user_text)

    # Step 3: Text to speech (simulated)
    text_to_speech_demo(agent_response)

    return agent_response


def main():
    """Run the voice agent demo."""
    print("=" * 70)
    print("🎤 Voice-Enabled Agent Demo")
    print("=" * 70)
    print()

    print("This demo simulates a voice conversation interface.")
    print("In production, integrate with real speech services.\n")

    # Simulate voice conversations
    conversations = [
        "Hello, what's the weather like in Seattle?",
        "Set a reminder for team meeting at 3 PM",
        "What time is it?",
        "Thank you for your help",
    ]

    for i, speech in enumerate(conversations, 1):
        print(f"{'='*70}")
        print(f"Conversation Turn {i}")
        print(f"{'='*70}")

        response = voice_conversation(speech)

        print(f"✅ Response delivered via speech\n")

    print("=" * 70)
    print("✨ Demo complete!")
    print("\n📚 To implement real voice capabilities:")
    print("\n1. Speech-to-Text (Choose one):")
    print("   - AWS Transcribe")
    print("   - Google Cloud Speech-to-Text")
    print("   - Azure Speech Services")
    print("\n2. Text-to-Speech (Choose one):")
    print("   - AWS Polly")
    print("   - Google Cloud TTS")
    print("   - Azure Speech Services")
    print("   - ElevenLabs (very natural)")
    print("   - Coqui TTS (open source)")
    print("\n3. Audio Processing:")
    print("   - PyAudio for microphone input")
    print("   - sounddevice for playback")
    print("   - pydub for audio manipulation")
    print("=" * 70)


if __name__ == "__main__":
    main()


"""
Setup Instructions:

1. Install required packages:
   uv add python-dotenv

2. For production voice features, add:
   uv add boto3   # For AWS Polly/Transcribe
   uv add pyaudio sounddevice pydub  # For audio I/O

3. Run the demo:
   python demo_20_voice_agent.py

Features Demonstrated:
- Voice conversation flow
- Speech-to-text processing (simulated)
- Text-to-speech synthesis (simulated)
- Voice-optimized responses
- Natural language interaction

Real Implementation Example with AWS Transcribe + Polly:

```python
import boto3
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave
import time

# Initialize AWS clients
transcribe = boto3.client('transcribe', region_name='us-east-1')
polly = boto3.client('polly', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

# Speech to Text with AWS Transcribe
def speech_to_text(audio_file, bucket_name='my-audio-bucket'):
    # Upload audio to S3
    s3.upload_file(audio_file, bucket_name, audio_file)

    # Start transcription job
    job_name = f"transcription-{int(time.time())}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://{bucket_name}/{audio_file}'},
        MediaFormat='wav',
        LanguageCode='en-US'
    )

    # Wait for completion
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(2)

    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    return transcript_uri

# Text to Speech with AWS Polly
def text_to_speech(text):
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna',
        Engine='neural'
    )

    with open("output.mp3", "wb") as f:
        f.write(response['AudioStream'].read())

    # Play audio
    audio = AudioSegment.from_mp3("output.mp3")
    play(audio)

# Record audio from microphone
def record_audio(filename="input.wav", duration=5):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000

    p = pyaudio.PyAudio()

    stream = p.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk
    )

    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename
```

AWS Polly Example:

```python
import boto3
from pydub import AudioSegment
from pydub.playback import play

def aws_text_to_speech(text):
    polly = boto3.client('polly')

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna',  # or Matthew, Salli, etc.
        Engine='neural'  # More natural sounding
    )

    with open('output.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())

    audio = AudioSegment.from_mp3('output.mp3')
    play(audio)
```

Use Cases:
- Accessibility tools for visually impaired
- Hands-free assistants
- Voice-controlled automation
- Language learning apps
- Elderly care assistants
- Drive-time information systems
- Smart home integration

Production Considerations:
- Handle background noise
- Implement voice activity detection (VAD)
- Support multiple languages
- Add wake word detection
- Implement interrupt handling
- Optimize for low latency
- Add speaker identification
- Support offline mode
- Implement privacy controls
- Add audio quality checks

Voice UI Best Practices:
1. Keep responses concise (2-3 sentences max)
2. Use conversational language
3. Provide audio feedback (beeps, tones)
4. Handle misrecognition gracefully
5. Offer visual fallbacks when possible
6. Support both voice and text input
7. Implement timeout handling
8. Add confirmation for critical actions
9. Use SSML for better speech control
10. Test with diverse accents and speech patterns
"""
