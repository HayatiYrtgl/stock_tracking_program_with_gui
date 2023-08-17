import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from database import *


# class for update, add, cost interface
class MainPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # const
        self.geometry("1024x720+300+90")
        self.title("ÇİLEKLİ MENÜ")

        # images
        self.products_image = ctk.CTkImage(Image.open("images/products_image.png"), size=(32, 32))
        self.sell_image = ctk.CTkImage(Image.open("images/sell.png"), size=(32, 32))
        self.graph_image = ctk.CTkImage(Image.open("images/graph.png"), size=(32, 32))
        self.logo = ctk.CTkImage(Image.open("images/strawberry.png"), size=(128, 128))

        # frame 1 navbar
        self.frame_navbar = ctk.CTkFrame(self, corner_radius=10, width=300)
        self.frame_navbar.pack(fill="y", padx=10, pady=10, side="left")

        # navbar label
        self.navbar_label = ctk.CTkLabel(self.frame_navbar, text_color="brown4", text="MENÜ", anchor="n",
                                         font=ctk.CTkFont(family="Ink Free", weight="bold", size=30))
        self.navbar_label.pack()

        # three Button to change frames

        # products button
        self.products_button = ctk.CTkButton(self.frame_navbar, text="ÜRÜN EKLE & ÇIKAR", image=self.products_image,
                                             anchor="w", corner_radius=10, border_spacing=10, text_color="black",
                                             hover_color="gray75", fg_color="transparent", command=self.products_command)
        self.products_button.pack(anchor="sw", padx=5, pady=20)

        # sell button
        self.sell_button = ctk.CTkButton(self.frame_navbar, text="ÜRÜN HARCANAN & KALAN", image=self.sell_image,
                                         anchor="w", corner_radius=10, border_spacing=10, text_color="black",
                                         hover_color="gray75", fg_color="transparent", command=self.sell_button_command)
        self.sell_button.pack(anchor="sw", padx=5, pady=20)

        # graph button
        self.graph_button = ctk.CTkButton(self.frame_navbar, text="ÜRÜN AYLIK GRAFİĞİ", image=self.graph_image,
                                          anchor="w", corner_radius=10, border_spacing=10, text_color="black",
                                          hover_color="gray75", fg_color="transparent",
                                          command=sql_operations.plotting_profit)
        self.graph_button.pack(anchor="sw", padx=5, pady=20)

        # logo & label
        self.logo_label_image = ctk.CTkLabel(self.frame_navbar, text="", image=self.logo)
        self.logo_label_image.pack(anchor="s", padx=5, pady=20)

        self.logo_label = ctk.CTkLabel(self.frame_navbar, text="ÇİLEKLİ \nKAHVALTICI",
                                       font=ctk.CTkFont(family="Ink Free", weight="bold", size=30),)
        self.logo_label.pack(anchor="s", padx=5, pady=20)

    """PRODUCT ADD SECTİON"""
    # button commands
    # products button
    def products_command(self):
        self.products_button.configure(fg_color="gray75", corner_radius=10)
        self.sell_button.configure(fg_color="transparent", corner_radius=10)
        self.graph_button.configure(fg_color="transparent", corner_radius=10)

        # disable
        self.sell_button.configure(state="enabled", text="ÜRÜN HARCANAN & KALAN", text_color_disabled="black")
        self.products_button.configure(state="disabled", text="ÜRÜN EKLE & ÇIKAR", text_color_disabled="black")

        # frame 2 add, update section
        self.add_update_frame = ctk.CTkFrame(self, corner_radius=10)
        self.add_update_frame.pack(fill="both", padx=10, pady=10, expand=True)

        try:
            # forget sell frame
            self.sarf_total.forget()
        except AttributeError:
            pass

        # labels
        self.main_label = ctk.CTkLabel(self.add_update_frame, text="ÜRÜN KONTROL PANELİ",
                                  font=ctk.CTkFont(family="Ink Free", weight="bold", size=30),
                                  text_color="VioletRed")
        self.main_label.pack(anchor="nw")

        # textbox for available
        self.available_products = ctk.CTkTextbox(self.add_update_frame, corner_radius=10)
        self.available_products.pack(padx=5, pady=25, fill="x")
        self.available_products.insert(ctk.INSERT, text="ELDE BULUNAN ÜRÜNLER\n")

        # get all data and insert the textbox
        sql_operations.get_all_available_products(self.available_products, ctk.END)

        # label
        self.add_label = ctk.CTkLabel(self.add_update_frame, text="ÜRÜN EKLEME PANELİ",
                                 font=ctk.CTkFont(family="Ink Free", weight="bold", size=30),
                                 text_color="VioletRed")
        self.add_label.pack(anchor="nw", padx=5, pady=5)

        # entries
        # NAME
        self.product_name_entry = ctk.CTkEntry(self.add_update_frame, placeholder_text="ÜRÜN İSMİ", corner_radius=10,
                                               border_color="green", fg_color="green2",
                                               font=ctk.CTkFont(family="Ink Free", weight="bold", size=15),
                                               placeholder_text_color="white")
        self.product_name_entry.pack(padx=5, pady=15, fill="x")

        # PİECE
        self.piece_entry = ctk.CTkEntry(self.add_update_frame, placeholder_text="ÜRÜN KİLOGRAMI/GRAMI", corner_radius=10,
                                        border_color="blue", fg_color="blue",
                                        font=ctk.CTkFont(family="Ink Free", weight="bold", size=15),
                                        placeholder_text_color="white")
        self.piece_entry.pack(padx=5, pady=15, fill="x")

        # PRİCE
        self.price_entry = ctk.CTkEntry(self.add_update_frame, placeholder_text="ÜRÜN FİYATI", corner_radius=10,
                                        border_color="red", fg_color="red",
                                        font=ctk.CTkFont(family="Ink Free", weight="bold", size=15),
                                        placeholder_text_color="white")
        self.price_entry.pack(padx=5, pady=15, fill="x")

        # add button
        self.add_button = ctk.CTkButton(self.add_update_frame, text="ÜRÜNÜ EKLE", corner_radius=10,
                                        command=self.adding_products_to_db, width=350)
        self.add_button.pack(side="left", padx=10, pady=15)

        # update button
        self.update_button = ctk.CTkButton(self.add_update_frame, text="ÜRÜNÜ GÜNCELLE", corner_radius=10,
                                           command=self.updating_products, fg_color="brown4", width=350,
                                           hover_color="brown2")
        self.update_button.pack(side="right", padx=10, pady=15)

    # adding_products
    def adding_products_to_db(self):
        # sql operations and input get
        name = self.product_name_entry.get().lower()

        try:
            piece = float(self.piece_entry.get())
            price = float(self.price_entry.get())

            # ask yes no
            ask_yes_no = messagebox.askyesno("EMİN MİSİNİZ", f"{name} adından {piece} adet "
                                                             f"{price} fiyatından eklenecektir, Emin misiniz?")
            # control
            if ask_yes_no is True:
                sql_operations.products_add(name, piece, price)
            else:
                pass

        except (TypeError, ValueError):
            messagebox.showwarning("UYARI", "FİYAT VE ADET KISMINI DOĞRU DOLDURDUĞUNUZA EMİN OLUN\n"
                                            "(not! fiyat kısmı küsüratını nokta '.' ile ayırın)")

        # update textbox
        sql_operations.get_all_available_products(self.available_products, ctk.END)

    # update products
    def updating_products(self):
        # sql operations and input get
        name = self.product_name_entry.get().lower()

        try:
            piece = float(self.piece_entry.get())
            price = float(self.price_entry.get())

            # ask yes no
            ask_yes_no = messagebox.askyesno("EMİN MİSİNİZ", f"{name} adındaki ürün {piece} adet "
                                                             f"{price} fiyatına güncellenecektir, Emin misiniz?")
            # control
            if ask_yes_no is True:
                sql_operations.products_update(name, piece, price)
            else:
                pass

        except (TypeError, ValueError):
            messagebox.showwarning("UYARI", "FİYAT VE ADET KISMINI DOĞRU DOLDURDUĞUNUZA EMİN OLUN\n"
                                            "(not! fiyat kısmı küsüratını nokta '.' ile ayırın)")

        # update textbox
        sql_operations.get_all_available_products(self.available_products, ctk.END)

    """PRODUCT SELL SECTİON"""
    # sell button
    def sell_button_command(self):

        # set bg color
        self.products_button.configure(fg_color="transparent", corner_radius=10)
        self.sell_button.configure(fg_color="gray75", corner_radius=10)
        self.graph_button.configure(fg_color="transparent", corner_radius=10)

        # disaable
        self.sell_button.configure(state="disabled", text="ÜRÜN HARCANAN & KALAN", text_color_disabled="black")
        self.products_button.configure(state="enabled", text="ÜRÜN EKLE & ÇIKAR", text_color_disabled="black")

        try:
            # forget products frame
            self.add_update_frame.forget()
        except AttributeError:
            pass

        # frame 3, sarf, total profit
        self.sarf_total = ctk.CTkFrame(self, corner_radius=10)
        self.sarf_total.pack(fill="both", padx=10, pady=10, expand=True)

        # sarf section
        self.sarf_label = ctk.CTkLabel(self.sarf_total, text="SARF ETME BÖLÜMÜ", text_color="brown4",
                                       font=ctk.CTkFont(family="Ink Free", weight="bold", size=30),)
        self.sarf_label.pack(pady=15, anchor="nw", padx=10)

        # sarf option menu and button
        self.db_products = ctk.CTkOptionMenu(self.sarf_total, values=sql_operations.get_all_available_products(),
                                             corner_radius=10, text_color="black", fg_color="LemonChiffon2",
                                             button_color="LemonChiffon3", button_hover_color="LemonChiffon")
        self.db_products.pack(fill="x", anchor="nw", padx=10, pady=20)
        self.db_products.set("HARCANACAK ÜRÜN NEDİR?")

        # entry section
        self.sarf_entry = ctk.CTkEntry(self.sarf_total,
                                       placeholder_text="KİLOGRAM(tam sayı veya ondalıklı)/GRAM(ondalıklı yazılmalı)/"
                                                        "ADET", fg_color="PaleGreen4", corner_radius=10,
                                       placeholder_text_color="black")
        self.sarf_entry.pack(fill="x", anchor="nw", padx=10, pady=10)

        # sarf et button
        self.sarf_button = ctk.CTkButton(self.sarf_total, text="ÜRÜNDEN DÜŞ", corner_radius=10,
                                         fg_color="red", text_color="white", command=self.sarf_button_command)
        self.sarf_button.pack(fill="x", padx=10, pady=10)

        # daily cost
        self.daily_cost_label = ctk.CTkLabel(self.sarf_total, text="GÜNLÜK KAZANILAN MİKTAR",
                                             text_color="brown4",
                                             font=ctk.CTkFont(family="Ink Free", weight="bold", size=30),
                                             )
        self.daily_cost_label.pack(pady=15, anchor="nw", padx=10)

        # daily profit entry
        self.daily_profit = ctk.CTkEntry(self.sarf_total, placeholder_text="Günlük kazanılan para (tl bazında)",
                                         placeholder_text_color="black", fg_color="magenta2")
        self.daily_profit.pack(fill="x", pady=15, padx=10, anchor="nw")

        # button
        self.daily_profit_button = ctk.CTkButton(self.sarf_total, text="Günlük Kâr Miktarını Hesapla",
                                                 command=self.daily_profit_command)
        self.daily_profit_button.pack(fill="x", padx=10, pady=15)

    # sarf button command
    def sarf_button_command(self):

        # get vars
        product_name = self.db_products.get()

        try:
            piece = float(self.sarf_entry.get())

            # ask yes no
            ask_yes_no = messagebox.askyesno("Emin Misiniz", f"{product_name} adındaki üründen,"
                                                             f"{piece} kg/gr/adet düşülecektir,"
                                                             f"Emin Misiniz?")

            # if question is yes commit else cancel
            if ask_yes_no is True:

                # sql operation
                sql_operations.sarf_et(product_name=product_name, pieces=piece)

                # give message
                messagebox.showinfo("BİLGİ", f"{product_name} adındaki üründen,"
                                                             f"{piece} kg/gr/adet DÜŞÜLDÜ!")

            else:
                pass

        except ValueError:
            messagebox.showwarning("UYARI", "ADET/KİLOGRAM/GRAM bölümü sadece sayısal veri içermelidir,"
                                            "Küsüratlı kısımlar '.' nokta ile ayrılmalıdır"
                                            "Kontrol EDİNİZ!")

    # daily_profit_button command
    def daily_profit_command(self):

        # get entry value
        try:
            daily_profit = int(self.daily_profit.get())

            # ask yes no
            ask_yes_no = messagebox.askyesno("EMİN MİSİNİZ",
                                             f"{date.today()} tarihinde kazanılan miktar {daily_profit}'dir"
                                             f"Veritabanına toplam kâr yazılacaktır...")
            # if control
            if ask_yes_no is True:

                # sql operations
                sql_operations.total_profit(daily_profit)

                # set disabled
                self.daily_profit_button.configure(state="disabled", text_color_disabled="black",
                                                   text="Günlük Kâr Miktarını Hesapla (İşlem zaten yapıldı)")

            else:
                pass

        except ValueError:
            messagebox.showerror("HATA", "GÜNLÜK PARA NOKTA, VİRGÜL VB. ŞEYLERLE AYRILMAMALI VE SADECE SAYI İÇERMELİDİR!")
