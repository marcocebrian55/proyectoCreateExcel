🧙‍♂️ Mago de Wizard - Automatización de Reportes con IA
Este proyecto es una aplicación web interna desarrollada en Python que actúa como un puente entre sistemas de gestión legacy (basados en terminal) y hojas de cálculo modernas.

El objetivo principal es eliminar el trabajo manual de "copy-paste", automatizando la extracción de datos de inventario y disponibilidad diaria mediante Inteligencia Artificial (Computer Vision).

✨ Características Principales
Extracción Inteligente: Utiliza la API de Google Gemini (IA Multimodal) para "leer" capturas de pantalla del sistema Wizard, identificando fechas, categorías de vehículos y tablas numéricas complejas (incluidos negativos en formato mainframe como "57-" = -57).

Procesamiento de Datos: Ordena cronológicamente la información, agrupa por categorías y elimina duplicados automáticamente por fecha + categoría.

Generación de Excel a Medida: Transforma los datos brutos en un archivo .xlsx con dobles cabeceras, anchos automáticos y colores de semáforo (rojo ≤0, naranja 1-15, verde ≥16).

Interfaz Sencilla: Una web minimalista donde el usuario solo tiene que subir las capturas y obtener su Excel listo en segundos.

Reintentos Automáticos: Manejo automático de errores 429 (rate limit) y 503 (servidor saturado) con espera y reintento.

🛠️ Tecnologías Utilizadas
Backend: Python, Flask
Procesamiento de Datos: Pandas
Generación de Excel: Openpyxl
Inteligencia Artificial: Google Gemini 2.5 Flash (API REST)
Procesamiento de Imágenes: Pillow (PIL)
HTTP: Requests
Frontend: HTML5, Bootstrap 5

🚀 Instalación y Despliegue (Local o Codespaces)

1. Clonar el repositorio:
git clone https://github.com/marcocebrian55/proyectoCreateExcel.git
cd proyectoCreateExcel/backend

2. Instalar las dependencias:
pip install flask pandas openpyxl pillow requests

3. Configurar la API Key:
Edita ia_processor.py línea 11 y pega tu clave de Google AI Studio (aistudio.google.com):
GOOGLE_API_KEY = "TU_KEY_AQUI"

4. Iniciar el servidor:
python app.py

5. Abrir en el navegador:
http://127.0.0.1:5000 (local) o el puerto que indique Codespaces.

Si actualizas el repo con git pull y tienes cambios locales (ej. tu API key):
git stash && git pull && git stash pop && python app.py

💻 Uso
1. Abre la web y haz clic en "Elegir archivos".
2. Selecciona una o varias capturas de pantalla del sistema Wizard.
3. Haz clic en "Generar / Actualizar Excel".
4. El archivo Reporte_Wizard.xlsx se descargará automáticamente.

Nota: con varias imágenes la IA espera 4 segundos entre cada una para respetar los límites de la API gratuita.

⚠️ Solución de Errores Frecuentes

| Error | Causa | Solución |
|---|---|---|
| `400 - API key expired` | La key de Google ha caducado | Genera una nueva en aistudio.google.com y pégala en ia_processor.py línea 11 |
| `429 - Quota exceeded` | Cuota diaria agotada o rate limit | Espera a que se resetee (~9am España) o crea una key nueva en un **proyecto nuevo** de Google AI Studio |
| `503 - High demand` | Servidores de Gemini saturados | El sistema reintenta automáticamente. Si persiste, espera unos minutos y vuelve a intentarlo |
| `404 - Model not found` | Nombre de modelo incorrecto para esa key | Las keys nuevas solo soportan modelos 2.x+. El modelo correcto es `gemini-2.5-flash` con endpoint `v1beta` |
| Excel con solo 1 fila aunque subiste varias imágenes | El prompt extraía la fecha del encabezado del sistema en lugar de la fecha de la tabla de datos, haciendo que todas las filas tuviesen la misma fecha y se deduplicasen | Ya corregido: el prompt ahora extrae la fecha del período de datos (ej: "23MAY2026 SATURDAY") |
| `git pull` falla con "would be overwritten" | Tienes cambios locales sin commitear (ej. tu API key) | Usa: `git stash && git pull && git stash pop` |
| Excel muestra datos de una sesión anterior | El archivo reporte_wizard.xlsx persiste entre sesiones y se acumula | Bórralo antes de una prueba limpia: `rm uploads/reporte_wizard.xlsx` |
