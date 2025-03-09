import pandas as pd

# Función para mapear descripciones a Payee
def map_payee(description):
    if 'UBER' in description:
        return 'Uber'
    elif 'AMAZON' in description:
        return 'Amazon'
    elif 'ADOBE' in description:
        return 'Adobe'
    elif 'UPWORK' in description:
        return 'Upwork'
    elif 'REGUS' in description:
        return 'Regus Management'
    elif '7-ELEVEN' in description:
        return '7-Eleven'
    else:
        return 'Other'

# Leer el archivo CSV, saltando las primeras 7 líneas (6 de metadatos + 1 en blanco)
try:
    transactions_df = pd.read_csv(
        'Calcoast_Calendar Year 2024 Transactions_Example (1).csv',
        delimiter=',',  # Cambia esto si el delimitador no es una coma
        skiprows=7,  # Saltar las primeras 7 líneas
        engine='python'  # Usar el motor de Python para manejar errores
    )
except pd.errors.ParserError as e:
    print(f"Error al leer el archivo CSV: {e}")
    print("Intentando leer el archivo como texto y limpiarlo...")
    
    # Leer el archivo como texto
    with open('Calcoast_Calendar Year 2024 Transactions_Example (1).csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Saltar las primeras 7 líneas (6 de metadatos + 1 en blanco)
    cleaned_lines = lines[7:]
    
    # Convertir las líneas limpias en un DataFrame
    transactions_df = pd.read_csv(pd.compat.StringIO(''.join(cleaned_lines)))

# Limpiar los nombres de las columnas (eliminar tabuladores y espacios al final)
transactions_df.columns = transactions_df.columns.str.strip()

# Mostrar las primeras filas para verificar que se leyó correctamente
print("Datos leídos correctamente:")
print(transactions_df.head())

# Verificar los nombres de las columnas
print("\nNombres de las columnas:")
print(transactions_df.columns)

# Seleccionar y transformar las columnas necesarias
# Asegúrate de que los nombres de las columnas coincidan con los del archivo CSV
ready_to_upload_df = transactions_df[['Transaction ID', 'Date', 'Description', 'Amount']].copy()

# Renombrar las columnas para que coincidan con el formato de ReadyToUpload
ready_to_upload_df.columns = ['Reference', 'Date', 'Description', 'Amount']

# Agregar una columna de Payee usando la función map_payee
ready_to_upload_df['Payee'] = ready_to_upload_df['Description'].apply(map_payee)

# Mostrar las primeras filas del nuevo DataFrame
print("\nDatos transformados:")
print(ready_to_upload_df.head())

# Guardar el archivo final
ready_to_upload_df.to_csv('Calcoast_Calendar Year 2024_ReadytoUpload_Final.csv', index=False)

print("\nArchivo 'Calcoast_Calendar Year 2024_ReadytoUpload_Final.csv' generado con éxito!")