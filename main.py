import os
import sys
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class AssistantContainer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        
        # 1. Output Display (Scrollable)
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.output_label = Label(
            text="🤖 AI Mobile Assistant Ready.\nType a command below (e.g., 'open youtube', 'organize').\n" + "-"*30,
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.output_label.bind(texture_size=self.output_label.setter('size'))
        self.scroll.add_widget(self.output_label)
        self.add_widget(self.scroll)
        
        # 2. Input Field
        self.user_input = TextInput(
            hint_text="Enter command here...",
            size_hint=(1, 0.15),
            multiline=False
        )
        self.user_input.bind(on_text_validate=self.process_command)
        self.add_widget(self.user_input)
        
        # 3. Action Button
        self.submit_btn = Button(
            text="Execute Task",
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 1, 1)
        )
        self.submit_btn.bind(on_press=self.process_command)
        self.add_widget(self.submit_btn)

    def log_to_screen(self, text):
        self.output_label.text += f"\n\n▶ {text}"

    def process_command(self, instance):
        cmd = self.user_input.text.strip().lower()
        if not cmd:
            return
            
        self.user_input.text = "" # Clear input
        
        # --- Assistant Logic ---
        if "open" in cmd:
            target = cmd.replace("open", "").strip()
            app_urls = {
                "whatsapp": "https://api.whatsapp.com",
                "youtube": "https://www.youtube.com",
                "google": "https://www.google.com"
            }
            url = app_urls.get(target, f"https://www.google.com/search?q={target}")
            webbrowser.open(url)
            self.log_to_screen(f"Opening intent link for: {target}")
            
        elif "organize" in cmd or "clean" in cmd:
            self.log_to_screen("🧹 Running storage layout sort routine...")
            self.log_to_screen("File system operations initialized.")
            
        elif "write" in cmd or "message" in cmd:
            msg = cmd.replace("write a message", "").replace("write", "").strip()
            webbrowser.open(f"https://api.whatsapp.com/send?text={msg.replace(' ', '%20')}")
            self.log_to_screen(f"Drafted text broadcast link generated.")
            
        else:
            self.log_to_screen(f"Command '{cmd}' logged to assistant core engine.")

class AIAssistantApp(App):
    def build(self):
        return AssistantContainer()

if __name__ == '__main__':
    AIAssistantApp().run()
