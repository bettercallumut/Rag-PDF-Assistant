import math
import random
import numpy as np
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF, QElapsedTimer
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QFont, QLinearGradient, QRadialGradient, QPainterPath

class SpeakingVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(220)
        self.active = False
        self.time = 0.0
        self.audio_data = None
        self.audio_position = 0
        self.sample_rate = 44100
        self.samples_per_frame = 735
        self.frequency_bands = [0.0] * 64  # Daha fazla band = daha smooth waveform
        self.frame_count = 0
        self.stopwatch = QElapsedTimer()
        self.stopwatch.start()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        
        # TEMPORAL SMOOTHING - DENGELİ ayarlar
        self.frequency_history = []  # Son N frame'in band değerleri
        self.history_length = 8  # 8 frame buffer (~130ms) - Responsive!
        self.peak_values = [0.0] * 64  # Peak hold mekanizması
        self.peak_decay = 0.97  # DENGELİ - smooth ama responsive

    def set_audio_data(self, file_path):
        try:
            import wave
            import subprocess
            import tempfile
            import os
            import struct
            self.audio_data = None
            wav_path = file_path
            temp_wav = None
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            fd, temp_wav = tempfile.mkstemp(suffix='.wav')
            os.close(fd)
            try:
                subprocess.run([
                    ffmpeg_exe, "-y", "-i", file_path, 
                    "-vn", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "44100", 
                    "-f", "wav", temp_wav
                ], check=True, stdout=subprocess.DEVNULL, stderr=None)
                wav_path = temp_wav
            except Exception as e_ffmpeg:
                try:
                    subprocess.run([
                        "ffmpeg", "-y", "-i", file_path, 
                        "-vn", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "44100", 
                        "-f", "wav", temp_wav
                    ], check=True, stdout=subprocess.DEVNULL, stderr=None)
                    wav_path = temp_wav
                except Exception as e_sys:
                    wav_path = file_path

            try:
                with wave.open(wav_path, 'rb') as wf:
                    self.sample_rate = wf.getframerate()
                    n_frames = wf.getnframes()
                    raw_bytes = wf.readframes(n_frames)
                    if wf.getsampwidth() == 2:
                        total_samples = len(raw_bytes) // 2
                        fmt = f"{total_samples}h"
                        samples = struct.unpack(fmt, raw_bytes)
                        samples = np.array(samples, dtype=np.float32)
                        samples = samples / 32768.0
                    else:
                        raise ValueError("Only 16-bit PCM supported by simple reader")
                    self.audio_data = samples
            except Exception as e_wave:
                try:
                    with open(wav_path, 'rb') as f:
                        f.seek(0)
                        header = f.read(44)
                        audio_fmt = struct.unpack('<H', header[20:22])[0]
                        n_channels = struct.unpack('<H', header[22:24])[0]
                        self.sample_rate = struct.unpack('<I', header[24:28])[0]
                        bits_per_sample = struct.unpack('<H', header[34:36])[0]
                        f.seek(0)
                        raw = f.read()
                        data_offset = raw.find(b'data')
                        if data_offset != -1:
                            data_offset += 8
                        else:
                            data_offset = 44
                        if bits_per_sample == 16:
                            samples = np.frombuffer(raw, dtype=np.int16, offset=data_offset)
                            samples = samples.astype(np.float32) / 32768.0
                        elif bits_per_sample == 32:
                            if audio_fmt == 3:
                                samples = np.frombuffer(raw, dtype=np.float32, offset=data_offset)
                            else:
                                samples = np.frombuffer(raw, dtype=np.int32, offset=data_offset)
                                samples = samples.astype(np.float32) / 2147483648.0
                        else:
                            raise ValueError(f"Unsupported bits: {bits_per_sample}")
                        if n_channels > 1:
                            samples = samples[::n_channels]
                        self.audio_data = samples
                except Exception as e_manual:
                    raise e_wave


            self.duration_ms = (len(self.audio_data) / self.sample_rate) * 1000
            if temp_wav and os.path.exists(temp_wav):
                os.remove(temp_wav)
            self.audio_position = 0
            self.samples_per_frame = int(self.sample_rate / 60)
            self.frame_count = 0
            self.time = 0.0
            self.active = True
            self.stopwatch = QElapsedTimer()
            self.stopwatch.start()
            if not self.timer.isActive():
                self.timer.start(16)
            self.setVisible(True)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.audio_data = None

    def start(self):
        self.active = True
        self.time = 0.0
        self.frame_count = 0
        self.frequency_bands = [0.0] * 64
        self.stopwatch = QElapsedTimer()
        self.stopwatch.start()
        if not self.timer.isActive():
            self.timer.start(16)
        self.setVisible(True)

    def stop(self):
        self.active = False
        self.timer.stop()
        self.audio_data = None
        self.setVisible(False)

    def update_animation(self):
        if hasattr(self, 'frame_count'):
            self.frame_count += 1
        if not self.active:
            return
        current_time_ms = self.stopwatch.elapsed()
        self.time += 0.016 

        if self.audio_data is not None and len(self.audio_data) > 0:
            sample_pos = int((current_time_ms / 1000.0) * self.sample_rate)
            if sample_pos < len(self.audio_data):
                start = sample_pos
                end = min(sample_pos + self.samples_per_frame, len(self.audio_data))
                chunk = self.audio_data[start:end]
                if len(chunk) > 32:
                    self.analyze_frequencies(chunk)
                else:
                    self.fade_out_bands()
            else:
                self.fade_out_bands()
        else:
            for i in range(len(self.frequency_bands)):
                self.frequency_bands[i] = abs(math.sin(self.time * 1.5 + i * 0.1)) * 0.04
        self.update()

    def fade_out_bands(self):
        # DENGELİ süzülme - responsive ama smooth
        for i in range(len(self.frequency_bands)):
            self.frequency_bands[i] *= 0.93  # DENGELİ - orta hız
            
    def analyze_frequencies(self, chunk):
        n = len(chunk)
        window = np.hanning(n)
        windowed = chunk * window
        fft = np.fft.rfft(windowed)
        magnitude = np.abs(fft)
        if len(magnitude) > 1:
            magnitude = magnitude[1:]
        num_bins = len(magnitude)
        bands = len(self.frequency_bands)
        for i in range(bands):
            start_idx = int((i / bands) ** 1.5 * num_bins)
            end_idx = int(((i + 1) / bands) ** 1.5 * num_bins)
            if start_idx < num_bins and end_idx > start_idx:
                avg_mag = np.mean(magnitude[start_idx:end_idx])
                # NORMALIZATION - Düşürüldü - daha güçlü FFT!
                normalized = min(1.0, avg_mag / 100)  # 150'den 100'e DÜŞTÜ!
                # SMOOTH EASING - Yükselme çok hızlı, düşme orta yavaş
                if normalized > self.frequency_bands[i]:
                    # YÜKSELİRKEN - çok hızlı (0.8 ağırlık) - RESPONSIVE!
                    self.frequency_bands[i] = self.frequency_bands[i] * 0.2 + normalized * 0.8
                else:
                    # DÜŞERKEN - orta yavaş (0.25 ağırlık) - DENGELİ
                    self.frequency_bands[i] = self.frequency_bands[i] * 0.75 + normalized * 0.25
        self.frequency_history.append(self.frequency_bands.copy())
        if len(self.frequency_history) > self.history_length:
            self.frequency_history.pop(0)
        if len(self.frequency_history) > 1:
            weights = np.linspace(0.5, 1.0, len(self.frequency_history))
            weights = weights / np.sum(weights)
            smoothed = np.zeros(len(self.frequency_bands))
            for i, hist in enumerate(self.frequency_history):
                smoothed += np.array(hist) * weights[i]
            self.frequency_bands = smoothed.tolist()
        for i in range(len(self.frequency_bands)):
            if self.frequency_bands[i] > self.peak_values[i]:
                self.peak_values[i] = self.frequency_bands[i]
            else:
                self.peak_values[i] *= self.peak_decay
                self.frequency_bands[i] = max(self.frequency_bands[i], self.peak_values[i])

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2
        
        # Dark gradient background - Siri style
        bg_grad = QLinearGradient(0, 0, 0, h)
        bg_grad.setColorAt(0, QColor(5, 5, 15))
        bg_grad.setColorAt(0.5, QColor(10, 8, 20))
        bg_grad.setColorAt(1, QColor(5, 5, 15))
        painter.fillRect(self.rect(), bg_grad)

        if not self.active:
            painter.setPen(QColor(80, 80, 100))
            painter.setFont(QFont("Segoe UI", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Asistan Hazır")
            return

        avg_intensity = sum(self.frequency_bands) / len(self.frequency_bands)
        
        glow_radius = min(w, h) * 0.35
        glow_pulse = 1.0 + avg_intensity * 0.8
        for i in range(4):
            layer_radius = glow_radius * glow_pulse * (1.0 + i * 0.15)
            layer_alpha = int(30 - i * 6)
            glow_grad = QRadialGradient(cx, cy, layer_radius)
            glow_grad.setColorAt(0, QColor(0, 200, 200, layer_alpha))
            glow_grad.setColorAt(0.7, QColor(0, 150, 180, layer_alpha // 2))
            glow_grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(glow_grad)
            painter.drawEllipse(QPointF(cx, cy), layer_radius, layer_radius)
        ring_pen = QPen(QColor(0, 200, 200, 140), 2.5)
        painter.setPen(ring_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), glow_radius * glow_pulse, glow_radius * glow_pulse)
        
        # 3. HORIZONTAL WAVEFORM (Center - Siri style) - DENG ELİ!
        wave_width = min(w, h) * 0.55
        wave_height_max = min(w, h) * 0.28  # Azaltıldı - daha kontrollü
        
        # Create smooth waveform points
        num_points = 80
        wave_points_top = []
        wave_points_bottom = []
        
        for i in range(num_points):
            # Horizontal position
            t = (i / (num_points - 1)) - 0.5  # -0.5 to 0.5
            x = cx + t * wave_width * 2
            
            # Get frequency intensity for this position
            band_idx = int(abs(t) * (len(self.frequency_bands) - 1))
            intensity = self.frequency_bands[band_idx]
            
            # Ses varken dalgalı, yokken estetik çizgi
            if avg_intensity > 0.01:  # Threshold düştü - daha hassas!
                # Add flowing wave motion - KONTROLLÜ
                wave_phase = self.time * 4 + i * 0.3
                base_wave = math.sin(wave_phase) * 12  # 20'den 12'ye - daha kontrollü
                
                # Intensity amplification - DENG ELİ
                wave_amplitude = (intensity * wave_height_max * 4.5) + base_wave + 18  # 6.4x->4.5x, 32px->18px
                
                # Smooth falloff at edges
                edge_falloff = 1.0 - (abs(t) * 1.5) ** 2
                wave_amplitude *= max(0.4, edge_falloff)
                
                # MAX CLAMP - Ekranın %35'inden fazla çıkmasın!
                max_amplitude = h * 0.35
                wave_amplitude = min(wave_amplitude, max_amplitude)
                
            else:  # Ses yoksa - estetik horizontal çizgi
                # Hafif dalga efekti - Kontrollü
                gentle_wave = math.sin(self.time * 2 + i * 0.25) * 2  # 3'ten 2'ye
                wave_amplitude = 5 + gentle_wave  # 6'dan 5'e
            
            # Top and bottom points
            y_top = cy - wave_amplitude
            y_bottom = cy + wave_amplitude
            
            wave_points_top.append(QPointF(x, y_top))
            wave_points_bottom.append(QPointF(x, y_bottom))
        
        # Draw waveform with gradient
        # Create path for filled waveform
        path = QPainterPath()
        path.moveTo(wave_points_top[0])
        
        # Top curve
        for point in wave_points_top:
            path.lineTo(point)
        
        # Bottom curve (reversed)
        for point in reversed(wave_points_bottom):
            path.lineTo(point)
        
        path.closeSubpath()
        
        # Gradient fill - Blue to Pink (Siri colors)
        wave_grad = QLinearGradient(cx - wave_width, cy, cx + wave_width, cy)
        wave_grad.setColorAt(0, QColor(100, 150, 255, int(180 + avg_intensity * 75)))  # Blue
        wave_grad.setColorAt(0.5, QColor(200, 100, 255, int(200 + avg_intensity * 55)))  # Purple
        wave_grad.setColorAt(1, QColor(255, 100, 200, int(180 + avg_intensity * 75)))  # Pink
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(wave_grad)
        painter.drawPath(path)
        
        # Draw bright center line
        center_line_grad = QLinearGradient(cx - wave_width, cy, cx + wave_width, cy)
        center_line_grad.setColorAt(0, QColor(150, 200, 255, 250))
        center_line_grad.setColorAt(0.5, QColor(255, 150, 255, 255))
        center_line_grad.setColorAt(1, QColor(255, 150, 200, 250))
        
        center_pen = QPen(QBrush(center_line_grad), 3)
        center_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(center_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        # Draw center line
        for i in range(len(wave_points_top) - 1):
            y_avg = (wave_points_top[i].y() + wave_points_bottom[i].y()) / 2
            y_avg_next = (wave_points_top[i+1].y() + wave_points_bottom[i+1].y()) / 2
            painter.drawLine(
                QPointF(wave_points_top[i].x(), y_avg),
                QPointF(wave_points_top[i+1].x(), y_avg_next)
            )
        
        # 4. Center Orb (pulsating)
        orb_radius = 8 + avg_intensity * 12
        orb_grad = QRadialGradient(cx, cy, orb_radius * 2)
        orb_grad.setColorAt(0, QColor(255, 255, 255, 240))
        orb_grad.setColorAt(0.4, QColor(200, 150, 255, 200))
        orb_grad.setColorAt(1, QColor(0, 0, 0, 0))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(orb_grad)
        painter.drawEllipse(QPointF(cx, cy), orb_radius * 2, orb_radius * 2)
