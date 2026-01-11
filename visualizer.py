import math
import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QFont, QLinearGradient, QRadialGradient

class ThinkingVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.animating = False
        self.time = 0.0
        self.rotation = 0.0
        self.sphere_nodes = []
        self.outer_particles = []
        self.energy_rays = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.init_sphere()
        self.init_particles()

    def init_sphere(self):
        self.sphere_nodes = []
        phi = (1 + math.sqrt(5)) / 2
        base_points = [
            (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi),
            (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
            (phi, 0, 1), (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1)
        ]
        for x, y, z in base_points:
            length = math.sqrt(x*x + y*y + z*z)
            self.sphere_nodes.append({
                'x': x/length, 'y': y/length, 'z': z/length,
                'active': 0, 'pulse': random.uniform(0, math.pi*2)
            })
        for i in range(20):
            theta = random.uniform(0, math.pi * 2)
            phi_angle = random.uniform(-math.pi/2, math.pi/2)
            x = math.cos(phi_angle) * math.cos(theta)
            y = math.cos(phi_angle) * math.sin(theta)
            z = math.sin(phi_angle)
            self.sphere_nodes.append({
                'x': x, 'y': y, 'z': z,
                'active': 0, 'pulse': random.uniform(0, math.pi*2)
            })

    def init_particles(self):
        self.outer_particles = []
        for _ in range(60):
            self.outer_particles.append({
                'angle': random.uniform(0, math.pi * 2),
                'dist': random.uniform(1.2, 2.5),
                'speed': random.uniform(0.5, 2.0),
                'z': random.uniform(-0.5, 0.5),
                'size': random.uniform(1, 3),
                'color_shift': random.uniform(0, 1)
            })

    def start_animation(self):
        self.animating = True
        self.time = 0.0
        self.timer.start(16)
        self.setVisible(True)
        self.energy_rays = []

    def stop_animation(self):
        self.animating = False
        self.timer.stop()
        self.setVisible(False)

    def update_animation(self):
        if not self.animating:
            return
        self.time += 0.016
        self.rotation += 0.012
        for node in self.sphere_nodes:
            node['pulse'] += 0.05
            if random.random() < 0.03:
                node['active'] = 15
            if node['active'] > 0:
                node['active'] -= 1
        for p in self.outer_particles:
            p['angle'] += p['speed'] * 0.02
        if random.random() < 0.08:
            self.energy_rays.append({
                'angle': random.uniform(0, math.pi * 2),
                'length': 0,
                'max_length': random.uniform(0.5, 1.5),
                'speed': random.uniform(0.05, 0.15),
                'width': random.uniform(1, 3)
            })
        for ray in self.energy_rays[:]:
            ray['length'] += ray['speed']
            if ray['length'] > ray['max_length']:
                self.energy_rays.remove(ray)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2
        base_radius = min(w, h) * 0.28
        bg_gradient = QRadialGradient(cx, cy, max(w, h))
        bg_gradient.setColorAt(0, QColor(15, 15, 25))
        bg_gradient.setColorAt(1, QColor(5, 5, 10))
        painter.fillRect(self.rect(), bg_gradient)
        if not self.animating:
            return
        for i in range(3):
            glow_radius = base_radius * (1.3 + i * 0.15)
            glow_color = QColor(0, 255, 255, int(25 / (i + 1)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(glow_color)
            painter.drawEllipse(QPointF(cx, cy), glow_radius, glow_radius)
        for ray in self.energy_rays:
            start_x = cx + math.cos(ray['angle']) * base_radius
            start_y = cy + math.sin(ray['angle']) * base_radius
            end_x = cx + math.cos(ray['angle']) * (base_radius + ray['length'] * base_radius)
            end_y = cy + math.sin(ray['angle']) * (base_radius + ray['length'] * base_radius)
            ray_gradient = QLinearGradient(start_x, start_y, end_x, end_y)
            ray_gradient.setColorAt(0, QColor(0, 255, 255, 200))
            ray_gradient.setColorAt(0.5, QColor(255, 0, 255, 150))
            ray_gradient.setColorAt(1, QColor(255, 0, 255, 0))
            pen = QPen(QBrush(ray_gradient), ray['width'])
            painter.setPen(pen)
            painter.drawLine(QPointF(start_x, start_y), QPointF(end_x, end_y))
        for p in self.outer_particles:
            px = cx + math.cos(p['angle']) * p['dist'] * base_radius
            py = cy + math.sin(p['angle']) * p['dist'] * base_radius * 0.6
            hue_shift = (p['color_shift'] + self.time * 0.1) % 1.0
            if hue_shift < 0.5:
                color = QColor(int(255 * hue_shift * 2), 255, 255, 180)
            else:
                color = QColor(255, int(255 * (1 - hue_shift) * 2), 255, 180)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawEllipse(QPointF(px, py), p['size'], p['size'])
        sorted_nodes = sorted(self.sphere_nodes, key=lambda n: n['z'])
        for i, n1 in enumerate(sorted_nodes):
            scale1 = 1 + n1['z'] * 0.3
            x1 = cx + (n1['x'] * math.cos(self.rotation) - n1['y'] * math.sin(self.rotation)) * base_radius * scale1
            y1 = cy + n1['z'] * base_radius * 0.6 * scale1
            for n2 in sorted_nodes[i+1:]:
                dist = math.sqrt((n1['x']-n2['x'])**2 + (n1['y']-n2['y'])**2 + (n1['z']-n2['z'])**2)
                if dist < 0.8:
                    scale2 = 1 + n2['z'] * 0.3
                    x2 = cx + (n2['x'] * math.cos(self.rotation) - n2['y'] * math.sin(self.rotation)) * base_radius * scale2
                    y2 = cy + n2['z'] * base_radius * 0.6 * scale2
                    opacity = int(120 * (1 - dist / 0.8))
                    line_color = QColor(0, 220, 220, opacity)
                    painter.setPen(QPen(line_color, 1))
                    painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        for node in sorted_nodes:
            scale = 1 + node['z'] * 0.3
            x = cx + (node['x'] * math.cos(self.rotation) - node['y'] * math.sin(self.rotation)) * base_radius * scale
            y = cy + node['z'] * base_radius * 0.6 * scale
            pulse_size = 1 + 0.3 * math.sin(node['pulse'])
            if node['active'] > 0:
                size = 5 * pulse_size
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(0, 255, 255), 2))
            else:
                size = 3 * pulse_size
                brightness = int(100 + 50 * (0.5 + node['z']))
                painter.setBrush(QColor(0, brightness, brightness))
                painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(x, y), size, size)
        core_pulse = 1 + 0.2 * math.sin(self.time * 3)
        core_gradient = QRadialGradient(cx, cy, base_radius * 0.3 * core_pulse)
        core_gradient.setColorAt(0, QColor(255, 255, 255, 200))
        core_gradient.setColorAt(0.3, QColor(0, 255, 255, 150))
        core_gradient.setColorAt(0.7, QColor(255, 0, 255, 80))
        core_gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(core_gradient)
        painter.drawEllipse(QPointF(cx, cy), base_radius * 0.3 * core_pulse, base_radius * 0.3 * core_pulse)
