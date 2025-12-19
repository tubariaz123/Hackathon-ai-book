---
title: "Speech-to-Text with Whisper"
sidebar_position: 2
---

# Speech-to-Text with Whisper

This section covers the implementation of Whisper-based speech recognition for robotic applications. We'll explore how to deploy Whisper models, handle real-time audio input, and optimize for robotic command recognition.

## Installing Whisper

First, install the OpenAI Whisper library:

```bash
pip install openai-whisper
```

For GPU acceleration (recommended for real-time applications):

```bash
# For CUDA 11.x
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.x
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Basic Whisper Implementation

Here's a basic implementation for robotic command recognition:

```python
import whisper
import torch
import pyaudio
import wave
import numpy as np
from queue import Queue
import threading

class WhisperRobotSTT:
    def __init__(self, model_size="small"):
        """
        Initialize Whisper-based speech-to-text for robotics
        """
        self.model_size = model_size
        self.model = whisper.load_model(model_size)
        self.audio_queue = Queue()

        # Audio configuration for robotics
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000  # Standard for speech recognition
        self.chunk = 1024
        self.audio = pyaudio.PyAudio()

        # Recording parameters
        self.recording = False
        self.audio_buffer = []

    def start_listening(self):
        """Start real-time audio listening"""
        self.recording = True

        # Open audio stream
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        # Start audio recording thread
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()

    def _record_audio(self):
        """Record audio in a separate thread"""
        while self.recording:
            data = self.stream.read(self.chunk)
            self.audio_queue.put(data)

    def stop_listening(self):
        """Stop audio recording"""
        self.recording = False
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'audio'):
            self.audio.terminate()

    def transcribe_audio(self, audio_data):
        """Transcribe audio data using Whisper"""
        # Convert audio data to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        audio_float = audio_array.astype(np.float32) / 32768.0  # Normalize

        # Transcribe using Whisper
        result = self.model.transcribe(audio_float)
        return result["text"].strip()

    def get_command(self, timeout=5.0):
        """Get a single command from audio input"""
        start_time = time.time()
        audio_frames = []

        # Collect audio for the specified timeout
        while time.time() - start_time < timeout:
            try:
                frame = self.audio_queue.get(timeout=0.1)
                audio_frames.append(frame)
            except:
                continue

        if audio_frames:
            # Combine audio frames
            audio_data = b''.join(audio_frames)
            return self.transcribe_audio(audio_data)

        return ""
```

## Optimizing for Robot Commands

Robot commands are typically short and specific. Here's how to optimize Whisper for robotic applications:

```python
class OptimizedRobotSTT(WhisperRobotSTT):
    def __init__(self, model_size="small"):
        super().__init__(model_size)

        # Define common robot command patterns
        self.robot_commands = {
            'move_forward': ['move forward', 'go forward', 'forward'],
            'move_backward': ['move backward', 'go backward', 'backward'],
            'turn_left': ['turn left', 'left', 'rotate left'],
            'turn_right': ['turn right', 'right', 'rotate right'],
            'stop': ['stop', 'halt', 'pause'],
            'pick_up': ['pick up', 'grasp', 'take'],
            'put_down': ['put down', 'release', 'drop'],
            'follow_me': ['follow me', 'follow', 'come with me'],
            'go_to': ['go to', 'move to', 'navigate to']
        }

    def transcribe_with_context(self, audio_data):
        """Transcribe with robot command context"""
        # Transcribe normally first
        text = self.transcribe_audio(audio_data)

        # Apply post-processing for robot commands
        processed_text = self._process_robot_command(text)
        return processed_text

    def _process_robot_command(self, text):
        """Process text to match robot command patterns"""
        text_lower = text.lower().strip()

        # Look for exact command matches first
        for command_type, phrases in self.robot_commands.items():
            for phrase in phrases:
                if phrase in text_lower:
                    return phrase

        return text
```

## Handling Different Whisper Models

Different Whisper models offer trade-offs between speed and accuracy:

```python
def select_model_for_robot(robot_type, environment):
    """
    Select appropriate Whisper model based on robot type and environment
    """
    if robot_type == "mobile_base":
        # Mobile robots may have limited compute
        if environment == "controlled":
            return "base"  # Good balance of speed/accuracy
        else:
            return "small"  # Better accuracy for noisy environments
    elif robot_type == "stationary":
        # Stationary robots can use more compute-intensive models
        return "medium"
    elif robot_type == "humanoid":
        # Humanoid robots need high accuracy for social interaction
        return "large"
```

## Performance Optimization

For real-time robotic applications, consider these optimizations:

```python
class OptimizedWhisperSTT:
    def __init__(self, model_size="small"):
        # Use GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_size).to(self.device)

        # Use faster inference settings for robotics
        self.options = whisper.DecodingOptions(
            language='en',  # Specify language for better performance
            without_timestamps=True,  # Not needed for command recognition
            fp16=True if self.device == "cuda" else False  # Use fp16 on GPU
        )

    def transcribe_optimized(self, audio_data):
        """Optimized transcription for real-time performance"""
        audio_array = self._preprocess_audio(audio_data)

        # Convert to tensor and move to device
        mel = whisper.log_mel_spectrogram(audio_array).to(self.device)

        # Decode using pre-configured options
        result = whisper.decode(self.model, mel, self.options)
        return result.text
```

## Integration with ROS 2

Integrate Whisper with ROS 2 for robotic applications:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import AudioData

class WhisperROS2Node(Node):
    def __init__(self):
        super().__init__('whisper_stt_node')

        # Create publisher for recognized commands
        self.command_publisher = self.create_publisher(String, 'robot_commands', 10)

        # Create subscriber for audio data
        self.audio_subscription = self.create_subscription(
            AudioData,
            'audio_input',
            self.audio_callback,
            10
        )

        # Initialize Whisper STT
        self.stt = OptimizedRobotSTT()

        self.get_logger().info('Whisper STT node initialized')

    def audio_callback(self, msg):
        """Process incoming audio data"""
        try:
            command = self.stt.transcribe_audio(msg.data)
            if command:
                # Publish recognized command
                cmd_msg = String()
                cmd_msg.data = command
                self.command_publisher.publish(cmd_msg)
                self.get_logger().info(f'Recognized command: {command}')
        except Exception as e:
            self.get_logger().error(f'Error in audio processing: {e}')
```

## Testing and Validation

Test your Whisper implementation with various robotic command scenarios:

```python
def test_robot_commands(stt_instance):
    """Test Whisper with common robot commands"""
    test_commands = [
        "move forward",
        "turn left",
        "stop immediately",
        "pick up the red block",
        "go to the kitchen"
    ]

    for command in test_commands:
        print(f"Testing: {command}")
        # Simulate audio input for testing
        result = stt_instance.transcribe_with_context(command.encode())
        print(f"Recognized: {result}")
        print("---")
```

This implementation provides a solid foundation for using Whisper in robotic applications, with optimizations for real-time performance and robot-specific command recognition.