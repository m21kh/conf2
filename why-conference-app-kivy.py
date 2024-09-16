from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from plyer import notification
import random
import datetime
import arabic_reshaper
from bidi.algorithm import get_display

class ConferenceApp(App):
    def build(self):
        # Set background color of the entire window to teal
        Window.clearcolor = get_color_from_hex('#008080')

        # Register Arabic font
        LabelBase.register(name='Rubik-Italic-VariableFont_wght', fn_regular='F:\الخدمه\لماذا 4\Rubik-Italic-VariableFont_wght.ttf')

        self.tb_panel = TabbedPanel(do_default_tab=False)

        # Add tabs
        self.tb_panel.add_widget(self.create_home_tab())
        self.tb_panel.add_widget(self.create_schedule_tab())
        self.tb_panel.add_widget(self.create_verses_tab())
        self.tb_panel.add_widget(self.create_paul_life_tab())
        self.tb_panel.add_widget(self.create_hymns_tab())

        # Start verse updates and lecture notifications
        self.update_verse()
        Clock.schedule_interval(self.update_verse, 3600)  # Update every hour
        Clock.schedule_interval(self.check_lectures, 60)  # Check every minute

        return self.tb_panel

    def reshape_arabic_text(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text

    def add_background(self, layout, image_path):
        background = Image(source=image_path, allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

    def create_home_tab(self):
        home_tab = TabbedPanelItem(text='Home')
        home_content = BoxLayout(orientation='vertical')

        # Add background image of Paul the Apostle
        self.add_background(home_content, 'path/to/paul_background.jpg')

        # Add conference title
        title = Label(text='Conference "Why?"', font_size='24sp',
                      color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=100)
        home_content.add_widget(title)

        # Add short description
        description = Label(text='About Paul\'s life',
                            font_size='18sp', color=get_color_from_hex('#FFFFFF'),
                            size_hint_y=None, height=100)
        home_content.add_widget(description)

        home_tab.content = home_content
        return home_tab

    def create_schedule_tab(self):
        schedule_tab = TabbedPanelItem(text='Schedule')
        schedule_content = BoxLayout(orientation='vertical')

        # Add background for the schedule tab
        self.add_background(schedule_content, 'path/to/schedule_background.jpg')

        scroll = ScrollView()
        schedule_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        schedule_box.bind(minimum_height=schedule_box.setter('height'))

        schedule = [
            ('Day 1', [
                ('10:00', 'Lecture by Bishop Pavli', 'Main Conference Hall'),
                ('03:30', 'Trip to Alexandria', 'Gathering Point: Hotel Entrance')
            ]),
            ('Day 2', [
                ('10:00', 'Lecture by Bishop Mattaous', 'Main Conference Hall'),
                ('02:00', 'Lecture by Bishop Raphael', 'Main Conference Hall'),
                ('06:00', 'Lecture by Bishop Fam', 'Main Conference Hall')
            ]),
            ('Day 3', [
                ('08:00', 'Trip to Wadi El-Natrun Monasteries', 'Gathering Point: Hotel Entrance')
            ])
        ]

        for day, events in schedule:
            day_label = Label(text=day, font_size='20sp',
                              size_hint_y=None, height=40, color=get_color_from_hex('#0000FF'))
            schedule_box.add_widget(day_label)

            for time, event, location in events:
                event_box = BoxLayout(orientation='vertical', size_hint_y=None, height=60)
                event_label = Label(text=f'{time} - {event}', font_size='16sp')
                location_label = Label(text=location, font_size='14sp',
                                       color=get_color_from_hex('#888888'))
                event_box.add_widget(event_label)
                event_box.add_widget(location_label)
                schedule_box.add_widget(event_box)

        scroll.add_widget(schedule_box)
        schedule_content.add_widget(scroll)
        schedule_tab.content = schedule_content
        return schedule_tab

    def create_verses_tab(self):
        verses_tab = TabbedPanelItem(text='Verses')
        verses_content = BoxLayout(orientation='vertical', padding=10)

        # Add background for the verses tab
        self.add_background(verses_content, 'path/to/verses_background.jpg')

        self.verse_label = Label(text='', font_size='18sp',
                                 color=get_color_from_hex('#FFFFFF'))
        verses_content.add_widget(self.verse_label)

        refresh_button = Button(text='Refresh Verse', size_hint_y=None, height=50)
        refresh_button.bind(on_press=self.update_verse)
        verses_content.add_widget(refresh_button)
        verses_tab.content = verses_content
        return verses_tab

    def create_paul_life_tab(self):
        paul_life_tab = TabbedPanelItem(text='Paul\'s Life')
        paul_life_content = BoxLayout(orientation='vertical', padding=10)

        # Add background for Paul's life tab
        self.add_background(paul_life_content, 'path/to/paul_life_background.jpg')

        # Read Paul's life content from a text file
        try:
            with open('F:\\الخدمه\\لماذا 4\\بولس الرسول.txt', 'r', encoding='utf-8') as file:
                pauls_life_text = file.read()
        except FileNotFoundError:
            pauls_life_text = "Paul's life information not found."

        # Reshape and display Arabic text
        bidi_text = self.reshape_arabic_text(pauls_life_text)

        # Add content about Paul's life
        content = Label(text=bidi_text, font_size='18sp', color=get_color_from_hex('#FFFFFF'),
                        font_name='Rubik-Italic-VariableFont_wght', halign='right', text_size=(Window.width, None))
        paul_life_content.add_widget(content)

        paul_life_tab.content = paul_life_content
        return paul_life_tab

    def create_hymns_tab(self):
        hymns_tab = TabbedPanelItem(text='Hymns')
        hymns_content = BoxLayout(orientation='vertical', padding=10)

        # Add background for the hymns tab
        self.add_background(hymns_content, 'path/to/hymns_background.jpg')

        # Read hymns content from a text file
        try:
            with open('F:\\الخدمه\\لماذا 4\\ترانيم.txt', 'r', encoding='utf-8') as file:
                hymns_text = file.read()
        except FileNotFoundError:
            hymns_text = "Hymns information not found."

        # Reshape and display Arabic text
        bidi_text = self.reshape_arabic_text(hymns_text)

        # Add content for hymns
        hymns_label = Label(text=bidi_text, font_size='18sp', color=get_color_from_hex('#FFFFFF'),
                            font_name='Rubik-Italic-VariableFont_wght', halign='right', text_size=(Window.width, None))
        hymns_content.add_widget(hymns_label)

        hymns_tab.content = hymns_content
        return hymns_tab

    def update_verse(self, *args):
        verses = [
            "For the message of the cross is foolishness to those who are perishing, but to us who are being saved it is the power of God.",
            "انا هو الراعي الصالح.",
            # Add more verses here
        ]
        verse = random.choice(verses)
        if any('\u0600' <= c <= '\u06FF' for c in verse):  # Check if the verse contains Arabic characters
            verse = self.reshape_arabic_text(verse)
        self.verse_label.text = verse
        self.verse_label.font_name = 'ArabicFont' if any('\u0600' <= c <= '\u06FF' for c in verse) else 'Roboto'

    def check_lectures(self, *args):
        now = datetime.datetime.now()
        schedule = [
            (datetime.datetime(2024, 9, 23, 9, 45), 'Lecture by Bishop Pavly starts in 15 minutes'),
            (datetime.datetime(2024, 9, 24, 9, 45), 'Lecture by Bishop Mattaous starts in 15 minutes'),
            (datetime.datetime(2024, 9, 24, 10, 45), 'Lecture by Bishop Raphael starts in 15 minutes'),
            (datetime.datetime(2024, 9, 24, 13, 45), 'Lecture by Bishop Fam starts in 15 minutes'),
        ]

        for lecture_time, message in schedule:
            if now.date() == lecture_time.date() and now.time() >= (lecture_time - datetime.timedelta(minutes=15)).time():
                self.show_notification("Lecture Reminder", message)

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_icon='path/to/app_icon.ico',  # Path to your icon
            timeout=10,  # seconds
        )

if __name__ == '__main__':
    ConferenceApp().run()