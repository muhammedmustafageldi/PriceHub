import tkinter
from tkinter import *
from PIL import Image, ImageTk
from service import PriceService
import webbrowser
import customtkinter
from CTkMessagebox import CTkMessagebox

root = tkinter.Tk()


def create_window():
    root.title('PriceHub')
    root.iconbitmap('pictures/logo.ico')
    root.geometry('1000x590')
    root.resizable(False, False)
    create_top_frame()
    create_main_layout()


def create_top_frame():
    banner_image = create_image_with_path(path='pictures/banner.png')

    top_label = Label(root, image=banner_image)

    top_label.image = banner_image
    top_label.pack()


def create_main_layout():
    # Search box ->
    search_bg = create_image_with_path("pictures/search_bg.png")

    search_label = Label(root, image=search_bg)
    search_label.image = search_bg
    search_label.pack(padx=5, pady=5)

    # Search Entry
    search_entry = Entry(search_label, justify='center', width=20, font=('poppins', 25, 'bold'), bg='#FFA51E',
                         border=0, fg='white')
    search_entry.place(x=50, y=20)

    search_icon = create_image_with_path('pictures/search_icon.png')

    search_button = Button(root, image=search_icon, borderwidth=0, cursor='hand2', bg='#FFA51E',
                           activebackground='#FFA51E',
                           command=lambda: search_and_get_data(search_entry.get(), frameTrendyol, frameAmazon,
                                                               frameHepsiburada))
    search_button.image = search_icon
    search_button.place(x=660, y=267)

    divider = Canvas(root, height=1, bg="#FFA51E")
    divider.pack(fill="x", pady=0)

    # Results Area ->
    results_frame = Frame(root)
    results_frame.pack(expand=True, fill="both")

    for i in range(3):
        results_frame.columnconfigure(i, weight=1)

    frameTrendyol = Frame(results_frame, bg='#FFF8EC', height=600)
    frameAmazon = Frame(results_frame, bg='#FFDA9A', height=600)
    frameHepsiburada = Frame(results_frame, bg='#FFFAF0', height=600)

    frameTrendyol.grid(row=0, column=0, sticky="nsew", pady=5)
    frameAmazon.grid(row=0, column=1, sticky="nsew", pady=5)
    frameHepsiburada.grid(row=0, column=2, sticky="nsew", pady=5)

    label1 = Label(frameTrendyol, text='TRENDYOL', font=('poppins', 15, 'bold'), bg='#FFF8EC')
    label1.pack(pady=10)

    label2 = Label(frameAmazon, text='AMAZON', font=('poppins', 15, 'bold'), bg='#FFDA9A')
    label2.pack(pady=10)

    label3 = Label(frameHepsiburada, text='HEPSİBURADA', font=('poppins', 15, 'bold'), bg='#FFFAF0')
    label3.pack(pady=10)


def create_image_with_path(path):
    opened_image = Image.open(path)
    return ImageTk.PhotoImage(opened_image)


