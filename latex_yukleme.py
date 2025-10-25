import os
import shutil
import subprocess
import json
from tkinter import Tk, filedialog, simpledialog, messagebox
from datetime import datetime

# Repodaki hedef dizinler
REPO_PATH = os.path.abspath(os.path.dirname(__file__))
TEX_DIR = os.path.join(REPO_PATH, 'assets', 'tex')
PDF_DIR = os.path.join(REPO_PATH, 'assets', 'pdf')
SAMPLES_PATH = os.path.join(REPO_PATH, 'data', 'samples.json')


# Tkinter ile dosya ve bilgi giriş arayüzü
import tkinter as tk
from tkinter import filedialog, messagebox

class LatexForm:
    def __init__(self, master):
        self.master = master
        master.title('LaTeX ve PDF Yükleme')
        master.geometry('400x420')

        self.tex_path = ''
        self.pdf_path = ''

        # Dosya seçimi
        tk.Label(master, text='TeX Dosyası:').pack(pady=(10,0))
        self.tex_btn = tk.Button(master, text='TeX Dosyası Seç', command=self.select_tex)
        self.tex_btn.pack()
        self.tex_label = tk.Label(master, text='Henüz seçilmedi', fg='gray')
        self.tex_label.pack()

        tk.Label(master, text='PDF Dosyası:').pack(pady=(10,0))
        self.pdf_btn = tk.Button(master, text='PDF Dosyası Seç', command=self.select_pdf)
        self.pdf_btn.pack()
        self.pdf_label = tk.Label(master, text='Henüz seçilmedi', fg='gray')
        self.pdf_label.pack()

        # Metadata alanları
        self.name_entry = self.create_entry('Başlık:')
        self.desc_entry = self.create_entry('Açıklama:')
        self.cat_entry = self.create_entry('Kategori (LaTeX/TiKz):')
        self.tags_entry = self.create_entry('Etiketler (virgülle ayır):')
        self.date_entry = self.create_entry('Tarih (YYYY-MM-DD, boş bırakılırsa bugün):')

        self.save_btn = tk.Button(master, text='Kaydet', command=self.save)
        self.save_btn.pack(pady=15)

    def create_entry(self, label):
        tk.Label(self.master, text=label).pack(pady=(10,0))
        entry = tk.Entry(self.master, width=40)
        entry.pack()
        return entry

    def select_tex(self):
        path = filedialog.askopenfilename(filetypes=[('TeX files', '*.tex')])
        if path:
            self.tex_path = path
            self.tex_label.config(text=os.path.basename(path), fg='black')
        else:
            self.tex_label.config(text='Henüz seçilmedi', fg='gray')

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
        if path:
            self.pdf_path = path
            self.pdf_label.config(text=os.path.basename(path), fg='black')
        else:
            self.pdf_label.config(text='Henüz seçilmedi', fg='gray')

    def save(self):
        if not self.tex_path or not self.pdf_path:
            messagebox.showerror('Hata', 'TeX ve PDF dosyası seçilmelidir.')
            return
        name = self.name_entry.get()
        description = self.desc_entry.get()
        category = self.cat_entry.get()
        tags_str = self.tags_entry.get()
        tags = [t.strip() for t in tags_str.split(',')] if tags_str else []
        createdAt = self.date_entry.get() or datetime.now().strftime('%Y-%m-%d')

        tex_dest = os.path.join(TEX_DIR, os.path.basename(self.tex_path))
        pdf_dest = os.path.join(PDF_DIR, os.path.basename(self.pdf_path))
        try:
            shutil.copy2(self.tex_path, tex_dest)
            shutil.copy2(self.pdf_path, pdf_dest)
        except Exception as e:
            messagebox.showerror('Hata', f'Dosya kopyalama hatası: {e}')
            return

        slug = os.path.splitext(os.path.basename(self.tex_path))[0].replace(' ', '-').lower()
        try:
            with open(SAMPLES_PATH, 'r', encoding='utf-8') as f:
                samples = json.load(f)
        except Exception:
            samples = []
        new_entry = {
            "slug": slug,
            "name": name,
            "category": category,
            "tags": tags,
            "description": description,
            "texPath": f"assets/tex/{os.path.basename(self.tex_path)}",
            "pdfPath": f"assets/pdf/{os.path.basename(self.pdf_path)}",
            "createdAt": createdAt
        }
        samples.append(new_entry)
        with open(SAMPLES_PATH, 'w', encoding='utf-8') as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
        messagebox.showinfo('Başarılı', 'samples.json güncellendi.')

        # Git işlemleri
        try:
            subprocess.run(['git', 'add', tex_dest, pdf_dest, SAMPLES_PATH], cwd=REPO_PATH)
            commit_message = f"Add {os.path.basename(self.tex_path)} and {os.path.basename(self.pdf_path)}"
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=REPO_PATH)
            subprocess.run(['git', 'push'], cwd=REPO_PATH)
            messagebox.showinfo('Başarılı', 'Dosyalar ve kayıt eklendi, commit ve push işlemi tamamlandı.')
        except Exception as e:
            messagebox.showerror('Git Hatası', f'Git işlemi başarısız: {e}')

        self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = LatexForm(root)
    root.mainloop()
