import tkinter as tk
from tkinter import ttk
import math
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#Vektor klasse

class Vektor:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def __add__(self, other):
        return Vektor(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vektor(self.x - other.x, self.y - other.y, self.z - other.z)

    def prikk(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def kryss(self, other):
        return Vektor(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def lengde(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def scale(self, k):
        return Vektor(self.x*k, self.y*k, self.z*k)

    def projeksjon_på(self, other):
        if other.lengde() == 0:
            raise ValueError("Kan ikke projisere på nullvektor")
        faktor = self.prikk(other) / other.prikk(other)
        return other.scale(faktor)



#GUI oppsett

root = tk.Tk()
APP_VERSION = "2.0"
root.title(f"Vektorkalkulator R1 v{APP_VERSION}")
root.geometry("1100x750")
root.minsize(900, 500)

#Farger og stil
style = ttk.Style()
style.theme_use("clam")

BG = "#1e1e1e"
FRAME_BG = "#252526"
TEXT_LIGHT = "#ffffff"
BTN_BG = "#ffffff"
BTN_HOVER = "#e6e6e6"

root.configure(bg=BG)

style.configure("Dark.TFrame", background=FRAME_BG)
style.configure("Dark.TLabel", background=FRAME_BG, foreground=TEXT_LIGHT)
style.configure("Modern.TButton", background=BTN_BG, foreground="black", font=("Segoe UI", 10, "bold"))
style.map("Modern.TButton", background=[("active", BTN_HOVER)])
style.configure("Danger.TButton", background="#d32f2f", foreground="white", font=("Segoe UI", 10, "bold"))
style.map("Danger.TButton", background=[("active", "#b71c1c")])

plot_synlig = True



#Hovedramme

main_frame = ttk.Frame(root, padding=20, style="Dark.TFrame")
main_frame.pack(fill="both", expand=True)

#grid-oppsett
main_frame.columnconfigure(0, weight=1)   # venstre panel
main_frame.columnconfigure(1, weight=0)   # knappesøyle
main_frame.columnconfigure(2, weight=3)   # plot panel
main_frame.rowconfigure(0, weight=1)



#Variabler

v1x = tk.StringVar()
v1y = tk.StringVar()
v1z = tk.StringVar()
v2x = tk.StringVar()
v2y = tk.StringVar()
v2z = tk.StringVar()
k_var = tk.StringVar()
resultat = tk.StringVar(value="Resultatet vil vises her")



#Hjelpefunksjoner

def get_vektor():
    try:
        v1 = Vektor(float(v1x.get() or 0), float(v1y.get() or 0), float(v1z.get() or 0))
        v2 = Vektor(float(v2x.get() or 0), float(v2y.get() or 0), float(v2z.get() or 0))
        return v1, v2
    except ValueError:
        resultat.set("Ugyldig input – bruk tall.")
        return None


def lag_label(master, tekst, row, column=0, sticky="w"):
    lbl = ttk.Label(master, text=tekst, style="Dark.TLabel")
    lbl.grid(row=row, column=column, sticky=sticky, pady=2)
    return lbl


def lag_entry(master, var, row, column=1):
    ent = ttk.Entry(master, textvariable=var, width=10)
    ent.grid(row=row, column=column, pady=2)
    return ent


def fjern():
    v1x.set("")
    v1y.set("")
    v1z.set("")
    v2x.set("")
    v2y.set("")
    v2z.set("")
    k_var.set("")
    resultat.set("Resultatet vil vises her")

#kalkulasjonsfunksjoner

def kalk_addisjon():
    v = get_vektor()
    if v:
        resultat.set(f"Addisjon: {v[0] + v[1]}")


def kalk_prikk():
    v = get_vektor()
    if v:
        resultat.set(f"Prikkprodukt: {v[0].prikk(v[1]):.3f}")


def kalk_sub():
    v = get_vektor()
    if v:
        resultat.set(f"Subtraksjon: {v[0] - v[1]}")

"Avstand mellom spissene"
def kalk_lengde():
    v = get_vektor()
    if v:
        resultat.set(f"Avstand mellom spissene: {(v[1] - v[0]).lengde():.3f}")


def kalk_vinkel():
    v = get_vektor()
    if not v:
        return
    v1, v2 = v
    prikk = v1.prikk(v2)
    mag1 = v1.lengde()
    mag2 = v2.lengde()
    if mag1 == 0 or mag2 == 0:
        resultat.set("Kan ikke regne vinkel med nullvektor.")
        return
    cos = prikk / (mag1 * mag2)
    cos = max(-1, min(1, cos))
    resultat.set(f"Vinkel: {math.degrees(math.acos(cos)):.2f}°")


def kalk_skalar_produkt():
    v = get_vektor()
    if not v:
        return
    try:
        k = float(k_var.get())
        resultat.set(f"Skalar × Vektor 1: {v[0].scale(k)}")
    except ValueError:
        resultat.set("Ugyldig skalar.")


def er_ortogonal():
    v = get_vektor()
    if v:
        resultat.set("Ortogonale ✓" if abs(v[0].prikk(v[1])) < 1e-6 else "Ikke ortogonale")


def posisjon_ved_t():
    v = get_vektor()
    if not v:
        return
    try:
        t = float(k_var.get())
    except ValueError:
        resultat.set("Bruk skalarfeltet som t.")
        return
    p = v[0] + v[1].scale(t)
    resultat.set(f"Posisjon ved t={t}: {p}")


def vektorprojeksjon():
    v = get_vektor()
    if v:
        try:
            resultat.set(f"Projeksjon: {v[0].projeksjon_på(v[1])}")
        except ValueError:
            resultat.set("Kan ikke projisere på nullvektor.")


def parallellogram_areal():
    v = get_vektor()
    if v:
        kryss = v[0].kryss(v[1])
        areal = kryss.lengde()
        resultat.set(f"Areal parallellogram: {areal:.3f}")



#   Plot-funksjoner
def oppdater_plot():
    v = get_vektor()
    if not v:
        return

    v1 = np.array([v[0].x, v[0].y, v[0].z])
    v2 = np.array([v[1].x, v[1].y, v[1].z])

    fig.clear()
    ax = fig.add_subplot(111, projection="3d")

    ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color="b", linewidth=2, arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color="r", linewidth=2, arrow_length_ratio=0.1)

    max_val = max(np.abs(v1).max(), np.abs(v2).max()) * 1.3

    if max_val == 0:  # eller max_val < 1e-10 om du vil være ekstra paranoid
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
    else:
        ax.set_xlim(-max_val, max_val)
        ax.set_ylim(-max_val, max_val)
        ax.set_zlim(-max_val, max_val)

    ax.set_title("3D Vektorplot")
    ax.grid(True)
    canvas.draw()


def clear_plot():
    fig.clear()
    canvas.draw()


def toggle_plot():
    global plot_synlig
    if plot_synlig:
        plot_frame.grid_remove()
        plot_toggle_knapp.config(text="Vis plot")
        plot_synlig = False
    else:
        plot_frame.grid()
        plot_toggle_knapp.config(text="Skjul plot")
        plot_synlig = True




#operasjonsliste
operasjoner = {
    "Prikkprodukt": kalk_prikk,
    "Addisjon": kalk_addisjon,
    "Subtraksjon": kalk_sub,
    "Lengde": kalk_lengde,
    "Skalar × Vektor 1": kalk_skalar_produkt,
    "Ortogonal test": er_ortogonal,
    "Vinkel": kalk_vinkel,
    "Posisjon ved t": posisjon_ved_t,
    "Vektorprojeksjon": vektorprojeksjon,
    "Areal parallellogram": parallellogram_areal,
}


def kjør_valgt_operasjon():
    op = valgt_operasjon.get()
    if op in operasjoner:
        operasjoner[op]()
    oppdater_plot()

#VENSTRE PANEL
left_panel = ttk.Frame(main_frame, style="Dark.TFrame")
left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

left_panel.columnconfigure(0, weight=1)
left_panel.columnconfigure(1, weight=1)

row = 0

# Vektor 1
ttk.Label(left_panel, text="Vektor 1", style="Dark.TLabel").grid(row=row, column=0, columnspan=2, pady=(5, 5), sticky="w")
row += 1

lag_label(left_panel, "X1:", row=row, column=0, sticky="e")
lag_entry(left_panel, v1x, row=row)
row += 1

lag_label(left_panel, "Y1:", row=row, column=0, sticky="e")
lag_entry(left_panel, v1y, row=row)
row += 1

lag_label(left_panel, "Z1:", row=row, column=0, sticky="e")
lag_entry(left_panel, v1z, row=row)
row += 1

# Vektor 2
ttk.Label(left_panel, text="Vektor 2", style="Dark.TLabel").grid(row=row, column=0, columnspan=2, pady=(10, 5), sticky="w")
row += 1

lag_label(left_panel, "X2:", row=row, column=0, sticky="e")
lag_entry(left_panel, v2x, row=row)
row += 1

lag_label(left_panel, "Y2:", row=row, column=0, sticky="e")
lag_entry(left_panel, v2y, row=row)
row += 1

lag_label(left_panel, "Z2:", row=row, column=0, sticky="e")
lag_entry(left_panel, v2z, row=row)
row += 1

#Skalar
ttk.Label(left_panel, text="Skalar k:", style="Dark.TLabel").grid(row=row, column=0, sticky="e", pady=(10, 5))
lag_entry(left_panel, k_var, row=row)
row += 1

#Operasjonsmeny
ttk.Label(left_panel, text="Velg operasjon:", style="Dark.TLabel").grid(row=row, column=0, sticky="e", pady=10)
valgt_operasjon = tk.StringVar()
operasjon_meny = ttk.Combobox(left_panel, textvariable=valgt_operasjon, values=list(operasjoner.keys()), state="readonly")
operasjon_meny.grid(row=row, column=1, sticky="ew")
row += 1

ttk.Button(left_panel, text="Beregn", command=kjør_valgt_operasjon, style="Modern.TButton").grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
row += 1

#Resultatboks
result_box = ttk.LabelFrame(left_panel, text="Resultat", padding=15, style="Dark.TFrame")
result_box.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)

ttk.Label(result_box, textvariable=resultat, font=("Consolas", 12, "bold"), background="#252526", foreground="#aaffff", wraplength=400, justify="left").pack(fill="both", expand=True)
row += 1

ttk.Button(left_panel, text="Kopier resultat", command=lambda: root.clipboard_append(resultat.get()), style="Modern.TButton").grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
ttk.Button(left_panel, text="Fjern input", command=fjern, style="Danger.TButton").grid(row=row+1, column=0, columnspan=2, sticky="ew", pady=5)



#PLOT PANEL

plot_frame = ttk.Frame(main_frame, style="Dark.TFrame", relief="solid", borderwidth=1)
plot_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

fig = Figure(figsize=(7, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)




#KNAPPER I KOLONNE 1
ttk.Button(main_frame, text="Tøm plot", command=clear_plot, style="Danger.TButton").grid(row=0, column=1, sticky="ne", pady=5)


plot_toggle_knapp = ttk.Button(main_frame, text="Skjul plot", command=toggle_plot, style="Modern.TButton")
plot_toggle_knapp.grid(row=1, column=0, sticky="ne", pady=5)


root.mainloop()
