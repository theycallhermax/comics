import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
import requests
import urllib.request
import os

def ExitAction(self):
    os.system("rm .comic.png")
    Gtk.main_quit()

class Comics(Gtk.ApplicationWindow):
    def __init__(self):
        super().__init__()
        self.set_border_width(10)

        def newImage(self):
            comicJSON = requests.get("https://random-xkcd-img.herokuapp.com/").json()
            comic = requests.get(comicJSON["url"]).text
            urllib.request.urlretrieve(comicJSON["url"], ".comic.png")
            comicImage.set_from_file(".comic.png")
            header.set_subtitle(comicJSON["title"])

        comicImage = Gtk.Image()
        popover = Gtk.Popover()
        newComic = Gtk.Button()
        menu = Gtk.MenuButton(popover=popover)
        header = Gtk.HeaderBar()
        scrolled_window = Gtk.ScrolledWindow()

        header.set_show_close_button(True)
        header.props.title = "Comics"
        self.set_titlebar(header)
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        icon = Gio.ThemedIcon(name="view-refresh")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        newComic.add(image)
        newComic.connect("clicked", newImage)
        header.pack_start(newComic)

        try:
            newImage(self)
        except:
            dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text="Unable to fetch a comic")
            dialog.format_secondary_text("This may be because of Internet-related errors.")
            dialog.run()
            dialog.destroy()

        self.add(image)
        self.add(comicImage)
        self.add(popover)
        self.add(menu)
        self.add(header)
        self.add(newComic)
        scrolled_window.add(image)
        self.add(scrolled_window)

window = Comics()
window.connect("destroy", ExitAction)
window.show_all()
Gtk.main()