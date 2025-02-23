import tkinter as tk
from tkinter import scrolledtext, ttk
import json
import difflib
import keyboard
import time
import threading
import ctypes
import requests

class Chatbot:
    def __init__(self, db_file):
        self.db_file = db_file
        self.load_data()

    def load_data(self):
        """Lädt die JSON-Datenbank."""
        try:
            with open(self.db_file, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
        """Speichert die Datenbank zurück in die JSON-Datei."""
        with open(self.db_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def train(self, question, answer):
        """Fügt eine neue Frage-Antwort-Kombination hinzu."""
        self.data[question.lower()] = answer
        self.save_data()

    def get_response(self, user_input):
        """Sucht nach der besten passenden Antwort."""
        user_input = user_input.lower()
        if user_input in self.data:
            return self.data[user_input]
        
        # Unscharfe Suche nach der ähnlichsten Frage
        closest_match = difflib.get_close_matches(user_input, self.data.keys(), n=1, cutoff=0.6)
        if closest_match:
            return self.data[closest_match[0]]

        # Wenn keine Antwort gefunden wird, im Internet suchen
        return self.search_wikipedia(user_input)

    def search_wikipedia(self, query):
        """Durchsucht Wikipedia nach einer Antwort."""
        try:
            # Wikipedia-API verwenden, um den Artikel zu finden
            url = "https://de.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "utf8": 1,
                "srlimit": 1
            }
            response = requests.get(url, params=params)
            response.raise_for_status()

            # Ergebnisse extrahieren
            data = response.json()
            if data["query"]["search"]:
                title = data["query"]["search"][0]["title"]

                # Zusammenfassung des Artikels extrahieren
                params = {
                    "action": "query",
                    "format": "json",
                    "prop": "extracts",
                    "exintro": True,
                    "explaintext": True,
                    "titles": title
                }
                response = requests.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                page = next(iter(data["query"]["pages"].values()))
                if "extract" in page:
                    return page["extract"]
                else:
                    return f"Ich habe etwas gefunden: {title}. Möchtest du mehr darüber erfahren?"
            else:
                return "Ich habe keine passende Antwort gefunden."
        except Exception as e:
            return f"Fehler bei der Internetsuche: {e}"

    def import_data(self, import_file):
        """Importiert neue Frage-Antwort-Paare aus einer JSON-Datei."""
        try:
            with open(import_file, "r", encoding="utf-8") as file:
                new_data = json.load(file)
                self.data.update(new_data)
                self.save_data()
                return "Import erfolgreich!"
        except Exception as e:
            return f"Fehler beim Import: {e}"


# GUI für den Chatbot
class ChatbotGUI:
    def __init__(self, root, chatbot):
        self.root = root
        self.chatbot = chatbot
        
        # Styling der Scrollbar mit ttk
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        # Scrollbar-Stil anpassen
        self.style.configure("Vertical.TScrollbar", background="#302f2f", troughcolor="#302f2f", bordercolor="#302f2f", arrowcolor="#f0f0f0")
        self.style.map("Vertical.TScrollbar", background=[("active", "#555555")])

        # Frame für den Chat
        self.chat_frame = tk.Frame(root, bg="#302f2f", highlightbackground="#555555", highlightthickness=2)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbares Textfeld für den Chat-Verlauf
        self.chat_window = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED, height=15, bg="#302f2f", fg="#f0f0f0", font=("Arial", 12), insertbackground="#f0f0f0")
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbar des Chat-Fensters anpassen
        self.chat_window.configure(yscrollcommand=self.style.configure("Vertical.TScrollbar"))

        # Frame für das Eingabefeld und den Button
        self.input_frame = tk.Frame(root, bg="#302f2f", highlightbackground="#555555", highlightthickness=2)
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Eingabefeld für neue Nachrichten
        self.entry = tk.Entry(self.input_frame, width=40, font=("Arial", 12), bg="#ffffff", fg="#000000", highlightbackground="#555555", highlightthickness=1)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Senden-Button
        self.send_button = tk.Button(self.input_frame, text="Senden", command=self.send_message, bg="#4CAF50", fg="#ffffff", font=("Arial", 12), highlightbackground="#555555", highlightthickness=1)
        self.send_button.pack(side=tk.LEFT)

        # Enter-Taste binden
        self.entry.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        message = self.entry.get()  # Text aus dem Eingabefeld holen
        if message:
            self.chat_window.config(state=tk.NORMAL)  # Chat-Fenster bearbeitbar machen
            
            # Benutzer-Nachricht einfügen
            self.chat_window.tag_config("user", foreground="#0000ff", font=("Arial", 12, "bold"))
            self.chat_window.insert(tk.END, "Du: ", "user")
            self.chat_window.insert(tk.END, message + "\n")
            
            self.chat_window.config(state=tk.DISABLED)  # Chat-Fenster nicht mehr bearbeitbar
            self.chat_window.yview(tk.END)  # Scrollen zum neuesten Beitrag
            self.entry.delete(0, tk.END)  # Eingabefeld leeren

            # Chatbot-Antwort in einem separaten Thread mit Typing-Animation
            threading.Thread(target=self.show_typing_animation, args=(message,), daemon=True).start()

    def show_typing_animation(self, message):
        """Zeigt eine Typing-Animation an und zeigt dann die Antwort des Chatbots."""
        self.chat_window.config(state=tk.NORMAL)
        
        # Typing-Animation
        self.chat_window.insert(tk.END, "Mira: ", "bot")
        self.chat_window.insert(tk.END, "schreibt...\n")
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.yview(tk.END)

        # Künstliche Verzögerung für die Typing-Animation
        time.sleep(1)

        # Antwort des Chatbots holen
        response = self.chatbot.get_response(message)

        # Typing-Animation entfernen
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.delete("end-2l", "end-1c")  # Entfernt die "schreibt..."-Nachricht

        # Antwort des Chatbots Zeichen für Zeichen anzeigen
        self.chat_window.insert(tk.END, "Mira: ", "bot")
        for char in response:
            self.chat_window.insert(tk.END, char)
            self.chat_window.yview(tk.END)
            self.chat_window.update()
            time.sleep(0.05)  # Verzögerung zwischen den Zeichen

        self.chat_window.insert(tk.END, "\n")
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.yview(tk.END)


