import tkinter as tk
from tkinter import ttk
import math

#Klasse
class Vektor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #representasjon
    def __repr__(self):
        return f"({self.x:.3f}, {self.y:.3f})"

    #grunnleggende operasjoner
    def __add__(self, other):
        return Vektor(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vektor(self.x - other.x, self.y - other.y)

    # Matematikk
    def prikk(self, other):
        return self.x * other.x + self.y * other.y

    def lengde(self):
        return math.sqrt(self.x**2 + self.y**2)

    def scale(self, k):
        return Vektor(self.x * k, self.y * k)

    def projeksjon_på(self, other):
        if other.lengde() == 0:
            raise ValueError("Kan ikke projisere på nullvektor")
        faktor = self.prikk(other) / other.prikk(other)
        return other.scale(faktor)

    def parallellogram_areal(self, other):
        return abs(self.x * other.y - self.y * other.x)



#GUI oppsett
root = tk.Tk()
APP_VERSION = "1.0"
root.title(f"Vektorkalkulator R1 v{APP_VERSION}")
root.geometry("800x550")
root.minsize(700, 400)

style = ttk.Style()
style.theme_use("clam")  # kostumerer fargene mine slik jeg vil

#rød Fjerne knapp
style.configure("Danger.TButton", background="#d32f2f", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)

#farger
BG = "#1e1e1e"
FRAME_BG = "#252526"
BTN_BG = "#ffffff"
BTN_HOVER = "#e6e6e6"
TEXT_LIGHT = "#ffffff"

root.configure(bg=BG)

#frames
style.configure("Dark.TFrame", background=FRAME_BG)

#lapper
style.configure("Dark.TLabel", background=FRAME_BG, foreground=TEXT_LIGHT)

#knapper m/hvit farge
style.configure("Modern.TButton", background=BTN_BG, foreground="black", font=("Segoe UI", 10, "bold"), padding=6)
style.map("Modern.TButton", background=[("active", BTN_HOVER), ("pressed", "#cccccc")])
style.map("Danger.TButton", background=[("active", "#b71c1c"), ("pressed", "#8b0000")])

main_frame = ttk.Frame(root, padding=20, style="Dark.TFrame")
main_frame.pack(fill="both", expand=True)

#variabler
v1x = tk.StringVar()
v1y = tk.StringVar()
v2x = tk.StringVar()
v2y = tk.StringVar()
k_var = tk.StringVar()
resultat = tk.StringVar(value="Resultatet vil vises her")


#hjelpefunskjoner
def get_vektor():
    try:
        v1 = Vektor(float(v1x.get() or 0), float(v1y.get() or 0))
        v2 = Vektor(float(v2x.get() or 0), float(v2y.get() or 0))
        return v1, v2
    except ValueError:
        resultat.set("Ugyldig, bruk tall (for eksempel 3 eller -2.5)")
        return None


def lag_label(master, tekst, row, column=0, columnspan=1, pady=2, sticky="w", font=None, style=None, textvariable=None):
    """Lager og gridder en label"""
    if textvariable is not None:
        lbl = ttk.Label(master, textvariable=textvariable, font=font, style=style)
    else:
        lbl = ttk.Label(master, text=tekst, font=font, style=style)
    lbl.grid(row=row, column=column, columnspan=columnspan, pady=pady, sticky=sticky)
    return lbl


def lag_entry(master, textvariable, row, column=1, width=10, pady=2):
    """Lager og gridder en entry"""
    ent = ttk.Entry(master, textvariable=textvariable, width=width)
    ent.grid(row=row, column=column, pady=pady)
    return ent


# funskjon som adderer to vektorer
def kalk_addisjon():
    values = get_vektor()
    if not values:
        return
    v1, v2 = values
    resultat.set(f"Addisjon: {v1 + v2}")


#funskjon som regner ut prikkprodukt
def kalk_prikk():
    values = get_vektor()
    if not values:
        return
    v1, v2 = values
    prikk = v1.prikk(v2)
    resultat.set(f"Prikkprodukt: {prikk:.3f}")



#funskjon som substraherer to vektorer
def kalk_sub():
    values = get_vektor()
    if not values:
        return
    v1, v2 = values
    diff = v1 - v2
    resultat.set(f"Subtraksjon: {diff}")



#Lengde mellom to punkter(avstand)

def kalk_lengde():
    values = get_vektor()
    if not values:
        return
    v1, v2 = values

    diff = v2 - v1
    lengde = diff.lengde()
    resultat.set(f"Lengde mellom to vektorer: {lengde:.3f}")



#kalkulerer vinkler mellom to vektorer
def kalk_vinkel():
    values = get_vektor()
    if not values:
        return
    v1, v2 = values

    prikk = v1.prikk(v2)
    mag1 = math.sqrt(v1.x**2 + v1.y**2)
    mag2 = math.sqrt(v2.x**2 + v2.y**2)

    if mag1 == 0 or mag2 == 0:
        resultat.set("kan ikke kalkulere vinkel med vektor som har 0 lengde")
        return

    cos_theta = prikk / (mag1 * mag2)
    cos_theta = max(-1, min(1, cos_theta))  # klamper for å unngå feil
    theta_deg = math.degrees(math.acos(cos_theta))
    resultat.set(f"Vinkel = {theta_deg:.2f}°")



#kalkulerer produkt av k*vektor
def kalk_skalar_produkt():
    values = get_vektor()
    if not values:
        return
    v1, _ = values  # bare bruk vektor 1

    try:
        k = float(k_var.get() or "1")  # default 1
        res_x = k * v1.x
        res_y = k * v1.y
        resultat.set(f"Skalar × Vektor 1: ({res_x:.3f}, {res_y:.3f})")
    except ValueError:
        resultat.set("Ugyldig skalar, bruk tall")



#funskjon som kalkulerer om prikkprodukt er 0 - vinkelrett vektorer
def er_ortogonal():
    values = get_vektor()
    if not values:
        return
    v1, v2 = values

    prikk = v1.prikk(v2)
    if abs(prikk) < 1e-6:  # liten terskel pga avrunding
        resultat.set("Vektorene er (nesten) ortogonale ✓")
    else:
        resultat.set(f"Ikke ortogonale (prikk = {prikk:.3f})")



#funksjon for parameterfremstilling
def posisjon_ved_t():
    values = get_vektor()  # v1 = startpunkt, v2 = fart/retning
    if not values:
        return
    v1, v2 = values

    try:
        t = float(k_var.get())  # bruker skalar-feltet som t
    except ValueError:
        resultat.set("Bruk Skalar k som tid t")
        return

    pos_x = v1.x + t * v2.x
    pos_y = v1.y + t * v2.y
    resultat.set(f"Posisjon ved t={t:.2f}: ({pos_x:.2f}, {pos_y:.2f})")



#funskjon for vektorprojeksjon
def vektorprojeksjon():
    values = get_vektor()
    if not values:
        return
    v1, v2 = values

    mag2_sq = v2.x**2 + v2.y**2
    if mag2_sq == 0:
        resultat.set("Kan ikke projisere på null-vektor")
        return

    faktor = (v1.x * v2.x + v1.y * v2.y) / mag2_sq
    proj_x = faktor * v2.x
    proj_y = faktor * v2.y

    resultat.set(f"Projeksjon av vektor1 på vektor2: ({proj_x:.3f}, {proj_y:.3f})")



def parallellogram_areal():
    values = get_vektor()
    if not values:
        return
    v1, v2 = values

    areal = abs(v1.x * v2.y - v1.y * v2.x)
    resultat.set(f"Areal parallellogram: {areal:.3f}")


#en funskjon som gjør at fjern knappen legger inn tomme verdier
def fjern():
    v1x.set("")
    v1y.set("")
    v2x.set("")
    v2y.set("")
    k_var.set("")
    resultat.set("Resultatet vil vises her")


def kopier_resultat():
    root.clipboard_clear()
    root.clipboard_append(resultat.get())
    original = resultat.get()
    resultat.set(f"{original} (kopiert!)")
    root.after(3000, lambda: resultat.set(original))  # resetter feltet etter 3 sekunder


#merkelapper/labels

lag_label(main_frame, "R1 Vektorkalkulator v1.0", row=9, column=0, columnspan=2, font=("Segoe UI", 9),
          style="Dark.TLabel")

#vektor 1
lag_label(main_frame, "Vektor 1", row=0, columnspan=2, pady=(0, 5), font=("Segoe UI", 11, "bold"), style="Dark.TLabel")
lag_label(main_frame, "X1:", row=1, sticky="e")
lag_entry(main_frame, v1x, row=1)
lag_label(main_frame, "Y1", row=2, sticky="e")
lag_entry(main_frame, v1y, row=2)

#vektor 2
lag_label(main_frame, "Vektor 2", row=3, columnspan=2, pady=(15, 5),
          font=("Segoe UI", 11, "bold"), style="Dark.TLabel")
lag_label(main_frame, "X2:", row=4, sticky="e")
lag_entry(main_frame, v2x, row=4)
lag_label(main_frame, "Y2", row=5, sticky="e")
lag_entry(main_frame, v2y, row=5)

#skalar k
lag_label(main_frame, "Skalar k:", row=6, sticky="e")
lag_entry(main_frame, k_var, row=6)

#resultat
ttk.Label(main_frame, textvariable=resultat, font=("Segoe UI", 11, "bold"), style="Dark.TLabel", padding=10).grid(row=8, column=0, columnspan=2, pady=10)

#knapper
button_frame = ttk.Frame(main_frame, style="Dark.TFrame")
button_frame.grid(row=7, column=0, columnspan=2, pady=15, sticky="ew")

#konfigurer kolonner jevnt så det blir oversiktlig og ikke overlapper
for i in range(4):
    button_frame.columnconfigure(i, weight=1, uniform="buttons")

#rad 0: Grunnleggende vektoroperasjoner først
ttk.Button(button_frame, text="Prikkprodukt", command=kalk_prikk, style="Modern.TButton").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
ttk.Button(button_frame, text="Addisjon", command=kalk_addisjon, style="Modern.TButton").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
ttk.Button(button_frame, text="Subtraksjon", command=kalk_sub, style="Modern.TButton").grid(row=0, column=2, padx=5, pady=5, sticky="ew")
ttk.Button(button_frame, text="Lengde", command=kalk_lengde, style="Modern.TButton").grid(row=0, column=3, padx=5, pady=5, sticky="ew")

#rad 1: Flere beregninger middels nivå
ttk.Button(button_frame, text="Skalar × Vektor 1", command=kalk_skalar_produkt, style="Modern.TButton").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
ttk.Button(button_frame, text="Ortogonal test", command=er_ortogonal, style="Modern.TButton").grid(row=1, column=1, padx=5, pady=5,  sticky="ew")
ttk.Button(button_frame, text="Vinkel", command=kalk_vinkel, style="Modern.TButton").grid(row=1, column=2, padx=5, pady=5, sticky="ew")
ttk.Button(button_frame, text="Posisjon ved t", command=posisjon_ved_t, style="Modern.TButton").grid(row=1, column=3, padx=5, pady=5, sticky="ew")

#rad 2: Avanserte funksjoner sist
ttk.Button(button_frame, text="Vektorprojeksjon", command=vektorprojeksjon, style="Modern.TButton").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
ttk.Button(button_frame, text="Areal parallellogram", command=parallellogram_areal, style="Modern.TButton").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
#rad 3: Fjern-knapp over hele bredden
ttk.Button(button_frame, text="Fjern", command=fjern, style="Danger.TButton").grid(row=3, column=0, columnspan=4, padx=5, pady=10, sticky="ew")

#kopierer
ttk.Button(main_frame, text="Kopier resultat", command=kopier_resultat, style="Modern.TButton").grid(row=8, column=2, padx=10, sticky="e")

#loop som kjører GUI
root.mainloop()
