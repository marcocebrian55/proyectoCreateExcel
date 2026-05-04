import base64
import json
import subprocess
import tempfile
import os
import PIL.Image
import io
import re

# 🔑 PEGA AQUÍ TU KEY DE GOOGLE
GOOGLE_API_KEY = "AIzaSyBrwXUvxDVl_KMEYoIPPnNc7XJMWtZIFvk"

def extraer_datos_imagen(ruta_imagen):
    try:
        print("📸 1. Preparando imagen (Modo Super-Bypass)...")
        img = PIL.Image.open(ruta_imagen)
        
        # Convertimos a RGB si es necesario (quitar transparencias)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # Redimensionamos para que no sea un archivo gigante
        img.thumbnail((1000, 1000))
        
        # Guardamos en memoria como JPEG
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80)
        img_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

        print("🛠️ 2. Creando paquete de datos...")
        # Usamos gemini-1.5-flash que es el más estable para cuentas gratuitas
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
        
        prompt = """
    Analiza esta captura de pantalla de un sistema de gestión de flotas (Wizard).
    
    1. Busca la fecha en la parte superior derecha (ejemplo: 03MAY2026) y devuélvela en formato DD/MM/YYYY.
    2. Busca en la esquina superior derecha el campo 'VEH CAT' y extrae la letra que aparece (ejemplo: S, M, E, L).
    3. Busca la fila que empieza por 'AVAIL'.
    4. Extrae los valores numéricos para las columnas: TOT, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P.

    Responde ÚNICAMENTE con un objeto JSON con este formato exacto:
    {
        "FECHA": "DD/MM/YYYY",
        "CATEGORIA": "Letra",
        "TOT": 0, "A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0, "O": 0, "P": 0
    }
    """

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
                ]
            }],
            "generationConfig": {"temperature": 0}
        }

        # Guardamos el JSON en un archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump(payload, temp_file)
            temp_file_path = temp_file.name

        print("🌐 3. Usando el sistema nativo del Mac (cURL) para enviar...")
        curl_command = [
            "curl", "-s", "-X", "POST",
            "-H", "Content-Type: application/json",
            "-d", f"@{temp_file_path}", url
        ]

        result = subprocess.run(curl_command, capture_output=True, text=True)
        os.remove(temp_file_path)

        # Validamos respuesta
        respuesta_cruda = result.stdout.strip()
        if not respuesta_cruda:
            print("❌ Google no respondió nada.")
            return None

        datos_respuesta = json.loads(respuesta_cruda)
        
        if "error" in datos_respuesta:
            print(f"❌ Error de Google: {datos_respuesta['error']}")
            return None

        texto_ia = datos_respuesta["candidates"][0]["content"]["parts"][0]["text"]
        print("🧠 4. Respuesta de la IA recibida.")
        
        # Limpiamos posibles textos extra de la IA
        match = re.search(r'\[.*\]|\{.*\}', texto_ia, re.DOTALL)
        if match:
            texto_ia = match.group(0)
            
        return json.loads(texto_ia)

    except Exception as e:
        print(f"\n❌ ERROR EN PROCESADOR: {e}\n")
        return None