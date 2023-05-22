import csv
import os
import sqlite3
import subprocess
import tkinter as tk
import webbrowser

import pyperclip


# Función para obtener el contenido del portapapeles
def obtener_portapapeles():
    return pyperclip.paste()


# Función para obtener el historial del navegador
def obtener_historial_navegador():
    # Directorio del historial del navegador (Ejemplo para Google Chrome en macOS)
    directorio_historial = os.path.expanduser('~') + "/Library/Application Support/Google/Chrome/Default"

    # Conexión a la base de datos del historial del navegador
    conexion = sqlite3.connect(directorio_historial + "/History")
    cursor = conexion.cursor()

    # Consulta para obtener el historial de navegación
    consulta = "SELECT title, url FROM urls"
    cursor.execute(consulta)
    resultados = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Formatear los resultados del historial
    contenido_historial = ""
    for resultado in resultados:
        titulo = resultado[0]
        url = resultado[1]
        contenido_historial += f"Título: {titulo}\nURL: {url}\n\n"

    return contenido_historial


# Función para abrir una URL en el navegador predeterminado
def abrir_url(url):
    webbrowser.open(url)


# Función para obtener las listas de redes en macOS
def obtener_listas_red():
    # Ejecutar el comando 'networksetup -listallhardwareports' para obtener las interfaces de red
    proceso = subprocess.Popen(["networksetup", "-listallhardwareports"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida, error = proceso.communicate()

    # Decodificar la salida del comando
    salida_decodificada = salida.decode("utf-8", errors="ignore")

    return salida_decodificada


# Función para mostrar los resultados en una ventana de GUI
def mostrar_resultados(contenido_portapapeles, contenido_historial, contenido_redes):
    ventana = tk.Tk()
    ventana.title("Resultados")

    # Etiquetas de los resultados
    etiqueta_portapapeles = tk.Label(ventana, text="Contenido del Portapapeles:")
    etiqueta_portapapeles.pack()

    texto_portapapeles = tk.Text(ventana)
    texto_portapapeles.insert(tk.END, contenido_portapapeles)
    texto_portapapeles.pack()

    etiqueta_historial = tk.Label(ventana, text="Historial del Navegador:")
    etiqueta_historial.pack()

    texto_historial = tk.Text(ventana)
    texto_historial.insert(tk.END, contenido_historial)
    texto_historial.pack()

    etiqueta_redes = tk.Label(ventana, text="Listas de Redes:")
    etiqueta_redes.pack()

    texto_redes = tk.Text(ventana)
    texto_redes.insert(tk.END, contenido_redes)
    texto_redes.pack()

    ventana.mainloop()


# Función principal
def main():
    # Obtener el contenido del portapapeles
    contenido_portapapeles = obtener_portapapeles()

    # Obtener el historial del navegador
    contenido_historial = obtener_historial_navegador()

    # Obtener las listas de redes
    contenido_redes = obtener_listas_red()

    # Guardar los resultados en un archivo CSV
    with open("resultados.csv", "w", newline="") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(["Contenido del Portapapeles", "Historial del Navegador", "Listas de Redes"])
        escritor_csv.writerow([contenido_portapapeles, contenido_historial, contenido_redes])

    # Mostrar los resultados en una ventana de GUI
    mostrar_resultados(contenido_portapapeles, contenido_historial, contenido_redes)


# Ejecutar la función principal
if __name__ == "__main__":
    main()
