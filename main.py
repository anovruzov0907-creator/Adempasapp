from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
import random
import string
import os

Window.clearcolor = (0.02, 0.02, 0.02, 1)

class ModernInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.1, 0.1, 0.1, 1)
        self.foreground_color = (1, 1, 1, 1)
        self.cursor_color = (0.12, 0.53, 0.9, 1)
        self.font_size = '20sp'
        self.padding = [15, 15, 15, 15]
        self.halign = 'center'

class AdemPassApp(App):
    def build(self):
        # Fayl yolu düzəlişi (Android üçün daha təhlükəsiz)
        self.file_path = "adem_sifreler.txt"
        
        main_layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        header = Label(text="/// M-PERFORMANCE", font_size='28sp', color=(0.12, 0.53, 0.9, 1), bold=True, italic=True, size_hint_y=0.2)
        main_layout.add_widget(header)
        
        main_layout.add_widget(Label(text="PLATFORMA", font_size='12sp', color=(0.4, 0.4, 0.4, 1), bold=True))
        self.platform_in = ModernInput(hint_text="Məs: Facebook", multiline=False)
        main_layout.add_widget(self.platform_in)

        main_layout.add_widget(Label(text="ŞİFRƏ UZUNLUĞU", font_size='12sp', color=(0.4, 0.4, 0.4, 1), bold=True))
        self.length_in = ModernInput(text="16", input_filter='int', multiline=False)
        main_layout.add_widget(self.length_in)

        yarat_btn = Button(text="YARAT VƏ YADDA SAXLA", background_normal='', background_color=(0.12, 0.53, 0.9, 1), font_size='18sp', bold=True, size_hint_y=0.18)
        yarat_btn.bind(on_press=self.generate)
        main_layout.add_widget(yarat_btn)

        self.result_lbl = Label(text="---", font_size='24sp', color=(0, 1, 0.7, 1), bold=True, size_hint_y=0.15)
        main_layout.add_widget(self.result_lbl)

        btn_box = BoxLayout(spacing=10, size_hint_y=0.12)
        copy_btn = Button(text="KOPYALA", background_normal='', background_color=(0.2, 0.2, 0.2, 1), bold=True)
        copy_btn.bind(on_press=self.copy_to_clip)
        archive_btn = Button(text="ARXİV", background_normal='', background_color=(0.2, 0.2, 0.2, 1), bold=True)
        archive_btn.bind(on_press=self.show_archive)
        
        btn_box.add_widget(copy_btn)
        btn_box.add_widget(archive_btn)
        main_layout.add_widget(btn_box)

        return main_layout

    def generate(self, instance):
        plat = self.platform_in.text.strip() or "Naməlum"
        try:
            ln = int(self.length_in.text)
            chars = string.ascii_letters + string.digits + "!@#$"
            res = ''.join(random.choice(chars) for _ in range(ln))
            self.result_lbl.text = res
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(f"Platforma: {plat} | Şifrə: {res}\n")
        except:
            self.result_lbl.text = "Xəta!"

    def copy_to_clip(self, instance):
        if self.result_lbl.text != "---":
            Clipboard.copy(self.result_lbl.text)

    def show_archive(self, instance):
        data = "Arxiv boşdur."
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = f.read()
        
        content = BoxLayout(orientation='vertical', padding=15)
        scroll = ScrollView()
        archive_text = Label(text=data, size_hint_y=None, font_size='15sp', halign='left', color=(0.9, 0.9, 0.9, 1))
        archive_text.bind(texture_size=archive_text.setter('size'))
        scroll.add_widget(archive_text)
        content.add_widget(scroll)
        Popup(title='Keçmiş Şifrələr', content=content, size_hint=(0.9, 0.85)).open()

if __name__ == '__main__':
    AdemPassApp().run()
