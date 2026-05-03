import requests
import urllib3

# Apagamos los avisos de seguridad de Mac para que no molesten
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 🔑 PEGA TU KEY AQUÍ
GOOGLE_API_KEY = "AIzaSyBrwXUvxDVl_KMEYoIPPnNc7XJMWtZIFvk"

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GOOGLE_API_KEY}"

print("🔍 Preguntándole a Google qué modelos tienes permitidos...")

try:
    respuesta = requests.get(url, verify=False)
    datos = respuesta.json()
    
    print("\n✅ ESTOS SON LOS MODELOS QUE PUEDES USAR PARA LEER IMÁGENES:")
    for modelo in datos.get('models', []):
        # Filtramos solo los que sirven para generar contenido
        if 'generateContent' in modelo.get('supportedGenerationMethods', []):
            print(f"👉 {modelo['name']}")
            
except Exception as e:
    print(f"❌ Error al consultar: {e}")