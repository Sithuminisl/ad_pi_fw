
"""
Filename: am_transmitter.py
Author: shanika sithumini
Date: 2025-06-28
Description: Complete AM audio transmission chain using AudioProcessor,
             AmModulator, and DacInterface, configured via config.yml
"""

import yaml
import argparse
from am_modulator import AmModulator
from audio_processor import AudioProcessor
from dac_interface import DacInterface

def load_config(config_path="config.yml"):
    """
    Load configuration from a YAML file.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def main(audio_file, config_path="config.yml"):
    # Load configuration
    config = load_config(config_path)

    # Audio configuration
    sample_rate = config["audio"]["sample_rate"]

    # Modulation config
    carrier_freq = config["modulation"]["carrier_freq"]
    modulation_index = config["modulation"].get("modulation_index", 1.0)

    # DAC config
    dac_device = "hw:1,0"  # Simplified for ALSA
    dac_sample_rate = sample_rate

    # Load and process audio
    audio = AudioProcessor(audio_file)
    audio.load_audio(audio_file)
    audio.monotone()
    audio.normalize_data()
    audio.oversample(sample_rate)  # Resample to 192 kHz for DAC

    # Modulate signal
    modulator = AmModulator(carrier_freq, audio.audio_data[:, 0], audio.sample_rate)
    modulated_signal = modulator.get_modulated_signal()

    # Play via DAC
    dac = DacInterface(device=dac_device, sample_rate=dac_sample_rate)
    dac.save_wav("modulated_output.wav", modulated_signal, sample_rate)
    dac.play(modulated_signal, sample_rate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AM Transmitter Audio System")
    parser.add_argument("audio_file", type=str, help="Path to input WAV or MP3 file")
    parser.add_argument("--config", type=str, default="config.yml", help="Path to YAML config file")
    args = parser.parse_args()
    main(args.audio_file, args.config)
