# -*- coding: utf-8 -*-

"""

<--  gerekli kütüphaneler  -->

customtkinter
opencv-python

"""

"""

YouTube Kanalı: https://www.youtube.com/@eminaruk
Türkiye Kuantum Topluluğu: https://x.com/i/communities/1861366749553103266

Soru, fikir ve önerileriniz için: byemin00@gmail.com

"""

import customtkinter # arayüz için, tkinter kütüphanesinin daha modern versiyonunu sunan kütüphane olan customtkinter kullanıyoruz
from tkinter import filedialog # kullanıcının resim seçebilmesi için açılacak olan pencereyi kullanmamızı sağlıyor
import cv2 # resim dosyalarını okuyabilmemize ve onlar üzerinde işlem yapabilmemizi sağlıyor
from PIL import Image, ImageTk # resim dosyalarını pencerede rahatlıkla görüntülememizi sağlıyor

customtkinter.set_appearance_mode("dark") # karanlık modda görüntülüyoruz
customtkinter.set_default_color_theme("blue")

# global değişkenlerimizi belirledik
secilen_resim = None
goruntulenecek_resim = None
sol_panel_label = None
sag_panel_label = None

panel_genislik = 400
panel_yukseklik = 500

# resim seç butonuna basıldıktan sonra çağrılacak olan fonksiyonu oluşturuyoruz
def resim_sec():
    global secilen_resim, goruntulenecek_resim, sol_panel_label, sag_panel_label

    
    # kullanıcıdan bir resim seçmesini istiyoruz
    resim_yolu = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg, *.png *.jpeg")]) # burada kabul edilen uzantılarımızı belirliyoruz
    
    if resim_yolu:

        # sol veya sağ panelden herhangi birinde mevcut bir resim varsa öncelikle panelleri temizliyoruz
        if sol_panel_label is not None:
            sol_panel_label.destroy()
        
        if sag_panel_label is not None:
            sag_panel_label.destroy()

        # seçilen resmi okuyoruz
        secilen_resim = cv2.imread(resim_yolu)

        # resmin renk uzayını BGR'den RGB'ye (Red, Green, Blue) dönüştürüyoruz
        secilen_resim_rgb = cv2.cvtColor(secilen_resim, cv2.COLOR_BGR2RGB)

        # pillow ile resmi pencerede görüntülenebilmesi için uyumlu hale getiriyoruz
        pil_resim = Image.fromarray(secilen_resim_rgb)
        
        # resmin genişlik/yükselik oranını bul
        oran = pil_resim.width / pil_resim.height
        
        # panelin genişliğine göre yüksekliği yeniden hesaplıyoruz, panelin yüksekliği de göz önünde bulundurulacak
        if pil_resim.width > pil_resim.height:
            yeni_genislik = panel_genislik
            yeni_yukseklik = int(panel_genislik / oran)
            if yeni_yukseklik > panel_yukseklik:
                yeni_yukseklik = panel_yukseklik
                yeni_genislik = int(panel_yukseklik * oran)
        else:
            yeni_yukseklik = panel_yukseklik
            yeni_genislik = int(panel_yukseklik * oran)
            if yeni_genislik > panel_genislik:
                yeni_genislik = panel_genislik
                yeni_yukseklik = int(panel_genislik / oran)

        # resmi panele sığacak şekilde yeniden boyutlandırıyoruz
        pil_resim = pil_resim.resize((panel_genislik, yeni_yukseklik))

        goruntulenecek_resim = customtkinter.CTkImage(light_image=pil_resim, size=(panel_genislik, yeni_yukseklik))

        # resmin ölçeklendirilmiş halini sol panelde görüntülüyoruz
        sol_panel_label = customtkinter.CTkLabel(sol_panel, image=goruntulenecek_resim, text="",  width=panel_genislik, height=yeni_yukseklik)
        sol_panel_label.place(x=0, y=0)

def kenar_tespit_et():

    global secilen_resim, goruntulenecek_resim, sol_panel_label, sag_panel_label # global değişkenleri dahil ediyoruz
    
    if secilen_resim is None: # herhangi bir resim seçilmediği sürece burası çalışmayacaktır
        return

    # kenar tespiti için canny algoritmasını uyguluyoruz
    kenar = cv2.Canny(secilen_resim, 100, 200, 3, L2gradient=True)

    # kenar görselinin renk uzayını RGB olarak değiştiriyoruz
    kenar_rgb = cv2.cvtColor(kenar, cv2.COLOR_GRAY2RGB)


    # resmin görüntülenmesinin rahat olması için pillow formatına dönüştürüyoruz
    pil_kenar = Image.fromarray(kenar_rgb)
    
    # resmin genişlik/yükseklik oranını buluyoruz
    oran = pil_kenar.width / pil_kenar.height
    
    # panelin genişliğine göre yüksekliği yeniden hesaplıyoruz, panelin yüksekliği de göz önünde bulundurulacak
    if pil_kenar.width > pil_kenar.height:
        yeni_genislik = panel_genislik
        yeni_yukseklik = int(panel_genislik / oran)
        if yeni_yukseklik > panel_yukseklik:
            yeni_yukseklik = panel_yukseklik
            yeni_genislik = int(panel_yukseklik * oran)
    else:
        yeni_yukseklik = panel_yukseklik
        yeni_genislik = int(panel_yukseklik * oran)
        if yeni_genislik > panel_genislik:
            yeni_genislik = panel_genislik
            yeni_yukseklik = int(panel_genislik / oran)

    # resmi panele sığacak şekilde yeniden boyutlandırıyoruz
    pil_kenar = pil_kenar.resize((yeni_genislik, yeni_yukseklik))
    
    # kenar tespit edilmiş resmi sağ panelde göstermek için CTkImage oluşturuyoruz
    goruntulenecek_resim = customtkinter.CTkImage(light_image=pil_kenar, size=(yeni_genislik, yeni_yukseklik))

    # resmin kenar tespitli halini sağ panelde görüntülüyoruz
    sag_panel_label = customtkinter.CTkLabel(sag_panel, image=goruntulenecek_resim, text="", width=yeni_genislik, height=yeni_yukseklik)
    sag_panel_label.place(x=0, y=0)



# pencere oluşturuyoruz
app = customtkinter.CTk()
app.geometry("900x650")  # pencere boyutunu genişlik-yükseklik olarak ayarlıyoruz

# resim seçme butonunu oluşturuyoruz ve sabit bir konuma yerleştiriyoruz
resim_secme_butonu = customtkinter.CTkButton(app, text="Resim Seç", command=resim_sec)
resim_secme_butonu.place(x=20, y=20) 

# kenar tespiti butonunu oluşturuyoruz ve sabit bir konuma yerleştiriyoruz
kenar_tespit_etme_butonu = customtkinter.CTkButton(app, text="Kenarları tespit et", command=kenar_tespit_et)
kenar_tespit_etme_butonu.place(x=200, y=20) 

# sol paneli oluşturuyoruz ve sabit bir konuma yerleştiriyoruz
sol_panel = customtkinter.CTkFrame(app, width=400, height=500, corner_radius=10)  # resmin orijinalinin görüntüleneceği panel
sol_panel.place(x=20, y=80)

# sağ paneli oluşturuyoruz ve sabit bir konuma yerleştiriyoruz
sag_panel = customtkinter.CTkFrame(app, width=400,height=500, corner_radius=10)  # resmin kenar tespitinden sonraki halinin görüntüleneceği panel
sag_panel.place(x=460, y=80) 

app.mainloop()



