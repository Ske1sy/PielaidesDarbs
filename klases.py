import sqlite3
import requests
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()
fernet_key = os.getenv("FERNET_KEY")
cipher = Fernet(fernet_key)

class Lietotajs:
    def __init__(self, vards, uzvards):
        self.vards = vards
        self.uzvards = uzvards

    def saglabasana(self):
        conn = sqlite3.connect('lietotajs.db')
        cursor = conn.cursor()

        # Šifrē vārdu un uzvārdu pirms meklēšanas/saglabāšanas
        encrypted_vards = cipher.encrypt(self.vards.encode('utf-8'))
        encrypted_uzvards = cipher.encrypt(self.uzvards.encode('utf-8'))

        cursor.execute("SELECT id FROM lietotajs WHERE vards = ? AND uzvards = ?", (encrypted_vards, encrypted_uzvards))
        rezultats = cursor.fetchone()

        if rezultats:
            lietotaja_id = rezultats[0]
        else:
            cursor.execute("INSERT INTO lietotajs (vards, uzvards) VALUES (?, ?)", (encrypted_vards, encrypted_uzvards))
            conn.commit()
            lietotaja_id = cursor.lastrowid

        conn.close()
        return lietotaja_id

class GramatasMekletajs(Lietotajs):
    def __init__(self, vards, uzvards):
        super().__init__(vards, uzvards)
        self.lietotaja_id = self.saglabasana()

    def gramatas_meklesana(self, title):
        saite = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
        pieprasijums = requests.get(saite)
        dati = pieprasijums.json()
        try:
            item = dati['items'][0]['volumeInfo']
            nosaukums = item.get('title', title)
            autors = item.get('authors', ['Nezināms'])[0]
            self.saglabat_meklejumu(nosaukums, autors)
            return nosaukums, autors
        except Exception:
            return None, None

    def saglabat_meklejumu(self, nosaukums, autors):
        conn = sqlite3.connect('lietotajs.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meklejumi (lietotaja_id, nosaukums, autors) VALUES (?, ?, ?)", (self.lietotaja_id, nosaukums, autors))
        conn.commit()
        conn.close()