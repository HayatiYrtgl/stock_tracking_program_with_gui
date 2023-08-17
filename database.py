import sqlite3 as sql
from sqlite3 import DataError, OperationalError
from tkinter import messagebox
from datetime import date
import matplotlib.pyplot as plt
import customtkinter as ctk
from random import choice


# creating class for crete to dbs
class SqlCreator:

    # const super
    def __init__(self, *args, **kwargs):
        super().__init__()

        # base constructor struct for creating databases
        self.db_database = sql.connect("dbs/database.db")

        # cursors
        self.db_cursor = self.db_database.cursor()

        # create tables
        self.database_creators()
        
    # function of creating database
    def database_creators(self):

        # user database
        command_users = """CREATE TABLE IF NOT EXISTS users(id int PRIMARY KEY, username string, password string)"""

        self.db_cursor.execute(command_users)

        self.db_database.commit()

        # products and sales
        command_products = """CREATE TABLE IF NOT EXISTS products(id int PRIMARY KEY, 
        product_name string, piece float, price float, day date)"""

        self.db_cursor.execute(command_products)

        self.db_database.commit()

        # cost table
        command_cost = """CREATE TABLE IF NOT EXISTS cost(id int PRIMARY KEY, cost float DEFAULT 0, day date)"""

        self.db_cursor.execute(command_cost)

        self.db_database.commit()

        # sales table
        command_sales = """CREATE TABLE IF NOT EXISTS sales(id int PRIMARY KEY, 
        sold_total float, cost_total float, total_profit float, day date)"""

        self.db_cursor.execute(command_sales)

        self.db_database.commit()

    # function 2 login
    def database_user_querry(self, username, password):

        # entered name and password
        # it will ask for registiration

        # try to get user information 
        # if user not exists in the table
        # throw a except message
        try:
            command = """SELECT password from users WHERE username=?"""

            self.db_cursor.execute(command, (username,))

            # fetch one
            querred_password = str(self.db_cursor.fetchone()[0])

            # match passwords
            if password == querred_password:

                messagebox.showinfo("BİLGİ", f"GİRİŞ YAPILDI {username}")

                return True
            
            elif password != querred_password:
                messagebox.showerror("HATA", f"ŞİFRE DOĞRU DEĞİL {username}")

                return False
            
        except TypeError:

            # show warning
            messagebox.showwarning("UYARI", f"KAYITLI DEĞİLSİN {username}")

            return False

    # function 3 add products
    def products_add(self, product_name, pieces, prices, days=date.today()):

        # if product name already exists
        qeurred_product = self.db_cursor.execute("SELECT * FROM products WHERE product_name=?", (product_name,))

        qeurred_product = qeurred_product.fetchone()

        if qeurred_product is not None:

            messagebox.showwarning("UYARI", "ZATEN HALİ HAZIRDA BULUNAN ÜRÜN ADINI GİRDİNİZ\nÜRÜN EKLENMEDİ GÜNCELLEMEYİ DENEYİNİZ!")
        
        else:
            # try except block to catch error
            try:
                # sql querry
                add_command = "INSERT INTO products(product_name, piece, price, day) VALUES (?,?,?,?)"

                self.db_cursor.execute(add_command, (product_name, pieces, prices, days))

                # commit
                self.db_database.commit()

                messagebox.showinfo("BİLGİ", f"{product_name} adındaki üründen {pieces} adet "
                                             f"{prices} fiyatından {days} tarihinde eklendi")

            except (OperationalError, DataError):

                # give message
                messagebox.showerror("HATA", "GİRİLENLER SİSTEME İŞLENEMEDİ")

    # funtion 4 update
    def products_update(self, product_name_for_querry, pieces, prices):

        try:

            # update command
            update_command = """UPDATE products SET piece=?, price=? WHERE product_name=?"""

            self.db_cursor.execute(update_command, (pieces, prices, product_name_for_querry))

            self.db_database.commit()

            messagebox.showinfo("BİLGİ", f"{product_name_for_querry} adındaki ürününün\n "
                                         f"fiyatı {prices} \n adeti {pieces} olarak güncellenmiştir")

        except:
            messagebox.showerror("HATA", "ÜRÜN GÜNCELLENEMEDİ")

    # function 5 spend resources
    # get price and commit the sales section
    def sarf_et(self, product_name, pieces, days=date.today()):
        
        # sarf sql command to get product and minus from products table
        get_products_features_command = """SELECT piece, price FROM products WHERE product_name=?"""

        # if products are avaible

        execute = self.db_cursor.execute(get_products_features_command, (product_name,))

        product_features = execute.fetchone()

        if product_features is not None:

            # assign features to variables
            product_price = product_features[1]
            product_pieces = product_features[0]

            # calculate the cost and commit the sale table
            cost = pieces * product_price

            cost_command = """INSERT INTO cost(cost, day) VALUES (?, ?)"""
            self.db_cursor.execute(cost_command, (cost, days))

            self.db_database.commit()

            # update pieces where product table is in 
            # calculate remaining value
            remaining_piece = product_pieces-pieces

            # if remaining value is less or equal to zero give message
            if remaining_piece <= 0:
                messagebox.showinfo("BİLGİ", f"{product_name} ÜRÜNÜNDEN SIFIR ADET KALMIŞTIR")

                update_command = """UPDATE products SET piece=? WHERE product_name=?"""

                # execute fun
                self.db_cursor.execute(update_command, (0, product_name))

                self.db_database.commit()
            
            else:

                update_command = """UPDATE products SET piece=? WHERE product_name=?"""

                # execute fun
                self.db_cursor.execute(update_command, (remaining_piece, product_name))

                self.db_database.commit()
        
        # else
        else:
            messagebox.showwarning("UYARI", "GİRİLEN ÜRÜN ENVANTERİNİZDE BULUNMAMAKTADIR")

        # costu güne göre gruplandırıp toplamamız lazım

    # calculate profit and daily cost
    def total_profit(self, sold_total, day=date.today()):

        try:
            # get cost
            cost_total = self.db_cursor.execute("""SELECT SUM(cost) FROM cost WHERE day=?""", (day,))

            cost_total = cost_total.fetchall()[0][0]

            profit = sold_total - cost_total

            # commit the db
            profit_command = """INSERT INTO sales(sold_total, cost_total, total_profit, day) VALUES(?,?,?,?)"""

            self.db_cursor.execute(profit_command, (sold_total, cost_total, profit, day))

            self.db_database.commit()

            messagebox.showinfo("BİLGİ", f" {day} tarihinde\n Yapılan Satış Tutarı: {sold_total}\n "
                                         f"Toplam Maliyet: {cost_total}\n VE genel kar miktarı : {profit} TL'dir")
        
        except:
            messagebox.showwarning("UYARI", "SİSTEME ERİŞİM SAĞLANAMADI")

    # get all available products
    def get_all_available_products(self, textbox=None, index=None):

        # if textbox object given
        if textbox is not None and index is not None:
            textbox.delete("1.0", "end")
            textbox.insert(ctk.INSERT, text="ELDE BULUNAN ÜRÜNLER\n")
            all_val = self.db_cursor.execute("SELECT * FROM products")
            all_val = all_val.fetchall()

            # for loop to insert
            for i in all_val:

                # name price piece
                name = i[1]
                piece = i[2]
                price = i[3]

                textbox.insert(index, text=f"\nÜrün :{name}\nAdet/kg/gr :{piece}\nFiyat :{price}TL\n"
                                           f"---------------------------------------------")

        else:
            # products_list
            products_list = []

            # sql command
            all_val = self.db_cursor.execute("SELECT * FROM products")
            all_val = all_val.fetchall()

            # for loop to insert
            for i in all_val:
                # name price piece
                products_list.append(i[1])

            # return
            return products_list

    # get plot values
    def plotting_profit(self):

        # groupby method sql
        list_of_profit_day = self.db_cursor.execute("SELECT total_profit, day FROM sales GROUP BY day")
        list_of_profit_day = list_of_profit_day.fetchmany(30)

        # profits
        profit_list = []

        # days
        days = []

        # color list
        color_list = ["m", "r", "b", "black"]

        for i in list_of_profit_day:
            # add proft to list
            profit_list.append(i[0])

            # add day to days list
            days.append(i[1])

        try:
            # plotting all values as bar plot
            plt.subplots(figsize=(6, 4))
            plt.bar(days, profit_list, label="GÜNLÜK KÂR MİKTARI", color=choice(color_list))
            plt.xlabel("TARİHLER")
            plt.ylabel("KÂR (TL)")
            plt.legend()
            plt.show()
        except:
            messagebox.showinfo("BİLGİ", "BR HATA MEYDANA GELDİ, BELKİ DE DAHA GÜNLÜK VERİ EKLENMEMİŞTİR")



try:
    # activate class
    sql_operations = SqlCreator()
    messagebox.showinfo("BİLGİ", "VERİTABANI GİRİŞİ YAPILDI")

except:
    raise


