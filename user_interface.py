import customtkinter as ctk
from PIL import Image
from database import sql_operations
from main_functions import MainPage


# class for login
class UserLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        # const structor
        self.geometry("500x500+550+190")
        self.title("Kullanıcı Girişi")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # main label
        self.main_welcome_label = ctk.CTkLabel(self, text="ÇİLEKLİ KAHVALTICI\nGİRİŞ EKRANI", text_color="black",
                                               font=ctk.CTkFont("Ink Free", size=20, weight="bold"))
        self.main_welcome_label.pack(side="top")

        # frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(pady=30, expand=True, fill="both", padx=30)

        # login image
        self.login_image = ctk.CTkImage(Image.open("images/login.png"), size=(64, 64))

        # image
        self.main_image_label = ctk.CTkLabel(self.main_frame, text="", image=self.login_image)
        self.main_image_label.pack(pady=5, side="top")

        # username label-input
        self.username_text = ctk.CTkLabel(self.main_frame, text="Kullanıcı Adı :", text_color="magenta",
                                          font=ctk.CTkFont(family="Ink Free", size=20, weight="bold"))

        self.username_text.pack(anchor="w", padx=5, pady=10)

        self.username_input = ctk.CTkEntry(self.main_frame)
        self.username_input.pack(anchor="sw", padx=5, pady=5, fill="x")

        # password label-input
        self.password_label = ctk.CTkLabel(self.main_frame, text="Şifre :", text_color="magenta",
                                          font=ctk.CTkFont(family="Ink Free", size=20, weight="bold"))

        self.password_label.pack(anchor="sw", padx=5, pady=10)

        self.password_input = ctk.CTkEntry(self.main_frame, show="*")
        self.password_input.pack(anchor="sw", padx=5, pady=5, fill="x")

        # login button
        self.login_button = ctk.CTkButton(self.main_frame, corner_radius=10, text="Giriş Yap", command=self.login)
        self.login_button.pack(anchor="sw", padx=5, pady=18, fill="x")

    # login function
    def login(self):

        # get input values
        username = self.username_input.get()
        password = self.password_input.get()

        # login process
        login = sql_operations.database_user_querry(username, password)

        # login process is achieved
        if login:
            # destroy the window
            self.destroy()

            # get main page
            main_page = MainPage()
            main_page.mainloop()
        else:
            pass

c = UserLogin()
c.mainloop()