import os
import shutil
import subprocess
from tkinter import Tk, filedialog

# Repodaki hedef dizinler
REPO_PATH = os.path.abspath(os.path.dirname(__file__))
TEX_DIR = os.path.join(REPO_PATH, 'assets', 'tex')
PDF_DIR = os.path.join(REPO_PATH, 'assets', 'pdf')

# Tkinter ile dosya seçimi
Tk().withdraw()
print('Bir LaTeX (.tex) dosyası seçin:')
tex_file = filedialog.askopenfilename(filetypes=[('TeX files', '*.tex')])
if not tex_file:
    print('TeX dosyası seçilmedi. Çıkılıyor.')
    exit(1)

print('Bir PDF dosyası seçin:')
pdf_file = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
if not pdf_file:
    print('PDF dosyası seçilmedi. Çıkılıyor.')
    exit(1)


# Dosyaları ilgili dizinlere kopyala
tex_dest = os.path.join(TEX_DIR, os.path.basename(tex_file))
pdf_dest = os.path.join(PDF_DIR, os.path.basename(pdf_file))

try:
    shutil.copy2(tex_file, tex_dest)
    print(f'{tex_file} -> {tex_dest}')
except Exception as e:
    print(f'TeX dosyası kopyalanamadı: {e}')
    exit(1)
try:
    shutil.copy2(pdf_file, pdf_dest)
    print(f'{pdf_file} -> {pdf_dest}')
except Exception as e:
    print(f'PDF dosyası kopyalanamadı: {e}')
    exit(1)

if not os.path.exists(tex_dest):
    print(f'TeX dosyası {tex_dest} dizinde bulunamadı!')
    exit(1)
if not os.path.exists(pdf_dest):
    print(f'PDF dosyası {pdf_dest} dizinde bulunamadı!')
    exit(1)

# Kullanıcıdan metadata al
slug = os.path.splitext(os.path.basename(tex_file))[0].replace(' ', '-').lower()
name = input('Başlık: ')
description = input('Açıklama: ')
category = input('Kategori (LaTeX/TiKz): ')
tags = input('Etiketler (virgülle ayır): ').split(',')
tags = [t.strip() for t in tags if t.strip()]
createdAt = input('Tarih (YYYY-MM-DD, boş bırakılırsa bugün): ')
if not createdAt:
    from datetime import datetime
    createdAt = datetime.now().strftime('%Y-%m-%d')

# samples.json'a ekle
import json
samples_path = os.path.join(REPO_PATH, 'data', 'samples.json')
with open(samples_path, 'r', encoding='utf-8') as f:
    samples = json.load(f)
new_entry = {
    "slug": slug,
    "name": name,
    "category": category,
    "tags": tags,
    "description": description,
    "texPath": f"assets/tex/{os.path.basename(tex_file)}",
    "pdfPath": f"assets/pdf/{os.path.basename(pdf_file)}",
    "createdAt": createdAt
}
samples.append(new_entry)
with open(samples_path, 'w', encoding='utf-8') as f:
    json.dump(samples, f, ensure_ascii=False, indent=2)
print('samples.json güncellendi.')

# Git işlemleri
subprocess.run(['git', 'add', tex_dest, pdf_dest, samples_path], cwd=REPO_PATH)
commit_message = f"Add {os.path.basename(tex_file)} and {os.path.basename(pdf_file)}"
subprocess.run(['git', 'commit', '-m', commit_message], cwd=REPO_PATH)
subprocess.run(['git', 'push'], cwd=REPO_PATH)
print('Dosyalar ve kayıt eklendi, commit ve push işlemi tamamlandı.')
