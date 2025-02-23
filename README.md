# Mira - Python Programm

Mira ist ein Python-Programm, . Diese Dokumentation erklärt, wie Sie das Programm installieren, die notwendigen Voraussetzungen erfüllen und das Programm verwenden können.

---

## Voraussetzungen

Bevor Sie Mira installieren und verwenden können, müssen Sie sicherstellen, dass die folgenden Voraussetzungen erfüllt sind:

1. **Python 3.12 oder höher**:
   - Laden Sie Python von der offiziellen Website herunter: [python.org](https://www.python.org/downloads/).
   - Stellen Sie sicher, dass Python während der Installation zu Ihrem System-PATH hinzugefügt wird.

2. **Pip (Python Package Manager)**:
   - Pip wird normalerweise automatisch mit Python installiert. Sie können überprüfen, ob Pip installiert ist, indem Sie den folgenden Befehl ausführen:
     ```bash
     pip --version
     ```

3. **Pillow (für Icon-Konvertierung)**:
   - Pillow wird benötigt, um `.png`-Dateien in `.ico`-Dateien zu konvertieren. Installieren Sie es mit:
     ```bash
     pip install pillow
     ```

4. **PyInstaller (für die Erstellung einer ausführbaren Datei)**:
   - PyInstaller wird verwendet, um das Python-Skript in eine ausführbare Datei zu packen. Installieren Sie es mit:
     ```bash
     pip install pyinstaller
     ```

---

## Installation

1. **Klonen Sie das Repository**:
   - Klonen Sie das GitHub-Repository auf Ihren lokalen Rechner:
     ```bash
     git clone [https://github.com/IhrBenutzername/IhrRepository.git](https://github.com/aoestudios57/Mira.git)
     cd IhrRepository
     ```

2. **Installieren Sie die Abhängigkeiten**:
   - Installieren Sie alle benötigten Python-Pakete:
     ```bash
     pip install -r requirements.txt
     ```

3. **Konvertieren Sie das Icon (falls nötig)**:
   - Wenn Ihr Icon im `.png`-Format vorliegt, konvertieren Sie es in das `.ico`-Format. Sie können das folgende Python-Skript verwenden:
     ```python
     from PIL import Image

     # Pfad zur PNG-Datei
     png_path = 'mira.png'
     # Pfad zur ICO-Datei
     ico_path = 'mira.ico'

     # Bild öffnen und in ICO konvertieren
     img = Image.open(png_path)
     img.save(ico_path, format='ICO')

     print(f"{png_path} wurde erfolgreich in {ico_path} konvertiert.")
     ```

---

## Verwendung

### 1. **Programm ausführen**
   - Führen Sie das Programm direkt aus, indem Sie das Python-Skript ausführen:
     ```bash
     python Mira.py
     ```

### 2. **Chat öffnen**
   - Während das Programm läuft, können Sie den Chat mit der Tastenkombination **Strg + Umschalt + C** öffnen.

### 3. **Erstellen einer ausführbaren Datei**
   - Um das Programm in eine ausführbare Datei zu packen, verwenden Sie PyInstaller:
     ```bash
     pyinstaller --onefile --icon=mira.ico Mira.py
     ```
   - Die ausführbare Datei wird im Ordner `dist` erstellt.

### 4. **Programm starten**
   - Navigieren Sie in den `dist`-Ordner und starten Sie die ausführbare Datei:
     ```bash
     cd dist
     ./Mira.exe  # Auf Windows
     ./Mira      # Auf macOS/Linux
     ```

---

## Beitrag

Falls Sie zum Projekt beitragen möchten, lesen Sie bitte die [CONTRIBUTING.md](CONTRIBUTING.md)-Datei für Details.

---

## Lizenz

Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert.

---

## Kontakt

Bei Fragen oder Problemen können Sie ein Issue im GitHub-Repository erstellen oder mich direkt kontaktieren:
- **E-Mail**: [Ihre E-Mail-Adresse]
- **GitHub**: [Ihr GitHub-Profil](https://github.com/IhrBenutzername)
