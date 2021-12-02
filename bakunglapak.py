import tkinter as tk
import tkinter.messagebox as tkmsg

class Product(object):
    def __init__(self, nama, harga, stok):
        self.__nama = nama
        self.__harga = harga
        self.__stok = stok

    def get_nama(self):
        return self.__nama

    def get_harga(self):
        return self.__harga

    def get_stok(self):
        return self.__stok

    def set_stok(self, jumlah):
        self.__stok -= jumlah

class Buyer(object):
    def __init__(self):
        self.__daftar_beli = {}

    def add_daftar_beli(self, produk, jumlah):
        if produk in self.__daftar_beli:
          self.__daftar_beli[produk] += jumlah
        else :
          self.__daftar_beli[produk] = jumlah

    def get_daftar_beli(self):
      return self.__daftar_beli



# GUI Starts from here

# Toplevel adalah sebuah class yang mirip dengan Frame namun akan terbuka
# secara terpisah dengan Window utama (jadi membuat top-level window yang
# terpisah)
class WindowLihatBarang(tk.Toplevel):
    def __init__(self, product_dict, master = None):
        super().__init__(master)
        self.product_dict = product_dict
        self.wm_title("Daftar Barang")
        self.create_widgets()

    def create_widgets(self):
        self.lbl_judul = tk.Label(self, \
                                  text = 'Daftar Barang Yang Tersedia').grid(row = 0, column = 1)
        self.lbl_nama = tk.Label(self, \
                                 text = 'Nama Produk').grid(row = 1, column = 0)
        self.lbl_harga = tk.Label(self, \
                                  text = 'Harga').grid(row = 1, column = 1)
        self.lbl_stok = tk.Label(self, \
                                 text = 'Stok Produk').grid(row = 1, column = 2)

        i = 2
        for nama, barang in sorted(self.product_dict.items()):
            tk.Label(self, \
                     text = f"{nama}").grid(row = i, column= 0)
            tk.Label(self, \
                     text = f"{barang.get_harga()}").grid(row = i, column= 1)
            tk.Label(self, \
                     text = f"{barang.get_stok()}").grid(row = i, column= 2)
            i += 1

        self.btn_exit = tk.Button(self, text = "EXIT", \
                                  command = self.destroy).grid(row = i, column=1)


class WindowBeliBarang(tk.Toplevel):
    def __init__(self, buyer, product_dict, master = None):
        super().__init__(master)
        self.buyer = buyer
        self.product_dict = product_dict
        self.wm_title("Beli Barang")
        self.geometry("280x100")
        self.create_widgets()

    def create_widgets(self):
        self.lbl_judul = tk.Label(self, text = "Form Beli Barang").grid(row=0,column=1,columnspan=3)
        self.lbl_nama = tk.Label(self, text = "Nama Barang").grid(row=1,column=0)
        self.lbl_jumlah = tk.Label(self, text = "Jumlah").grid(row=2,column=0)
        self.var_nama = tk.StringVar()
        self.var_jumlah = tk.StringVar()
        self.entry_nama = tk.Entry(self, textvariable=self.var_nama)
        self.entry_nama.grid(row=1,column=1)
        self.entry_jumlah = tk.Entry(self, textvariable=self.var_jumlah)
        self.entry_jumlah.grid(row=2,column=1)
        self.btn_beli = tk.Button(self, text="BELI", command=self.beli_barang).grid(row=3,column=1)
        self.btn_exit = tk.Button(self, text="EXIT", command=self.destroy).grid(row=4,column=1)

    def beli_barang(self):
        nama_barang = self.var_nama.get()
        jumlah = int(self.var_jumlah.get())

        if nama_barang == "":
            self.action = tkmsg.askretrycancel(title="StringNamaKosong",parent=self,message="Nama barang tidak boleh kosong!")
            if self.action == False:
                self.destroy()            
        elif nama_barang not in self.product_dict:
            self.action = tkmsg.askretrycancel(title="BarangNotFound",parent=self,message=f"Barang dengna nama {nama_barang} tidak ditemukan dalam BakungLapak.")
            if self.action == False:
                self.destroy()
        elif self.product_dict[nama_barang].get_stok() - jumlah < 0:
            tkmsg.showwarning(title="StokEmpty",parent=self,message="Maaf, stok produk telah habis.")
        else:
            barang = self.product_dict[nama_barang]
            buyer.add_daftar_beli(barang, jumlah)
            barang.set_stok(jumlah)
            self.entry_nama.delete(0, tk.END)
            self.entry_jumlah.delete(0, tk.END)
            tkmsg.showinfo("Berhasil!", f"Berhasil membeli {nama_barang}",parent=self)