def get_taskbar_height():
    """Ermittelt die Höhe der Windows-Taskleiste."""
    try:
        # Verwende ctypes, um die Taskleisten-Höhe zu ermitteln
        user32 = ctypes.windll.user32
        SPI_GETWORKAREA = 0x0030
        rect = ctypes.wintypes.RECT()
        user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
        screen_height = user32.GetSystemMetrics(1)  # Gesamte Bildschirmhöhe
        work_area_height = rect.bottom - rect.top  # Höhe des Arbeitsbereichs (ohne Taskleiste)
        taskbar_height = screen_height - work_area_height  # Höhe der Taskleiste
        return taskbar_height
    except:
        # Fallback: Geschätzte Höhe der Taskleiste (40 Pixel)
        return 40


def start_chat():
    root = tk.Tk()
    root.title("Mira")
    root.geometry("400x500")

    # Bildschirmgröße in Pixeln
    screen_width = root.winfo_screenwidth()  # Beispiel: 1920 Pixel
    screen_height = root.winfo_screenheight()  # Beispiel: 1080 Pixel

    # Fenstergröße in Pixeln
    window_width = 550  # Breite des Fensters
    window_height = 600  # Höhe des Fensters

    # Höhe der Taskleiste in Pixeln
    taskbar_height = get_taskbar_height()  # Beispiel: 40 Pixel

    # Zusätzlicher Abstand nach oben (in Pixeln)
    offset_y = 100  # Beispiel: 100 Pixel höher

    # Position des Fensters in Pixeln
    x_position = screen_width - window_width  # Beispiel: 1920 - 400 = 1520
    y_position = screen_height - window_height - taskbar_height - offset_y  # Beispiel: 1080 - 500 - 40 - 100 = 440

    # Fensterposition setzen
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Hintergrundfarbe des Fensters
    root.configure(bg="#302f2f")

    # Chatbot-Instanz erstellen
    bot = Chatbot("database.json")

    # GUI für den Chatbot
    gui = ChatbotGUI(root, bot)

    # Hauptloop starten
    root.mainloop()

# Tastenkombination, um den Chat zu starten
keyboard.add_hotkey('ctrl+shift+c', start_chat)

# Warte darauf, dass der Benutzer die Tastenkombination drückt
keyboard.wait('esc')