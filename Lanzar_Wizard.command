#!/bin/bash

# 1. Navegar a tu carpeta del proyecto
cd "/Users/marcocebrian/Desktop/WIZARD PROYECTO"

# 2. Activar el entorno virtual de Python
source venv/bin/activate

# 3. Abrir la página web en tu navegador (Chrome/Safari) automáticamente
open http://127.0.0.1:5000

# 4. Encender el servidor
echo "🧙‍♂️ Encendiendo el Mago de Wizard..."
python3 backend/app.py