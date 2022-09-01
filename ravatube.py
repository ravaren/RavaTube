import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image

from pytube import YouTube
from pytube.exceptions import RegexMatchError

import os
import time


kivy.require("1.9.0")

# app_version = "RavaTube 0.1"


class RavaTube(App):
    # whole app
    def build(self):
        # create window object and set its params
        self.window = BoxLayout()
        self.window.orientation = "vertical"
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        # logo widget
        self.window.add_widget(Image(source="icon.png"))
        # app name/title widget
        self.window.add_widget(Label(text="RavaTube",
                                     color= "#9d0a2b",
                                     font_size=52
                              ))
        # text label with disclaimer
        self.window.add_widget(Label(text="WARNING: Downloading or converting videos from YouTube service is against the terms of service,\nand sometimes against the law. Use it on your own responsibility!",
                                     size_hint_y=0.6,
                                     font_size=10))
        # message box
        self.message = Label(text="",
                             size_hint=(1, 0.5)
                             )
        self.window.add_widget(self.message)
        # text input box
        self.link = TextInput(multiline=False,
                              text="Paste YT link here...",
                              # padding_y=(5),
                              size_hint=(1, 0.3),
                              )
        self.window.add_widget(self.link)
        # button that triggers converting process
        self.button = Button(text="Save as MP3!",
                             size_hint=(1, 0.5),
                             bold=True,
                             background_color="#0b8c49",
                             )
        self.button.bind(on_press=self.convert)
        self.window.add_widget(self.button)
        
        return self.window

    def convert(self, event):
        # function that creates mp3 file from yt video
        self.button.text = "Working..."
        # try if the link is good
        try:
            # create yt object and then scrap only audio from it
            yt = YouTube(self.link.text)
            video = yt.streams.filter(only_audio=True).first()
            out_audio = video.download()
            # create new file on device
            base, ext = os.path.splitext(out_audio)
            new_file = base + ".mp3"
            os.rename(out_audio, new_file)
            # set text boxes in app
            self.message.text = f"\"{yt.title}\" saved to your device!"
            self.button.text = "Done!"
        except RegexMatchError:
            # while link is wrong show this text in button box
            self.button.text = "Invalid link. Try again."


if __name__ == "__main__":
    RavaTube().run()
