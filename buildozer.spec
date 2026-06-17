import os
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivy.lang import Builder
from kivy.clock import Clock

# Gemini-Inspired Premium Structural Layout
KV = '''
MDScreen:
    md_bg_color: 0.05, 0.05, 0.06, 1  # Deep cosmic dark background

    MDBoxLayout:
        orientation: 'vertical'
        padding: [16, 24, 16, 16]
        spacing: 12

        # Header Title
        MDLabel:
            text: "Second Hand Man"
            font_style: "H5"
            bold: True
            theme_text_color: "Custom"
            text_color: 0.9, 0.9, 0.95, 1
            adaptive_height: True
            halign: "center"

        # Scrollable Active Logs Display
        ScrollView:
            id: chat_scroll
            bar_width: 4
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                id: log_container
                spacing: 12
                padding: [0, 10, 0, 10]

        # Gemini-style Rounded Input Console
        MDBoxLayout:
            orientation: 'horizontal'
            adaptive_height: True
            padding: [14, 6, 14, 6]
            spacing: 10
            md_bg_color: 0.11, 0.11, 0.14, 1
            radius: [28, 28, 28, 28]

            MDIconButton:
                icon: "microphone"
                icon_size: "26sp"
                icon_color: 0.3, 0.6, 1, 1  # Electric blue accent
                pos_hint: {"center_y": .5}
                on_release: app.start_voice_listening()

            MDTextField:
                id: user_prompt
                hint_text: "Type a command..."
                mode: "rectangle"
                fill_color_normal: 0, 0, 0, 0
                line_color_normal: 0, 0, 0, 0
                line_color_focus: 0, 0, 0, 0
                text_color_focus: 0.95, 0.95, 0.95, 1
                hint_text_color_focus: 0.5, 0.5, 0.6, 1
                pos_hint: {"center_y": .5}
                on_text_validate: app.process_text_command()

            MDIconButton:
                icon: "send-circle"
                icon_size: "34sp"
                icon_color: 0.3, 0.6, 1, 1
                pos_hint: {"center_y": .5}
                on_release: app.process_text_command()
'''

class AssistantApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def add_log(self, text, is_user=False):
        """Adds stylized speech/system logs to the UI screen"""
        bubble = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            padding=[14, 10, 14, 10],
            radius=[16, 16, 16, 16] if not is_user else [16, 16, 0, 16],
            md_bg_color=(0.16, 0.16, 0.2, 1) if not is_user else (0.15, 0.35, 0.7, 1),
            pos_hint={"right": 1} if is_user else {"left": 1},
            size_hint_x=0.8
        )
        lbl = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            adaptive_height=True
        )
        bubble.add_widget(lbl)
        self.root.ids.log_container.add_widget(bubble)
        # Auto-scroll down smoothly
        Clock.schedule_once(lambda dt: setattr(self.root.ids.chat_scroll, 'scroll_y', 0), 0.1)

    def process_text_command(self):
        text = self.root.ids.user_prompt.text.strip()
        if text:
            self.add_log(text, is_user=True)
            self.root.ids.user_prompt.text = ""
            self.execute_logic(text.lower())

    def start_voice_listening(self):
        """Triggers the built-in Android speech window without crashes"""
        self.add_log("Listening via microphone...")
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                RecognizerIntent = autoclass('android.speech.RecognizerIntent')
                
                intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to your assistant")
                PythonActivity.mActivity.startActivityForResult(intent, 1001)
            except Exception as e:
                self.add_log(f"Voice Init Error: {str(e)}")
        else:
            self.add_log("Voice recognition is only active on Android devices.")

    def execute_logic(self, command):
        """Core automation parser for calls, launching, and closing applications"""
        if "call" in command:
            number = ''.join(filter(str.isdigit, command))
            if number:
                self.add_log(f"Initiating call to {number}...")
                self.native_call(number)
            else:
                self.add_log("Please specify a valid phone number.")
                
        elif "open" in command:
            app_target = command.replace("open", "").strip()
            self.add_log(f"Searching for package to open: {app_target}...")
            self.native_open_app(app_target)
            
        elif "close" in command or "exit app" in command:
            self.add_log("Closing application down...")
            Clock.schedule_once(lambda dt: MDApp.get_running_app().stop(), 1)
            
        else:
            self.add_log("Command received. Looking for local execution profile...")

    def native_call(self, number):
        if platform == 'android':
            from jnius import autoclass, cast
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            intent = Intent(Intent.ACTION_CALL)
            intent.setData(Uri.parse(f"tel:{number}"))
            PythonActivity.mActivity.startActivity(intent)

    def native_open_app(self, app_name):
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = PythonActivity.mActivity
            pm = context.getPackageManager()
            
            # Simple popular package mapper to guarantee execution matches common terms
            pkg_map = {
                "facebook": "com.facebook.katana",
                "twitter": "com.twitter.android",
                "whatsapp": "com.whatsapp",
                "youtube": "com.google.android.youtube",
                "chrome": "com.android.chrome"
            }
            
            package_id = pkg_map.get(app_name, f"com.{app_name}")
            try:
                intent = pm.getLaunchIntentForPackage(package_id)
                if intent:
                    context.startActivity(intent)
                    self.add_log(f"Successfully launched {app_name}.")
                else:
                    self.add_log(f"Could not locate app package for: {package_id}")
            except Exception as e:
                self.add_log(f"Launch failed: {str(e)}")

if __name__ == '__main__':
    AssistantApp().run()
