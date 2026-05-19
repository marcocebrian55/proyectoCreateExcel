import base64
import json
import os
import re
import io
import time
import PIL.Image
import requests

# 🔑 PEGA AQUÍ TU KEY DE GOOGLE AI STUDIO (aistudio.google.com)
GOOGLE_API_KEY = "AIzaSyBrwXUvxDVl_KMEYoIPPnNc7XJMWtZIFvk"

def extraer_datos_imagen(ruta_imagen):
    try:
        print("📸 1. Preparando imagen...")
        img = PIL.Image.open(ruta_imagen)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail((1000, 1000))

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80)
        img_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"

        prompt = """
Analiza esta captura de pantalla de un sistema de gestión de flotas (Wizard).

1. Busca la fecha en la parte superior derecha. Estará en formato como "19MAY2026". Conviértela a DD/MM/YYYY. IMPORTANTE: la fecha que debes extraer es la que aparece en la línea de encabezado superior (ej: "19MAY2026"), NO la fecha de la fila de datos de la tabla.
2. Busca el campo 'VEH CAT' en la esquina superior derecha. Extrae la letra que aparece (S, M, E, L, etc.). Si el campo está vacío o no tiene letra, usa "ALL".
3. Busca la fila que empieza por 'AVAIL' en la tabla.
4. Extrae los valores numéricos de esa fila para las columnas: TOT, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P.
   IMPORTANTE sobre los números: en este sistema mainframe los negativos se escriben con el signo DESPUÉS del número (ejemplo: "57-" significa -57, "5-" significa -5). Conviértelos correctamente a negativos en el JSON.

Responde ÚNICAMENTE con un objeto JSON con este formato exacto, sin texto adicional, sin markdown:
{"FECHA": "DD/MM/YYYY", "CATEGORIA": "Letra", "TOT": 0, "A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0, "O": 0, "P": 0}
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

        # Reintentar hasta 3 veces si hay rate limit (429)
        for intento in range(3):
            print(f"🌐 2. Enviando a Gemini API (intento {intento + 1}/3)...")
            response = requests.post(url, json=payload, timeout=60)
            datos_respuesta = response.json()

            if "error" in datos_respuesta:
                codigo = datos_respuesta['error'].get('code', 0)
                mensaje = datos_respuesta['error'].get('message', '')
                print(f"❌ Error de Google API ({codigo}): {mensaje}")

                if codigo == 429:
                    # Extraer tiempo de espera sugerido por la API
                    match_retry = re.search(r'retry in ([\d.]+)s', mensaje)
                    espera = float(match_retry.group(1)) + 2 if match_retry else 30
                    print(f"⏳ Rate limit alcanzado. Esperando {espera:.0f} segundos...")
                    time.sleep(espera)
                    continue
                return None

            break
        else:
            print("❌ Se agotaron los reintentos por rate limit.")
            return None

        texto_ia = datos_respuesta["candidates"][0]["content"]["parts"][0]["text"]
        print(f"🧠 3. Respuesta IA: {texto_ia[:300]}")

        # Eliminar markdown si Gemini responde con ```json ... ```
        texto_limpio = re.sub(r'```(?:json)?\s*|\s*```', '', texto_ia).strip()

        # Extraer el primer objeto JSON plano (sin anidación)
        match = re.search(r'\{[^{}]+\}', texto_limpio, re.DOTALL)
        if match:
            return json.loads(match.group(0))

        return json.loads(texto_limpio)

    except Exception as e:
        print(f"\n❌ ERROR EN PROCESADOR: {e}\n")
        return None
