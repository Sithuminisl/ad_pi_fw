
"""
Filename: dac_interface.py
Author: shanika sithumini
Date: 2025-06-28
Description: A module to handle audio playback through ALSA-compatible DACs.
Version: 1.0
"""

import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import os

class DacInterface:
    """
    A class to interface with an external DAC (e.g., HiFi DAC HAT) and play audio signals.
    """

    def __init__(self, device=None, sample_rate=192000):
        """
        Initialize the DAC interface.

        Args:
            device (str or int): ALSA device name or index (e.g., 'hw:1,0').
            sample_rate (int): Default playback sample rate.
        """
        self.device = device
        self.sample_rate = sample_rate

    def play(self, signal, sample_rate=None):
        """
        Play audio through the configured DAC.

        Args:
            signal (np.ndarray): Modulated audio signal, float32 [-1.0, 1.0].
            sample_rate (int, optional): Override sample rate.
        """
        if signal is None:
            raise ValueError("Signal is None. Cannot play empty audio.")

        # Normalize to [-1.0, 1.0]
        signal = signal / np.max(np.abs(signal))
        signal = signal.astype(np.float32)

        # Ensure mono format
        if signal.ndim == 1:
            signal = signal.reshape(-1, 1)

        fs = sample_rate if sample_rate is not None else self.sample_rate
        print(f"Playing signal via DAC at {fs} Hz on device '{self.device}'...")
        sd.play(signal, samplerate=fs, device=self.device)
        sd.wait()
        print("Playback complete.")

    def save_wav(self, filename, signal, sample_rate=None):
        """
        Save the audio signal to a WAV file for later playback or testing.

        Args:
            filename (str): Output file path.
            signal (np.ndarray): Audio signal to save.
            sample_rate (int, optional): Sampling rate.
        """
        if signal is None:
            raise ValueError("Signal is None. Cannot save empty audio.")
        if filename is None or not filename.lower().endswith(".wav"):
            raise ValueError("Invalid filename. Must be a '.wav' file.")

        # Normalize and convert to int16
        signal = signal / np.max(np.abs(signal))
        signal_int16 = np.int16(signal * 32767)
        fs = sample_rate if sample_rate is not None else self.sample_rate

        wavfile.write(filename, fs, signal_int16)
        print(f"Saved WAV file: {filename}")

    def test_playback_from_wav(self, file_path):
        """
        Load a WAV file and test playback through the DAC.

        Args:
            file_path (str): Path to the WAV file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"WAV file '{file_path}' not found.")

        fs, signal = wavfile.read(file_path)

        # If int16, convert to float32
        if signal.dtype == np.int16:
            signal = signal.astype(np.float32) / 32767.0

        self.play(signal, sample_rate=fs)
