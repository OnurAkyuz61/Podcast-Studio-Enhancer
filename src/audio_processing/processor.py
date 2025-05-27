import os
import time
import numpy as np
import soundfile as sf
import librosa
import noisereduce as nr
from pydub import AudioSegment
from scipy import signal

class AudioProcessor:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'output')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def process_audio(self, input_file, settings, progress_callback=None):
        """
        Process audio file to enhance it to studio podcast quality
        
        Args:
            input_file (str): Path to input audio file
            settings (dict): Dictionary containing processing settings
            progress_callback (callable): Function to call with progress updates (0-100)
            
        Returns:
            str: Path to the processed output file
        """
        # Update progress
        if progress_callback:
            progress_callback(5)
            
        # Load audio file
        y, sr = librosa.load(input_file, sr=None)
        
        # Update progress
        if progress_callback:
            progress_callback(15)
        
        # Apply noise reduction
        if settings.get('noise_reduction', 0) > 0:
            noise_reduction_amount = settings.get('noise_reduction', 0.5)
            y = self._apply_noise_reduction(y, sr, noise_reduction_amount)
            
        # Update progress
        if progress_callback:
            progress_callback(30)
            
        # Apply EQ based on preset
        eq_preset = settings.get('eq_preset', 'Stüdyo')  # Default to Studio preset
        y = self._apply_eq(y, sr, eq_preset)
        
        # Update progress
        if progress_callback:
            progress_callback(50)
            
        # Apply compression
        if settings.get('compression', 0) > 0:
            compression_amount = settings.get('compression', 0.5)
            y = self._apply_compression(y, compression_amount)
            
        # Update progress
        if progress_callback:
            progress_callback(70)
            
        # Normalize audio
        y = self._normalize_audio(y)
        
        # Update progress
        if progress_callback:
            progress_callback(85)
            
        # Create output filename
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_file = os.path.join(self.output_dir, f"{base_name}_enhanced_{timestamp}.wav")
        
        # Save processed audio
        sf.write(output_file, y, sr)
        
        # Try to convert to MP3 for smaller file size if FFmpeg is available
        mp3_output = output_file.replace('.wav', '.mp3')
        conversion_success = self._convert_to_mp3(output_file, mp3_output)
        
        # If conversion was successful, use the MP3 file and remove the WAV
        if conversion_success and os.path.exists(mp3_output):
            os.remove(output_file)
            output_file = mp3_output
        
        # Update progress
        if progress_callback:
            progress_callback(100)
            
        return output_file
    
    def _apply_noise_reduction(self, y, sr, amount):
        """Apply noise reduction to the audio"""
        # Calculate noise profile from the first second
        noise_sample = y[:min(len(y), sr)]
        
        # Apply noise reduction with sensitivity based on amount
        reduced_noise = nr.reduce_noise(
            y=y, 
            sr=sr,
            prop_decrease=amount,
            stationary=True
        )
        
        # For studio quality, apply a second pass with more gentle settings on higher amounts
        if amount > 0.6:
            reduced_noise = nr.reduce_noise(
                y=reduced_noise,
                sr=sr,
                prop_decrease=amount * 0.5,  # Gentler second pass
                stationary=True
            )
        
        return reduced_noise
    
    def _apply_eq(self, y, sr, preset):
        """Apply EQ based on preset"""
        if preset == 'Doğal':
            # Slight boost to mid frequencies for clarity
            return self._apply_eq_filter(y, sr, [
                (80, 0.8),    # Reduce low rumble
                (150, 1.1),   # Slight boost to low mids
                (3000, 1.2),  # Boost speech clarity
                (10000, 0.9)  # Slight reduction in high frequencies
            ])
        elif preset == 'Sıcak':
            # Boost low-mids for warmth
            return self._apply_eq_filter(y, sr, [
                (100, 1.2),   # Boost low end
                (250, 1.3),   # Boost low mids
                (2500, 0.9),  # Reduce high mids
                (8000, 0.8)   # Reduce highs
            ])
        elif preset == 'Parlak':
            # Boost high frequencies for brightness
            return self._apply_eq_filter(y, sr, [
                (100, 0.9),   # Reduce low end
                (1000, 1.1),  # Boost mids
                (3000, 1.3),  # Boost high mids
                (8000, 1.4)   # Boost highs
            ])
        elif preset == 'Derin':
            # Boost low frequencies for depth
            return self._apply_eq_filter(y, sr, [
                (80, 1.4),    # Boost sub bass
                (150, 1.3),   # Boost low end
                (400, 1.1),   # Boost low mids
                (3000, 0.9),  # Reduce high mids
                (8000, 0.8)   # Reduce highs
            ])
        elif preset == 'Stüdyo':
            # Professional studio sound with clarity and presence
            return self._apply_eq_filter(y, sr, [
                (60, 0.7),    # Reduce sub-bass rumble
                (120, 1.1),   # Slight boost to bass for warmth
                (250, 0.9),   # Cut muddiness
                (500, 0.95),  # Slight cut to prevent boxiness
                (1000, 1.05), # Slight boost for presence
                (2000, 1.15), # Boost for vocal clarity
                (3500, 1.25), # Boost for presence and articulation
                (5000, 1.2),  # Boost for presence
                (8000, 1.1),  # Slight boost for air
                (12000, 1.15) # Boost for sparkle and air
            ])
        else:  # 'Özel' or any other preset
            # Balanced EQ
            return self._apply_eq_filter(y, sr, [
                (100, 1.1),   # Slight boost to low end
                (1000, 1.1),  # Slight boost to mids
                (5000, 1.1)   # Slight boost to highs
            ])
    
    def _apply_eq_filter(self, y, sr, bands):
        """Apply multi-band EQ filter"""
        # Create a copy of the audio
        y_filtered = np.copy(y)
        
        # Apply each band
        for freq, gain in bands:
            # Design bandpass filter
            b, a = signal.butter(2, [(freq * 0.7) / (sr / 2), (freq * 1.3) / (sr / 2)], btype='band')
            
            # Apply filter to get the band
            y_band = signal.lfilter(b, a, y)
            
            # Apply gain and add to output
            y_filtered = y_filtered + (y_band * (gain - 1))
        
        return y_filtered
    
    def _apply_compression(self, y, amount):
        """Apply dynamic range compression"""
        # Calculate threshold based on amount (higher amount = lower threshold)
        threshold = 0.5 - (amount * 0.4)  # Threshold between 0.1 and 0.5
        
        # Calculate ratio based on amount (higher amount = higher ratio)
        ratio = 1 + (amount * 5)  # Ratio between 1:1 and 6:1
        
        # Apply compression
        y_compressed = np.zeros_like(y)
        for i in range(len(y)):
            if abs(y[i]) > threshold:
                # Compress the signal above threshold
                y_compressed[i] = threshold + (abs(y[i]) - threshold) / ratio
                # Preserve the sign
                if y[i] < 0:
                    y_compressed[i] = -y_compressed[i]
            else:
                y_compressed[i] = y[i]
        
        # Apply a slight makeup gain to compensate for compression
        makeup_gain = 1.0 + (amount * 0.3)  # More compression = more makeup gain
        y_compressed = y_compressed * makeup_gain
        
        return y_compressed
    
    def _normalize_audio(self, y):
        """Normalize audio to optimal level"""
        # Find the maximum amplitude
        max_amp = np.max(np.abs(y))
        
        # Target amplitude (slightly below 0 dB to prevent clipping)
        target_amp = 0.95
        
        # Normalize if needed
        if max_amp > 0:
            y_normalized = y * (target_amp / max_amp)
            return y_normalized
        else:
            return y
    
    def _convert_to_mp3(self, wav_file, mp3_file):
        """Convert WAV to MP3 using pydub"""
        try:
            audio = AudioSegment.from_wav(wav_file)
            audio.export(mp3_file, format="mp3", bitrate="192k")
            return True
        except Exception as e:
            # If FFmpeg is not found, just keep the WAV file
            if "ffmpeg" in str(e).lower():
                print(f"FFmpeg not found, keeping WAV format: {e}")
                return False
            else:
                # Re-raise other exceptions
                raise
