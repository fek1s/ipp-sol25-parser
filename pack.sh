#!/bin/bash

# Nastavení názvu archivu
ARCHIVE_NAME="xfukal01.zip"

# Dočasný adresář pro archivaci
TMP_DIR="/tmp/pack_project_$$"

# Cesta k aktuálnímu adresáři (kořen projektu)
ROOT_DIR="$PWD"

# Smazat případný starý ZIP v kořenovém adresáři projektu
rm -f "$ROOT_DIR/$ARCHIVE_NAME"

# Vytvořit dočasný adresář
mkdir -p "$TMP_DIR"

# Kopírovat požadované soubory
mkdir -p "$TMP_DIR/src"
rsync -av --exclude="__pycache__" src/ "$TMP_DIR/src"

# Přidat soubory z kořenového adresáře
cp parse.py "$TMP_DIR"
if [[ -f "readme1.pdf" ]]; then
    cp "readme1.pdf" "$TMP_DIR"
fi

if [[ -f "rozsireni" ]]; then
    cp "rozsireni" "$TMP_DIR"
fi

# Přesun do dočasného adresáře a vytvoření ZIP
cd "$TMP_DIR" || { echo "❌ Chyba: Nelze přejít do $TMP_DIR"; exit 1; }
zip -r "$ROOT_DIR/$ARCHIVE_NAME" ./*

# Návrat do kořenového adresáře projektu a smazání dočasných souborů
cd "$ROOT_DIR" || { echo "❌ Chyba: Nelze přejít zpět do $ROOT_DIR"; exit 1; }
rm -rf "$TMP_DIR"

# Ověření, že ZIP existuje
if [[ -f "$ARCHIVE_NAME" ]]; then
    echo "✅ Projekt byl úspěšně zabalen do $ARCHIVE_NAME!"
else
    echo "❌ Chyba: ZIP soubor nebyl vytvořen!"
    exit 1
fi
