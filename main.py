import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime

DATA_FILE = "tasks.csv"
fieldnames = [
    "ID", "Judul", "Deskripsi", "Proyek", "Tanggal Dibuat", "Batas Waktu",
    "Status", "Catatan", "Lampiran"
]
tasks = []

def load_tasks():
    tasks.clear()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append(row)

def save_tasks():
    with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)

def generate_task_id():
    bulan_ini = datetime.now().strftime("%Y%m")
    existing_ids = [task['ID'] for task in tasks if task['ID'].startswith(f"TUG{bulan_ini}")]
    numbers = [int(id.split("-")[1]) for id in existing_ids if "-" in id]
    next_number = max(numbers, default=0) + 1
    return f"TUG{bulan_ini}-{next_number:03d}"

def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    for task in tasks:
        tree.insert("", "end", values=(
            task['ID'], task['Judul'], task['Proyek'],
            task['Tanggal Dibuat'], task['Batas Waktu'], task['Status']
        ))

def tambah_tugas():
    def simpan():
        task = {
            "ID": generate_task_id(),
            "Judul": entry_judul.get(),
            "Deskripsi": text_deskripsi.get("1.0", "end").strip(),
            "Proyek": entry_proyek.get(),
            "Tanggal Dibuat": datetime.now().strftime("%d-%m-%Y"),
            "Batas Waktu": entry_batas.get(),
            "Status": "Belum",
            "Catatan": text_catatan.get("1.0", "end").strip(),
            "Lampiran": path_lampiran.get()
        }
        tasks.append(task)
        save_tasks()
        refresh_tree()
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Tambah Tugas")

    tk.Label(top, text="Judul:").grid(row=0, column=0, sticky="w")
    entry_judul = tk.Entry(top, width=40)
    entry_judul.grid(row=0, column=1)

    tk.Label(top, text="Deskripsi:").grid(row=1, column=0, sticky="nw")
    text_deskripsi = tk.Text(top, width=30, height=3)
    text_deskripsi.grid(row=1, column=1)

    tk.Label(top, text="Proyek/Kategori:").grid(row=2, column=0, sticky="w")
    entry_proyek = tk.Entry(top, width=30)
    entry_proyek.grid(row=2, column=1)

    tk.Label(top, text="Batas Waktu (DD-MM-YYYY):").grid(row=3, column=0, sticky="w")
    entry_batas = tk.Entry(top, width=30)
    entry_batas.insert(0, datetime.now().strftime("%d-%m-%Y"))
    entry_batas.grid(row=3, column=1)

    tk.Label(top, text="Catatan:").grid(row=4, column=0, sticky="nw")
    text_catatan = tk.Text(top, width=30, height=3)
    text_catatan.grid(row=4, column=1)

    tk.Label(top, text="Lampiran:").grid(row=5, column=0, sticky="w")
    path_lampiran = tk.StringVar()
    tk.Entry(top, textvariable=path_lampiran, width=25).grid(row=5, column=1, sticky="w")
    tk.Button(top, text="Pilih File", command=lambda: path_lampiran.set(filedialog.askopenfilename())).grid(row=5, column=1, sticky="e")

    tk.Button(top, text="Simpan", command=simpan).grid(row=6, column=1, pady=10)

def ubah_tugas():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Pilih Tugas", "Silakan pilih tugas untuk diubah.")
        return
    selected_id = tree.item(selected)['values'][0]
    task = next((t for t in tasks if t['ID'] == selected_id), None)
    if not task:
        return

    def simpan_ubah():
        task['Judul'] = entry_judul.get()
        task['Deskripsi'] = text_deskripsi.get("1.0", "end").strip()
        task['Proyek'] = entry_proyek.get()
        task['Batas Waktu'] = entry_batas.get()
        task['Status'] = var_status.get()
        task['Catatan'] = text_catatan.get("1.0", "end").strip()
        task['Lampiran'] = path_lampiran.get()
        save_tasks()
        refresh_tree()
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Ubah Tugas")

    tk.Label(top, text="Judul:").grid(row=0, column=0)
    entry_judul = tk.Entry(top, width=40)
    entry_judul.insert(0, task['Judul'])
    entry_judul.grid(row=0, column=1)

    tk.Label(top, text="Deskripsi:").grid(row=1, column=0)
    text_deskripsi = tk.Text(top, width=30, height=3)
    text_deskripsi.insert("1.0", task['Deskripsi'])
    text_deskripsi.grid(row=1, column=1)

    tk.Label(top, text="Proyek:").grid(row=2, column=0)
    entry_proyek = tk.Entry(top, width=30)
    entry_proyek.insert(0, task['Proyek'])
    entry_proyek.grid(row=2, column=1)

    tk.Label(top, text="Batas Waktu:").grid(row=3, column=0)
    entry_batas = tk.Entry(top, width=30)
    entry_batas.insert(0, task['Batas Waktu'])
    entry_batas.grid(row=3, column=1)

    tk.Label(top, text="Status:").grid(row=4, column=0)
    var_status = tk.StringVar(value=task['Status'])
    tk.OptionMenu(top, var_status, "Belum", "Selesai").grid(row=4, column=1, sticky="w")

    tk.Label(top, text="Catatan:").grid(row=5, column=0)
    text_catatan = tk.Text(top, width=30, height=3)
    text_catatan.insert("1.0", task['Catatan'])
    text_catatan.grid(row=5, column=1)

    tk.Label(top, text="Lampiran:").grid(row=6, column=0)
    path_lampiran = tk.StringVar(value=task['Lampiran'])
    tk.Entry(top, textvariable=path_lampiran, width=25).grid(row=6, column=1, sticky="w")
    tk.Button(top, text="Pilih File", command=lambda: path_lampiran.set(filedialog.askopenfilename())).grid(row=6, column=1, sticky="e")

    tk.Button(top, text="Simpan Perubahan", command=simpan_ubah).grid(row=7, column=1, pady=10)

def hapus_tugas():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Pilih Tugas", "Silakan pilih tugas untuk dihapus.")
        return
    selected_id = tree.item(selected)['values'][0]
    for i, task in enumerate(tasks):
        if task['ID'] == selected_id:
            tasks.pop(i)
            break
    save_tasks()
    refresh_tree()

root = tk.Tk()
root.title("Manajemen Tugas - Versi Sederhana")

tree = ttk.Treeview(root, columns=("ID", "Judul", "Proyek", "Tanggal Dibuat", "Batas Waktu", "Status"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.pack(pady=10, fill="x")

frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)

tk.Button(frame_btn, text="Tambah", command=tambah_tugas).pack(side="left", padx=5)
tk.Button(frame_btn, text="Ubah", command=ubah_tugas).pack(side="left", padx=5)
tk.Button(frame_btn, text="Hapus", command=hapus_tugas).pack(side="left", padx=5)

load_tasks()
refresh_tree()

root.mainloop()