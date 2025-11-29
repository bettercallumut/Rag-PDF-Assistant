import math
import random
import numpy as np
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QFont, QLinearGradient, QRadialGradient

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
        self.frequency_bands = [0.0] * 32
        self.wave_points = []
        self.particles = []
        self.ring_pulses = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.init_particles()

    def init_particles(self):
        self.particles = []
        for _ in range(40):
            self.particles.append({
                'angle': random.uniform(0, math.pi * 2),
                'dist': random.uniform(0.8, 1.5),
                'speed': random.uniform(0.3, 1.0),
                'size': random.uniform(2, 5),
                'phase': random.uniform(0, math.pi * 2)
            })

    def set_audio_data(self, file_path):
        try:
            import imageio_ffmpeg
            from pydub import AudioSegment
            AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()
            audio = AudioSegment.from_mp3(file_path)
            audio = audio.set_channels(1)
            self.sample_rate = audio.frame_rate
            samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
            samples = samples / (2**15)
            self.audio_data = samples
            self.audio_position = 0
            self.samples_per_frame = int(self.sample_rate / 60)
        except Exception as e:
            print(f"Audio error: {e}")
            self.audio_data = None

    def start(self):
        self.active = True
        self.time = 0.0
        self.audio_position = 0
        self.frequency_bands = [0.0] * 32
        self.ring_pulses = []
        self.timer.start(16)
        self.setVisible(True)

    def stop(self):
        self.active = False
        self.timer.stop()
        self.audio_data = None
        self.setVisible(False)

    def update_animation(self):
        if not self.active:
            return
        self.time += 0.016
        if self.audio_data is not None and len(self.audio_data) > 0:
            end_pos = min(self.audio_position + self.samples_per_frame, len(self.audio_data))
            if self.audio_position < len(self.audio_data):
                chunk = self.audio_data[self.audio_position:end_pos]
                self.audio_position = end_pos
                if len(chunk) > 64:
                    self.analyze_frequencies(chunk)
        else:
            for i in range(32):
                target = random.uniform(0.1, 0.5)
                self.frequency_bands[i] += (target - self.frequency_bands[i]) * 0.2
        for p in self.particles:
            p['angle'] += p['speed'] * 0.02
        avg_intensity = sum(self.frequency_bands) / len(self.frequency_bands)
        if avg_intensity > 0.3 and random.random() < 0.1:
            self.ring_pulses.append({'radius': 0, 'opacity': 1.0, 'speed': 2 + avg_intensity * 3})
        for ring in self.ring_pulses[:]:
            ring['radius'] += ring['speed']
            ring['opacity'] -= 0.02
            if ring['opacity'] <= 0:
                self.ring_pulses.remove(ring)
        self.update()

    def analyze_frequencies(self, chunk):
        n = len(chunk)
        window = np.hanning(n)
        windowed = chunk * window
        fft = np.fft.rfft(windowed)
        magnitude = np.abs(fft)
        if len(magnitude) > 1:
            magnitude = magnitude[1:]
        num_bins = len(magnitude)
        bands = 32
        for i in range(bands):
            start_idx = int((i / bands) ** 1.5 * num_bins)
            end_idx = int(((i + 1) / bands) ** 1.5 * num_bins)
            if start_idx < num_bins and end_idx > start_idx:
                avg_mag = np.mean(magnitude[start_idx:end_idx])
                normalized = min(1.0, avg_mag / 300)
                self.frequency_bands[i] = self.frequency_bands[i] * 0.4 + normalized * 0.6

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2
        base_radius = min(w, h) * 0.25
        bg = QRadialGradient(cx, cy, max(w, h))
        bg.setColorAt(0, QColor(10, 10, 20))
        bg.setColorAt(1, QColor(5, 5, 10))
        painter.fillRect(self.rect(), bg)
        if not self.active:
            painter.setPen(QColor(60, 60, 80))
            painter.setFont(QFont("Segoe UI", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "AI Voice")
            return
        avg_intensity = sum(self.frequency_bands) / len(self.frequency_bands)
        for ring in self.ring_pulses:
            ring_color = QColor(0, 200, 255, int(ring['opacity'] * 100))
            painter.setPen(QPen(ring_color, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(QPointF(cx, cy), ring['radius'] + base_radius, ring['radius'] + base_radius)
        glow_size = base_radius * (1.2 + avg_intensity * 0.5)
        for i in range(4):
            glow_r = glow_size + i * 15
            alpha = int(40 - i * 10)
            glow = QRadialGradient(cx, cy, glow_r)
            glow.setColorAt(0, QColor(0, 150, 255, alpha))
            glow.setColorAt(0.5, QColor(100, 0, 255, alpha // 2))
            glow.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(glow)
            painter.drawEllipse(QPointF(cx, cy), glow_r, glow_r)
        num_bands = len(self.frequency_bands)
        for i, band_value in enumerate(self.frequency_bands):
            angle = (i / num_bands) * math.pi * 2 - math.pi / 2
            inner_r = base_radius * 0.6
            outer_r = base_radius * (0.6 + band_value * 0.8)
            x1 = cx + math.cos(angle) * inner_r
            y1 = cy + math.sin(angle) * inner_r
            x2 = cx + math.cos(angle) * outer_r
            y2 = cy + math.sin(angle) * outer_r
            hue = 180 + band_value * 60
            color = QColor.fromHsv(int(hue) % 360, 255, 255, 200)
            painter.setPen(QPen(color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            mirror_angle = math.pi - angle
            x1m = cx + math.cos(mirror_angle) * inner_r
            y1m = cy + math.sin(mirror_angle) * inner_r
            x2m = cx + math.cos(mirror_angle) * outer_r
            y2m = cy + math.sin(mirror_angle) * outer_r
            painter.drawLine(QPointF(x1m, y1m), QPointF(x2m, y2m))
        for p in self.particles:
            dist = p['dist'] + avg_intensity * 0.3
            px = cx + math.cos(p['angle']) * base_radius * dist
            py = cy + math.sin(p['angle']) * base_radius * dist
            pulse = 0.5 + 0.5 * math.sin(self.time * 3 + p['phase'])
            size = p['size'] * (0.5 + pulse * 0.5 + avg_intensity)
            alpha = int(150 + 100 * pulse)
            particle_color = QColor(100, 200, 255, alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(particle_color)
            painter.drawEllipse(QPointF(px, py), size, size)
        core_pulse = 1 + 0.15 * math.sin(self.time * 4) + avg_intensity * 0.3
        core_r = base_radius * 0.35 * core_pulse
        core = QRadialGradient(cx, cy, core_r)
        core.setColorAt(0, QColor(255, 255, 255, 255))
        core.setColorAt(0.3, QColor(100, 200, 255, 200))
        core.setColorAt(0.6, QColor(80, 100, 255, 150))
        core.setColorAt(1, QColor(50, 0, 150, 0))
        painter.setBrush(core)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(cx, cy), core_r, core_r)
        wave_r = base_radius * 0.5
        painter.setPen(QPen(QColor(150, 220, 255, 180), 2))
        points = []
        for i in range(60):
            angle = (i / 60) * math.pi * 2
            band_idx = int((i / 60) * len(self.frequency_bands)) % len(self.frequency_bands)
            wave_offset = self.frequency_bands[band_idx] * 15
            r = wave_r + wave_offset + 3 * math.sin(self.time * 5 + angle * 3)
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            points.append(QPointF(x, y))
        if points:
            points.append(points[0])
            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i + 1])
