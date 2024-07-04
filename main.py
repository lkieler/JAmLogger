from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSlideTransition
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.list import MDList
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from datetime import datetime
import tzlocal
import json
import os

KV = '''
MDScreenManager: 
    md_bg_color: self.theme_cls.backgroundColor
    HomeScreen:
    LogEntryScreen:

<LogEntryItem>:
    orientation: 'vertical'
    size_hint_y: None
    height: '60dp'
    spacing: '10dp'
    padding: '10dp'

    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1  # Gray color for the line
        Line:
            points: self.x + dp(10), self.y, self.x + self.width - dp(10), self.y  # Draws line at the top of the item
    MDBoxLayout:
        orientation: 'horizontal'
        MDBoxLayout:
            orientation: 'vertical'
            spacing: '10dp'
            MDLabel:
                id: primary_text
                text: "Primary Text"
                bold: True
            MDLabel:
                id: secondary_text
                text: "Secondary Text"
            MDLabel:
                id: tertiary_text
                text: "Tertiary Text"
        MDIconButton:
            icon: "pencil"
            id: edit_entry
                

<HomeScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            size_hint_y: None
            height: '48dp'
            orientation: 'horizontal'
            MDIconButton:
                icon: "information"
                on_release: root.show_info_dialog()
            MDLabel:
                text: "JAmLogger"
                halign: "center"
            MDIconButton:
                icon: "plus"
                on_release: app.switch_to_screen('log_entry', direction="left")
        MDBoxLayout:
            orientation: 'vertical'
            spacing: '10dp'
            MDScrollView:
                size_hint_y: 1, None
                height: root.height - dp(48)  # Fill remaining space minus top bar height
                MDList:
                    id: log_list
                    height: self.minimum_height  # Allow list to expand vertically as needed
            


<LogEntryScreen>:
    name: 'log_entry'
    MDBoxLayout:
        pos_hint: {'top': 1}
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'
        
        MDBoxLayout:
            size_hint_y: None
            height: '40dp'
            orientation: 'horizontal'
            MDButton:
                style: "elevated"
                on_release:
                    app.switch_to_screen('home', direction="right")
                    root.clear_entries()
                MDButtonIcon:
                    icon: 'home'
                MDButtonText:
                    text: "Back to Home"
            Widget: # This will take up the remaining space
            MDButton:
                style: "elevated"
                pos_hint: {"top": 1}
                on_release: root.save_log_entry()
                MDIconButton:
                    icon: 'content-save'
                MDButtonText:
                    text: "Save"

        MDBoxLayout:
            size_hint_y: None
            height: '60dp'
            orientation: 'horizontal'
            spacing: '10dp'
            MDTextField:
                id: time
                mode: "outlined"
                MDTextFieldHintText:
                    text: "Time"
            MDButton:
                on_release: root.update_time()
                pos_hint: {"center_y": 0.5}
                MDButtonText:
                    text: "Now"
                
        MDBoxLayout:
            size_hint_y: None
            height: '60dp'
            orientation: 'horizontal'
            spacing: '10dp'
            MDTextField:
                id: callsign
                mode: "outlined"
                size_hint_x: 0.5
                MDTextFieldHintText:
                    text: "Callsign"
            MDTextField:
                id: qrg
                mode: "outlined"
                size_hint_x: 0.5
                MDTextFieldHintText:
                    text: "QRG"

        MDBoxLayout:
            size_hint_y: None
            height: '60dp'
            orientation: 'horizontal'
            spacing: '10dp'
            MDTextField:
                id: mode
                mode: "outlined"
                size_hint_x: 0.5
                MDTextFieldHintText:
                    text: "Mode"
            MDBoxLayout:
                size_hint_y: None
                size_hint_x: 0.5
                orientation: 'horizontal'
                spacing: '10dp'
                MDTextField:
                    id: srst
                    mode: "outlined"
                    size_hint_x: 0.5
                    MDTextFieldHintText:
                        text: "SRST"
                MDTextField:
                    id: trst
                    mode: "outlined"
                    size_hint_x: 0.5
                    MDTextFieldHintText:
                        text: "TRST"

        MDBoxLayout:
            size_hint_y: None
            height: '60dp'
            orientation: 'horizontal'
            spacing: '10dp'
            MDTextField:
                id: qth
                mode: 'outlined'
                MDTextFieldHintText:
                    text: "QTH"
            MDTextField:
                id: state
                mode: 'outlined'
                MDTextFieldHintText:
                    text: "State"
            MDTextField:
                id: country
                mode: 'outlined'
                MDTextFieldHintText:
                    text: "Country"

        MDTextField:
            id: notes
            mode: 'outlined'
            multiline: True
            height: '60dp'
            max_height: '180dp'
            MDTextFieldHintText:
                text: "Notes"

        Widget:

'''

