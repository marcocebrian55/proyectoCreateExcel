import os
import time
import pandas as pd
from flask import Flask, request, send_file, render_template
from ia_processor import extraer_datos_imagen
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # 1. Recogemos la LISTA de archivos que vienen de la web
    archivos = request.files.getlist('file')
    
    if not archivos or archivos[0].filename == '':
        return "Ningún archivo seleccionado", 400
        
    datos_nuevos_lista = []

    # 2. BUCLE: Procesamos cada imagen una por una
    for index, file in enumerate(archivos):
        print(f"\n📸 Procesando imagen {index + 1} de {len(archivos)}: {file.filename}")
        
        imagen_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(imagen_path)
        
        # Llamamos a la IA
        datos = extraer_datos_imagen(imagen_path)
        
        if datos:
            datos_nuevos_lista.append(datos)
            print(f"✅ Datos extraídos de {file.filename}")
        else:
            print(f"⚠️ No se pudieron extraer datos de {file.filename}")
            
        # 3. EL SEMÁFORO: Pausa de 4 segundos para no saturar a Google
        if index < len(archivos) - 1:
            print("⏳ Esperando 4 segundos antes de la siguiente foto...")
            time.sleep(4)
    
    if not datos_nuevos_lista:
        return "Error: No se ha podido procesar ninguna imagen.", 500
        
    try:
        # 4. ACTUALIZAR EXCEL (Acumulativo)
        df_nuevos = pd.DataFrame(datos_nuevos_lista)
        excel_path = os.path.join(UPLOAD_FOLDER, 'reporte_wizard.xlsx')
        
        if os.path.exists(excel_path):
            df_existente = pd.read_excel(excel_path)
            df_final = pd.concat([df_existente, df_nuevos], ignore_index=True)
        else:
            df_final = df_nuevos
            
        df_final.to_excel(excel_path, index=False)
        
        # 5. DISEÑO Y COLORES (Openpyxl)
        wb = load_workbook(excel_path)
        ws = wb.active
        
        # Colores suaves (estilo el tuyo)
        color_rojo = PatternFill(start_color='E6B8B7', end_color='E6B8B7', fill_type='solid')
        color_naranja = PatternFill(start_color='FCD5B4', end_color='FCD5B4', fill_type='solid')
        color_verde = PatternFill(start_color='D8E4BC', end_color='D8E4BC', fill_type='solid')
        color_gris = PatternFill(start_color='D9D9D9', end_color='D9D9D9', fill_type='solid')

        # Formato de cabecera
        for cell in ws[1]:
            cell.fill = color_gris
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')

        # Coloreado condicional de los números
        for row in ws.iter_rows(min_row=2, min_col=2, max_col=ws.max_column):
            for cell in row:
                if isinstance(cell.value, (int, float)):
                    if cell.value <= 0:
                        cell.fill = color_rojo
                    elif 0 < cell.value <= 15:
                        cell.fill = color_naranja
                    else:
                        cell.fill = color_verde
                cell.alignment = Alignment(horizontal='center')
        
        # Ancho de columnas
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = 15

        wb.save(excel_path)
        print(f"🚀 TODO LISTO. Excel actualizado con {len(datos_nuevos_lista)} nuevas filas.")
        
        return send_file(excel_path, as_attachment=True)
        
    except Exception as e:
        print(f"❌ Error final: {e}")
        return f"Error al generar el Excel: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)