import os
import json
import subprocess

REPO_PATH = os.path.abspath(os.path.dirname(__file__))
TEX_DIR = os.path.join(REPO_PATH, 'assets', 'tex')
PDF_DIR = os.path.join(REPO_PATH, 'assets', 'pdf')
SAMPLES_PATH = os.path.join(REPO_PATH, 'data', 'samples.json')

# Kullanıcıdan dosya adlarını al
tex_name = input('Silinecek TeX dosyasının adı (ör: Coulomb.tex): ').strip()
pdf_name = input('Silinecek PDF dosyasının adı (ör: Coulomb.pdf): ').strip()

tex_path = os.path.join(TEX_DIR, tex_name)
pdf_path = os.path.join(PDF_DIR, pdf_name)

# Dosyaları sil
for path in [tex_path, pdf_path]:
    if os.path.exists(path):
        os.remove(path)
        print(f'Silindi: {path}')
    else:
        print(f'Bulunamadı (zaten silinmiş olabilir): {path}')

# samples.json'dan kaydı sil
with open(SAMPLES_PATH, 'r', encoding='utf-8') as f:
    samples = json.load(f)

new_samples = [s for s in samples if not (s.get('texPath') == f'assets/tex/{tex_name}' and s.get('pdfPath') == f'assets/pdf/{pdf_name}')]

if len(samples) == len(new_samples):
    print('samples.json içinde eşleşen kayıt bulunamadı.')
else:
    with open(SAMPLES_PATH, 'w', encoding='utf-8') as f:
        json.dump(new_samples, f, ensure_ascii=False, indent=2)
    print('samples.json güncellendi ve kayıt silindi.')

# Git işlemleri
subprocess.run(['git', 'add', SAMPLES_PATH], cwd=REPO_PATH)
subprocess.run(['git', 'rm', '-f', tex_path], cwd=REPO_PATH)
subprocess.run(['git', 'rm', '-f', pdf_path], cwd=REPO_PATH)
commit_message = f"Remove {tex_name} and {pdf_name}"
subprocess.run(['git', 'commit', '-m', commit_message], cwd=REPO_PATH)
# Otomatik olarak uzak repo ile senkronize et
subprocess.run(['git', 'pull', '--rebase'], cwd=REPO_PATH)
subprocess.run(['git', 'push'], cwd=REPO_PATH)
print('Silme, commit, pull --rebase ve push işlemi tamamlandı.')