class LogEntryItem(BoxLayout):
    def __init__(self, primary_text, secondary_text, tertiary_text, **kwargs):
        super().__init__(**kwargs)
        self.ids.primary_text.text = primary_text
        self.ids.secondary_text.text = secondary_text
        self.ids.tertiary_text.text = tertiary_text

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.info_dialog = None

    def on_enter(self, *args):
        Clock.schedule_once(self.load_log_entries, 0.1)

    def load_log_entries(self, *args):
        self.ids.log_list.clear_widgets()  # Clear existing widgets before loading new ones
        if os.path.exists("log_data.json"):
            with open("log_data.json", "r") as f:
                log_data = json.load(f)
                for entry_key, entry_value in log_data.items():
                    if entry_key != "counter":
                        new_item = LogEntryItem(
                            primary_text=f"Entry {entry_key}:   Time: {entry_value['time']}",
                            secondary_text=f"Call: {entry_value['callsign']}    QRG: {entry_value['qrg']}   Mode: {entry_value['mode']}", 
                            tertiary_text=f"QTH: {entry_value['qth']}   State: {entry_value['state']}  Country: {entry_value['country']}"
                        )
                        new_item.ids.edit_entry.bind(on_release=lambda x, ek=entry_key, ev=entry_value: self.edit_entry(ek, ev))
                        self.ids.log_list.add_widget(new_item)

    def show_info_dialog(self, *args):
        if not self.info_dialog:
            self.info_dialog = MDDialog(
                MDDialogIcon(
                    icon="information",
                ),
                MDDialogHeadlineText(
                    text="Hello Headline",
                ),
                MDDialogSupportingText(
                    text="Hello MDDialogSupportingText World!",
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(
                        MDButtonText(
                            text="Close",
                        ),
                        style="elevated",
                        on_release=lambda x: self.info_dialog.dismiss()
                    )
                )
            )
        self.info_dialog.open()

    def add_log_entry(self, entry_key, entry_value):
        self.ids.log_list.add_widget(
            OneLineListItem(text=f"Entry {entry_key}: {entry_value['callsign']}")
        )

    def edit_entry(self, entry_key, entry_value):
        log_entry_screen = self.manager.get_screen('log_entry')
        log_entry_screen.load_entry(entry_value)

class LogEntryScreen(Screen):
    log_file = "log_data.json"
    def save_log_entry(self):
        # Load existing log data or initialize a new log if file doesn't exist
        if os.path.exists(LogEntryScreen.log_file):
            with open(LogEntryScreen.log_file, "r") as f:
                log_data = json.load(f)
        else:
            log_data = {"counter": 0}

        counter = log_data["counter"]
        new_entry_key = f"{counter}"
        new_entry = {
            "time": self.ids.time.text,
            "callsign": self.ids.callsign.text,
            "qrg": self.ids.qrg.text,
            "mode": self.ids.mode.text,
            "srst": self.ids.srst.text,
            "trst": self.ids.trst.text,
            "qth": self.ids.qth.text,
            "state": self.ids.state.text,
            "country": self.ids.country.text,
            "notes": self.ids.notes.text,
        }
        
        log_data[new_entry_key] = new_entry
        log_data["counter"] = counter + 1
        
        with open(LogEntryScreen.log_file, "w") as f:
            json.dump(log_data, f, indent=4)

        #self.add_log_entry(new_entry_key, new_entry)

        # Reset text fields after saving
        for key in new_entry.keys():
            if key in self.ids:
                self.ids[key].text = ""

    def read_json(*args):
        if os.path.exists(LogEntryScreen.log_file):
            with open(LogEntryScreen.log_file, 'r') as file:
                print(json.load(file))
                return json.load(file)
        return {"counter": 0}

    def update_time(self):
        now = datetime.now(tzlocal.get_localzone())
        current_time = datetime.now().strftime('%d.%m.%Y %H:%M:00 ') + now.tzname()
        self.ids.time.text = current_time

    def load_entry(self, entry_value):
        self.ids.time.text = entry_value['time']
        self.ids.callsign.text = entry_value['callsign']
        self.ids.qrg.text = entry_value['qrg']
        self.ids.mode.text = entry_value['mode']
        self.ids.srst.text = entry_value['srst']
        self.ids.trst.text = entry_value['trst']
        self.ids.qth.text = entry_value['qth']
        self.ids.state.text = entry_value['state']
        self.ids.country.text = entry_value['country']
        self.ids.notes.text = entry_value['notes']

    def clear_entries(self):
        self.ids.time.text = ""
        self.ids.callsign.text = ""
        self.ids.qrg.text = ""
        self.ids.mode.text = ""
        self.ids.srst.text = ""
        self.ids.trst.text = ""
        self.ids.qth.text = ""
        self.ids.state.text = ""
        self.ids.country.text = ""
        self.ids.notes.text = ""


class JAmLoggerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.root = Builder.load_string(KV)
        self.root.transition = MDSlideTransition(direction="up")  # Set the initial direction to up
        return self.root

    def switch_to_screen(self, screen_name, direction="up", duration=0.05, transition_type="slide"):
        transition_classes = {
            "slide": MDSlideTransition,
            #"fade": MDFadeTransition,
            #"no": MDNoTransition,
            #"swap": MDSwapTransition,
            #"card": MDCardTransition,
        }

        transition_class = transition_classes.get(transition_type, MDSlideTransition)
        self.root.transition = transition_class(direction=direction, duration=duration)
        self.root.current = screen_name


if __name__ == '__main__':
    JAmLoggerApp().run()

