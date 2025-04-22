import tkinter as tk
from tkinter import messagebox
from klases import GramatasMekletajs
from datu_baze import datu_bazes_izveide

def login():
    vards = vards_entry.get()
    uzvards = uzvards_entry.get()
    if not vards or not uzvards:
        messagebox.showerror("Kļūda", "Lūdzu ievadi vārdu un uzvārdu.")
        return
    root.searcher = GramatasMekletajs(vards, uzvards)
    meklesanas_poga.config(state=tk.NORMAL)
    messagebox.showinfo("Sveicināti!", f"{vards} {uzvards}, tagad vari meklēt grāmatas!")

def mekle_gramatu():
    nosaukums = gramatas_entry.get()
    if not nosaukums:
        messagebox.showwarning("Brīdinājums!", "Ievadi grāmatas nosaukumu.")
        return

    nosaukums_atrasts, autors = root.searcher.gramatas_meklesana(nosaukums)
    if nosaukums_atrasts:
        resultata_label.config(text=f"Atrasts: {nosaukums_atrasts} — {autors}")
    else:
        resultata_label.config(text="Grāmata nav atrasta.")


root = tk.Tk()
root.title("📚 Grāmatu Meklētājs")

tk.Label(root, text="Vārds:", font=("Helvetica", 20)).grid(pady=10, padx=40, row=0, column=0)
tk.Label(root, text="Uzvārds:", font=("Helvetica", 20)).grid(pady=10, padx=40,row=1, column=0)

vards_entry = tk.Entry(root, font=("Helvetica", 20))
vards_entry.grid(row=0, pady=10, padx=40, column=1)

uzvards_entry = tk.Entry(root, font=("Helvetica", 20))
uzvards_entry.grid(row=1, pady=10, padx=40, column=1)

login_button = tk.Button(root, text="Ieiet", command=login, font=("Helvetica", 20))
login_button.grid(pady=10, padx=40, columnspan=2)

tk.Label(root, text="Grāmatas nosaukums:", font=("Helvetica", 20)).grid(pady=10, padx=40, row=4, column=0)
gramatas_entry = tk.Entry(root, font=("Helvetica", 20))
gramatas_entry.grid(pady=10, padx=40, row=4, column=1)

meklesanas_poga = tk.Button(root, text="Meklēt", state=tk.DISABLED, command=mekle_gramatu, font=("Helvetica", 20))
meklesanas_poga.grid(pady=10, padx=40, columnspan=2)

resultata_label = tk.Label(root, text="", font=("Helvetica", 20))
resultata_label.grid(pady=10, padx=40, columnspan=2)


if __name__ == "__main__":
    datu_bazes_izveide()
    root.mainloop()