def search_and_get_data(search_value, trendyol_frame, amazon_frame, hepsiburada_frame):
    service = None
    try:
        msg = CTkMessagebox(master=root, title='Chrome Başlatılıyor',
                            message="Fiyat bilgileri için chrome çalıştırılsın mı?"
                                    "\nLütfen programın çalıştırılması durumunda pencereyi kapatmayın.",
                            button_color='#FFA51E', button_hover_color='#FFC46C', button_text_color='#ffffff',
                            option_1='Tamam', option_2='İptal', font=('poppins', 12, 'bold'),
                            icon='pictures/loading.png')
        if msg.get() == 'Tamam':
            # Start selenium service
            service = PriceService()
            # Get data from service
            product_dict = service.get_prices(search_value=search_value)

            product_trendyol = product_dict['product_trendyol']
            product_amazon = product_dict['product_amazon']
            product_hepsiburada = product_dict['product_hepsiburada']

            # Put Trendyol data in place
            divider = Canvas(trendyol_frame, height=1, bg="#FFA51E")
            divider.pack(fill="x", pady=0)

            product_name_trendyol = Label(trendyol_frame, text=shorten_or_add(product_trendyol.name),
                                          font=('poppins', 12, 'bold'),
                                          bg='#FFFAF0')
            product_name_trendyol.pack(padx=10, pady=10)

            product_seller_trendyol = Label(trendyol_frame, text=shorten_or_add(product_trendyol.store),
                                            font=('poppins', 12, 'bold'),
                                            bg='#FFFAF0')
            product_seller_trendyol.pack(padx=10, pady=10)

            product_price_trendyol = Label(trendyol_frame, text=product_trendyol.price, font=('poppins', 12, 'bold'),
                                           bg='#FFFAF0')
            product_price_trendyol.pack(padx=10, pady=10)

            trendyol_go_to_link = customtkinter.CTkButton(trendyol_frame, text='Ürüne git', fg_color='#FFA51E',
                                                          font=('poppins', 15, 'bold'),
                                                          text_color='#ffffff',
                                                          hover_color='#ffeccc',
                                                          command=lambda: go_to_link(product_trendyol.product_url))
            trendyol_go_to_link.pack(expand=True, fill='both', padx=10)

            # Put Amazon data in place
            divider = Canvas(amazon_frame, height=1, bg="#FFA51E")
            divider.pack(fill="x", pady=0)

            product_name_amazon = Label(amazon_frame, text=shorten_or_add(product_amazon.name),
                                        font=('poppins', 12, 'bold'),
                                        bg='#FFDA9A')
            product_name_amazon.pack(padx=10, pady=10)

            product_seller_amazon = Label(amazon_frame, text=shorten_or_add(product_amazon.store),
                                          font=('poppins', 12, 'bold'),
                                          bg='#FFDA9A')
            product_seller_amazon.pack(padx=10, pady=10)

            product_price_amazon = Label(amazon_frame, text=product_amazon.price, font=('poppins', 12, 'bold'),
                                         bg='#FFDA9A')
            product_price_amazon.pack(padx=10, pady=10)

            amazon_go_to_link = customtkinter.CTkButton(amazon_frame, text='Ürüne git', fg_color='#FFA51E',
                                                        font=('poppins', 15, 'bold'),
                                                        text_color='#ffffff',
                                                        hover_color='#ffeccc',
                                                        command=lambda: go_to_link(product_amazon.product_url))
            amazon_go_to_link.pack(expand=True, fill='both', padx=10)

            # Put Hepsiburada data in place
            divider = Canvas(hepsiburada_frame, height=1, bg="#FFA51E")
            divider.pack(fill="x", pady=0)

            product_name_hepsiburada = Label(hepsiburada_frame, text=shorten_or_add(product_hepsiburada.name),
                                             font=('poppins', 12, 'bold'),
                                             bg='#FFFAF0')
            product_name_hepsiburada.pack(padx=10, pady=10)

            product_seller_hepsiburada = Label(hepsiburada_frame, text=shorten_or_add(product_hepsiburada.store),
                                               font=('poppins', 12, 'bold'),
                                               bg='#FFFAF0')
            product_seller_hepsiburada.pack(padx=10, pady=10)

            product_price_hepsiburada = Label(hepsiburada_frame, text=product_hepsiburada.price,
                                              font=('poppins', 12, 'bold'),
                                              bg='#FFFAF0')
            product_price_hepsiburada.pack(padx=10, pady=10)

            hepsiburada_go_to_link = customtkinter.CTkButton(hepsiburada_frame, text='Ürüne git', fg_color='#FFA51E',
                                                             font=('poppins', 15, 'bold'),
                                                             text_color='#ffffff',
                                                             hover_color='#ffeccc',
                                                             command=lambda: go_to_link(
                                                                 product_hepsiburada.product_url))
            hepsiburada_go_to_link.pack(expand=True, fill='both', padx=10)
    except:
        CTkMessagebox(master=root, title='Hata oluştu',
                      message='Bot maalesef bir hata ile karşılaştı :(\nLütfen yeniden arama yapmayı deneyin.',
                      button_color='#FFA51E', button_hover_color='#FFC46C', button_text_color='#ffffff',
                      option_1='Tamam', width=300, height=100, font=('poppins', 12, 'bold'), icon='pictures/error.png')
        if service:
            service.quit_driver()


def go_to_link(url):
    webbrowser.open(url=url)


def shorten_or_add(string):
    if len(string) > 25:
        return string[:25] + '...'
    else:
        return string


create_window()
root.mainloop()
