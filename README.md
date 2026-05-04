🧙‍♂️ Mago de Wizard - Automatización de Reportes con IA
Este proyecto es una aplicación web interna desarrollada en Python que actúa como un puente entre sistemas de gestión legacy (basados en terminal) y hojas de cálculo modernas.

El objetivo principal es eliminar el trabajo manual de "copy-paste", automatizando la extracción de datos de inventario y disponibilidad diaria mediante Inteligencia Artificial (Computer Vision).

✨ Características Principales
Extracción Inteligente: Utiliza la API de Google Gemini (IA Multimodal) para "leer" capturas de pantalla del sistema antiguo, identificando fechas, categorías de vehículos y tablas numéricas complejas.

Procesamiento de Datos: Ordena cronológicamente la información, agrupa por categorías y elimina duplicados automáticamente.

Generación de Excel a Medida: Transforma los datos brutos en un archivo .xlsx con un diseño preestablecido (dobles cabeceras, anchos automáticos y reglas de formato condicional con colores de semáforo).

Interfaz Sencilla: Una web minimalista donde el usuario solo tiene que subir las capturas y obtener su Excel listo en cuestión de segundos.

🛠️ Tecnologías Utilizadas
Backend: Python, Flask

Procesamiento de Datos: Pandas

Generación de Excel: Openpyxl

Inteligencia Artificial: Google Generative AI (gemini-1.5-flash)

Procesamiento de Imágenes: Pillow (PIL)

Frontend: HTML5, CSS3

🚀 Instalación y Despliegue (Local o Codespaces)
Sigue estos pasos para arrancar el proyecto en tu entorno local o en GitHub Codespaces:

1. Clonar el repositorio:
git clone https://github.com/marcocebrian55/proyectoCreateExcel.git
cd proyectoCreateExcel/backend

2. Crear y activar un entorno virtual (Recomendado):

Windows: python -m venv venv y luego venv\Scripts\activate

Mac/Linux/Codespaces: python3 -m venv venv y luego source venv/bin/activate

3. Instalar las dependencias:
pip install flask pandas openpyxl google-generativeai Pillow

4. Configurar la API Key:
Asegúrate de configurar tu clave de API de Google Gemini en el archivo ia_processor.py o mediante variables de entorno para que el modelo de visión pueda funcionar.

5. Iniciar el servidor:
python app.py

💻 Uso
Abre tu navegador y dirígete a http://127.0.0.1:5000 (o al puerto proporcionado por Codespaces).

Haz clic en "Elegir archivos" y selecciona las capturas de pantalla del sistema.

Haz clic en "Generar / Actualizar Excel".

¡Listo! El archivo se descargará automáticamente con todos los datos procesados y listos para su análisis.

