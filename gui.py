from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class Gui:
    def __init__(self, root):
        self.root = root
        root.title('PriceHub')
        root.iconbitmap('pictures/logo.ico')
        root.geometry('1000x600')
        root.resizable(False, False)

        self.create_top_frame()
        self.create_main_layout()

    def create_top_frame(self):
        banner_image = self.create_image_with_path(path='pictures/banner.png')

        top_label = Label(self.root, image=banner_image)

        top_label.image = banner_image
        top_label.pack()

    def create_main_layout(self):
        # Search box ->
        search_bg = self.create_image_with_path("pictures/search_bg.png")

        search_label = Label(self.root, image=search_bg)
        search_label.image = search_bg
        search_label.pack(padx=5, pady=5)

        # Search Entry
        search_entry = Entry(search_label, justify='center', width=20, font=('poppins', 25, 'bold'), bg='#FFA51E',
                             border=0, fg='white')
        search_entry.place(x=50, y=20)

        search_icon = self.create_image_with_path('pictures/search_icon.png')

        search_button = Button(self.root, image=search_icon, borderwidth=0, cursor='hand2', bg='#FFA51E',
                               activebackground='#FFA51E')
        search_button.image = search_icon
        search_button.place(x=660, y=267)

        divider = Canvas(self.root, height=1, bg="#FFA51E")
        divider.pack(fill="x", pady=0)

        # Results Area ->
        trendyol_card = self.create_card_view(x=130, y=390)
        amazon_card = self.create_card_view(x=420, y=390)
        hepsiburada_card = self.create_card_view(x=710, y=390)

        label1 = Label(trendyol_card, text='Merhabalar', bg='#FFA51E')
        label1.place(x=50, y=30)

    def create_card_view(self, x, y):
        # Create card label
        card_bg = self.create_image_with_path('pictures/card_bg.png')
        card_label = Label(self.root, height=170, width=160, image=card_bg)
        card_label.image = card_bg
        card_label.place(x=x, y=y)
        return card_label

    def create_image_with_path(self, path):
        opened_image = Image.open(path)
        return ImageTk.PhotoImage(opened_image)
