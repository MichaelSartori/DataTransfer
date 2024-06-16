import cv2
import base64
from pymongo import MongoClient
from datetime import datetime
import time

def capture_image():
    # Öffne die Kamera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Kamera konnte nicht geöffnet werden")

    # Ein Bild aufnehmen
    ret, frame = cap.read()
    if not ret:
        cap.release()  # Kamera freigeben
        raise Exception("Bild konnte nicht aufgenommen werden")

    # Kamera freigeben
    cap.release()
    return frame

def convert_image_to_html(image):
    # Konvertiere das Bild in das JPEG-Format im Speicher
    _, buffer = cv2.imencode('.jpg', image)
    # Kodieren das Bild in Base64
    encoded_string = base64.b64encode(buffer).decode('utf-8')

    # Erzeuge ein HTML-Image-Tag
    html_image = f'<img src="data:image/jpeg;base64,{encoded_string}" alt="image">'
    return html_image

def save_to_mongodb(html_content):
    # Verbindet sich mit dem MongoDB-Client (Standardport 27017)
    client = MongoClient('192.168.0.100', 27017)
    try:
        # Wählt die Datenbank und die Sammlung aus
        db = client['Weatherstation']
        collection = db['images']
        
        # Aktuellen Zeitstempel erzeugen
        timestamp = datetime.now().isoformat()

        # Das Dokument, das in die Sammlung eingefügt wird
        document = {
            'image_html': html_content,
            'timestamp': timestamp
        }
        # Fügt das Dokument in die Sammlung ein
        collection.insert_one(document)
        print(f"{timestamp} - Daten erfolgreich in MongoDB gespeichert.")
    finally:
        client.close()

if __name__ == "__main__":
    while True:
        try:
            image = capture_image()  # Bild aufnehmen
            html_image = convert_image_to_html(image) # Bild in HTML umwandeln
            save_to_mongodb(html_image)  # HTML in MongoDB speichern
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
        time.sleep(1800)  # 30 Minuten warten
