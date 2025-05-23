import os
import re
import gdown
import zipfile

# Configurações
TXT_FILE = 'links.txt'
OUTPUT_DIR = 'downloads'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Regex para extrair IDs
RE_FILE = re.compile(r'(?:/d/|id=)([a-zA-Z0-9_-]+)')
RE_FOLDER = re.compile(r'/folders/([a-zA-Z0-9_-]+)')

def baixar_url(url):
    """Baixa arquivo ou pasta do Drive conforme o tipo de link."""
    # pasta?
    m_folder = RE_FOLDER.search(url)
    if m_folder:
        folder_id = m_folder.group(1)
        dest = os.path.join(OUTPUT_DIR, folder_id)
        print(f"Baixando pasta {folder_id} em {dest} …")
        gdown.download_folder(
            id=folder_id,
            output=dest,
            quiet=False,
            use_cookies=False
        )
        return dest

    # arquivo
    m_file = RE_FILE.search(url)
    if m_file:
        file_id = m_file.group(1)
        out = os.path.join(OUTPUT_DIR, file_id)
        print(f"Baixando arquivo {file_id} em {out} …")
        gdown.download(
            f'https://drive.google.com/uc?id={file_id}',
            out,
            quiet=False
        )
        return out

    print(f"Link inválido ou não suportado: {url}")
    return None

def extrair_zips(root_dir):
    """Encontra e extrai todo ZIP dentro de root_dir."""
    for dirpath, _, files in os.walk(root_dir):
        for fn in files:
            full = os.path.join(dirpath, fn)
            if zipfile.is_zipfile(full):
                name, _ = os.path.splitext(fn)
                dest = os.path.join(dirpath, name)
                os.makedirs(dest, exist_ok=True)
                print(f"Extraindo {full} → {dest}")
                with zipfile.ZipFile(full, 'r') as z:
                    z.extractall(dest)

if __name__ == '__main__':
    with open(TXT_FILE, 'r') as f:
        for line in f:
            link = line.strip()
            if not link:
                continue
            path = baixar_url(link)
            # se baixou algo, tente extrair zips dentro dele
            if path:
                extrair_zips(path)