class WindowCheckOut(tk.Toplevel):
    def __init__(self, buyer, master = None):
        super().__init__(master)
        self.buyer = buyer
        self.wm_title("Daftar Barang")
        self.daftar_dibeli = buyer.get_daftar_beli()
        self.create_widgets()

    def create_widgets(self):
        self.lbl_judul = tk.Label(self, text="Keranjangku").grid(row = 0, column = 1)
        self.lbl_nama_title = tk.Label(self, text="Nama Produk").grid(row = 1, column = 0)
        self.lbl_harga_title = tk.Label(self, text="Harga Barang").grid(row = 1, column = 1)
        self.lbl_jumlah_title = tk.Label(self, text="Jumlah").grid(row = 1, column = 2)
        self.var_daftar_beli = self.buyer.get_daftar_beli()
        i = 2
        if self.var_daftar_beli == {}:
            tk.Label(self, text="Belum ada barang yang dibeli :(").grid(row = 2, column= 1)
            i += 1
        else:
            for barang, jumlah in self.var_daftar_beli.items():
                tk.Label(self, \
                        text = f"{barang.get_nama()}").grid(row = i, column= 0)
                tk.Label(self, \
                        text = f"{barang.get_harga()}").grid(row = i, column= 1)
                tk.Label(self, \
                        text = f"{jumlah}").grid(row = i, column= 2)
                i += 1
        self.btn_exit = tk.Button(self, text="EXIT", command=self.destroy).grid(row=i,column=1)


class MainWindow(tk.Frame):
    def __init__(self, buyer, product_dict, master = None):
        super().__init__(master)
        self.buyer = buyer
        self.product_dict = product_dict
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, \
                              text = 'Selamat datang di BakungLapak. Silahkan pilih Menu yang tersedia')

        self.btn_lihat_daftar_barang = tk.Button(self, \
                                                 text = "LIHAT DAFTAR BARANG", \
                                                 command = self.popup_lihat_barang)
        self.btn_beli_barang = tk.Button(self, \
                                         text = "BELI BARANG", \
                                         command = self.popup_beli_barang)
        self.btn_check_out = tk.Button(self, \
                                       text = "CHECK OUT", \
                                       command = self.popup_check_out)
        self.btn_exit = tk.Button(self, \
                                  text = "EXIT", \
                                  command = self.destroy)

        self.label.pack()
        self.btn_lihat_daftar_barang.pack()
        self.btn_beli_barang.pack()
        self.btn_check_out.pack()
        self.btn_exit.pack()

    # semua barang yand dijual
    def popup_lihat_barang(self):
        WindowLihatBarang(self.product_dict)

    # menu beli barang
    def popup_beli_barang(self):
        WindowBeliBarang(self.buyer, self.product_dict)

    # menu riwayat barang yang dibeli
    def popup_check_out(self):
        WindowCheckOut(self.buyer)

if __name__ == "__main__":

    buyer = Buyer()

    product_dict = {"Kebahagiaan" : Product("Kebahagiaan", 999999, 1),
                    "Kunci TP3 SDA" : Product("Kunci TP3 SDA", 1000000, 660)}

    m = MainWindow(buyer, product_dict)
    m.master.title("BakungLapak")
    m.master.mainloop()

# References:
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/
# https://stackoverflow.com/a/1101765