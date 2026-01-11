from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

import os
from threading import Thread
from collections import deque

import config
from rag_system import RAGSystem
from workers import QueryWorker, SummaryWorker, PersistentTTSWorker

try:
    from android.media import MediaPlayer
    HAS_ANDROID_MEDIA = True
except:
    HAS_ANDROID_MEDIA = False
    try:
        from kivy.core.audio import SoundLoader
    except:
        SoundLoader = None


class ModernButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex('#6366F1')
        self.color = get_color_from_hex('#FFFFFF')
        self.font_size = dp(14)
        self.size_hint_y = None
        self.height = dp(48)
        self.bold = True


class PDFAssistantApp(App):
    def build(self):
        self.title = "PDF Asistanı"
        self.rag_system = None
        self.tts_enabled = True
        self.audio_queue = deque()
        self.is_playing_audio = False
        self.persistent_tts = None
        
        Window.clearcolor = get_color_from_hex('#18181B')
        
        self.root_layout = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(10)
        )
        
        top_panel = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10),
            padding=[dp(5), 0]
        )
        
        title_label = Label(
            text="PDF Asistanı",
            font_size=dp(20),
            bold=True,
            color=get_color_from_hex('#F4F4F5')
        )
        
        self.status_label = Label(
            text="Başlatılıyor...",
            font_size=dp(12),
            color=get_color_from_hex('#A1A1AA')
        )
        
        top_panel.add_widget(title_label)
        top_panel.add_widget(self.status_label)
        
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=dp(4)
        )
        
        self.chat_scroll = ScrollView(size_hint=(1, 0.5))
        self.chat_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8),
            padding=dp(10)
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        
        input_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(8),
            padding=[0, dp(5)]
        )
        
        self.input_field = TextInput(
            hint_text="Soru sorun...",
            multiline=False,
            font_size=dp(14),
            size_hint_y=None,
            height=dp(48),
            background_color=get_color_from_hex('#27272A'),
            foreground_color=get_color_from_hex('#F4F4F5'),
            cursor_color=get_color_from_hex('#6366F1'),
            padding=[dp(12), dp(12)]
        )
        self.input_field.bind(on_text_validate=self.send_query)
        
        btn_row = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8)
        )
        
        self.btn_send = ModernButton(text="GÖNDER")
        self.btn_send.bind(on_press=self.send_query)
        self.btn_send.disabled = True
        
        btn_row.add_widget(self.btn_send)
        
        input_container.add_widget(self.input_field)
        input_container.add_widget(btn_row)
        
        control_panel = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8)
        )
        
        self.btn_load = ModernButton(text="📁 PDF Yükle")
        self.btn_load.bind(on_press=self.load_pdf)
        self.btn_load.disabled = True
        
        self.btn_tts = ModernButton(text="🔊 Sesli")
        self.btn_tts.background_color = get_color_from_hex('#4ADE80')
        self.btn_tts.bind(on_press=self.toggle_tts)
        
        control_panel.add_widget(self.btn_load)
        control_panel.add_widget(self.btn_tts)
        
        self.root_layout.add_widget(top_panel)
        self.root_layout.add_widget(self.progress)
        self.root_layout.add_widget(self.chat_scroll)
        self.root_layout.add_widget(input_container)
        self.root_layout.add_widget(control_panel)
        
        Clock.schedule_once(self.init_system, 0.5)
        
        return self.root_layout
    
    def init_system(self, dt):
        try:
            self.rag_system = RAGSystem()
            self.update_status("Hazır")
            self.btn_load.disabled = False
            self.add_message("SİSTEM", "✅ Asistan hazır. PDF yükleyin.", "#A1A1AA")
            
            self.tts_enabled = False
            self.btn_tts.text = "🔇 TTS Kapalı"
            self.btn_tts.background_color = get_color_from_hex('#F87171')
            self.btn_tts.disabled = True
            
        except Exception as e:
            self.update_status("❌ Hata")
            self.add_message("HATA", f"Başlatma hatası: {str(e)}", "#F87171")
    
    @mainthread
    def update_status(self, status):
        self.status_label.text = status
    
    @mainthread
    def add_message(self, sender, message, color_hex):
        msg_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(12),
            spacing=dp(5)
        )
        msg_container.bind(minimum_height=msg_container.setter('height'))
        
        sender_label = Label(
            text=sender,
            font_size=dp(11),
            bold=True,
            color=get_color_from_hex(color_hex),
            size_hint_y=None,
            height=dp(20),
            halign='left',
            valign='middle'
        )
        sender_label.bind(size=sender_label.setter('text_size'))
        
        msg_label = Label(
            text=message,
            font_size=dp(13),
            color=get_color_from_hex('#F4F4F5'),
            size_hint_y=None,
            halign='left',
            valign='top',
            padding=[dp(5), dp(5)]
        )
        msg_label.bind(
            width=lambda *x: setattr(msg_label, 'text_size', (msg_label.width, None)),
            texture_size=lambda *x: setattr(msg_label, 'height', msg_label.texture_size[1] + dp(10))
        )
        
        msg_container.add_widget(sender_label)
        msg_container.add_widget(msg_label)
        
        self.chat_layout.add_widget(msg_container)
        Clock.schedule_once(lambda dt: setattr(self.chat_scroll, 'scroll_y', 0), 0.1)
    
    def load_pdf(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        filechooser = FileChooserIconView(
            filters=['*.pdf'],
            size_hint=(1, 0.85)
        )
        
        btn_layout = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8)
        )
        
        btn_select = ModernButton(text="✓ Seç")
        btn_select.background_color = get_color_from_hex('#4ADE80')
        
        btn_cancel = ModernButton(text="✗ İptal")
        btn_cancel.background_color = get_color_from_hex('#F87171')
        
        btn_layout.add_widget(btn_select)
        btn_layout.add_widget(btn_cancel)
        
        content.add_widget(filechooser)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='PDF Dosyası Seç',
            content=content,
            size_hint=(0.95, 0.9),
            background_color=get_color_from_hex('#27272A')
        )
        
        def select_file(*args):
            if filechooser.selection:
                pdf_path = filechooser.selection[0]
                popup.dismiss()
                Clock.schedule_once(lambda dt: self.process_pdf(pdf_path), 0.2)
        
        def cancel(*args):
            popup.dismiss()
        
        btn_select.bind(on_release=select_file)
        btn_cancel.bind(on_release=cancel)
        
        popup.open()
    
    def process_pdf(self, pdf_path):
        self.update_status("⏳ PDF işleniyor...")
        self.btn_load.disabled = True
        self.btn_send.disabled = True
        self.add_message("SİSTEM", f"📄 {os.path.basename(pdf_path)} yükleniyor...", "#38BDF8")
        
        def load_thread():
            try:
                count = self.rag_system.process_pdf(
                    pdf_path,
                    lambda x: Clock.schedule_once(lambda dt: self.update_progress(x), 0)
                )
                Clock.schedule_once(lambda dt: self.on_pdf_loaded(count), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.add_message("HATA", str(e), "#F87171"), 0)
                Clock.schedule_once(lambda dt: self.on_pdf_loaded(0), 0)
        
        Thread(target=load_thread, daemon=True).start()
    
    @mainthread
    def update_progress(self, value):
        self.progress.value = value
    
    @mainthread
    def on_pdf_loaded(self, count):
        self.update_progress(100)
        self.btn_load.disabled = False
        self.btn_send.disabled = False
        
        if count > 0:
            self.update_status("✅ Hazır")
            self.add_message("SİSTEM", f"✓ {count} sayfa analiz edildi. Soru sorabilirsiniz.", "#4ADE80")
        else:
            self.update_status("❌ Hata")
            self.add_message("HATA", "PDF yüklenemedi", "#F87171")
        
        Clock.schedule_once(lambda dt: self.update_progress(0), 1.5)
    
    def send_query(self, instance=None):
        text = self.input_field.text.strip()
        if not text or not self.rag_system:
            return
        
        self.input_field.text = ""
        self.add_message("SEN", text, "#38BDF8")
        self.btn_send.disabled = True
        self.update_status("🤔 Düşünüyor...")
        
        def query_thread():
            try:
                result = self.rag_system.query(text, config.API_KEY)
                Clock.schedule_once(lambda dt: self.on_query_result(result), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.add_message("HATA", str(e), "#F87171"), 0)
                Clock.schedule_once(lambda dt: self.reset_ui(), 0)
        
        Thread(target=query_thread, daemon=True).start()
    
    @mainthread
    def on_query_result(self, result):
        self.add_message("ASİSTAN", result, "#4ADE80")
        self.reset_ui()
    
    @mainthread
    def reset_ui(self):
        self.btn_send.disabled = False
        self.update_status("✅ Hazır")
    
    def toggle_tts(self, instance):
        pass


def main():
    PDFAssistantApp().run()


if __name__ == '__main__':
    main()
