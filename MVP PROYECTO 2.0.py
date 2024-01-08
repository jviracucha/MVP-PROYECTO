import psutil
import time
import pygetwindow as gw
from fpdf import FPDF


def obtener_lista_procesos():
    """Obtiene la lista de procesos en ejecución."""
    try:
        return [p.info for p in psutil.process_iter(['pid', 'name', 'create_time', 'cpu_percent', 'memory_percent'])]
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return []


def obtener_lista_ventanas():
    """Obtiene la lista de ventanas abiertas."""
    return gw.getAllTitles()


def formatear_tiempo(tiempo_segundos):
    """Convierte el tiempo de segundos a un formato legible."""
    minutos, segundos = divmod(tiempo_segundos, 60)
    return f"{int(minutos)} minutos y {int(segundos)} segundos"


def sugerir_aplicaciones_no_utilizadas(tiempo_limite=1800):  # 1800 segundos = 30 minutos
    """Sugiere aplicaciones que no se han utilizado en un tiempo específico."""
    tiempo_actual = time.time()
    info_ventanas = []  # Lista para almacenar la información de las ventanas no utilizadas

    for proceso in obtener_lista_procesos():
        tiempo_inicio = proceso['create_time']
        tiempo_transcurrido = tiempo_actual - tiempo_inicio

        if tiempo_transcurrido > tiempo_limite and proceso['memory_percent'] < 5:
            mensaje = f"Sugerencia: La aplicación '{proceso['name']}' se ejecuta en segundo plano o no se ha utilizado recientemente."
            print(mensaje)
            info_ventanas.append(f"{mensaje} Tiempo de uso: {formatear_tiempo(tiempo_transcurrido)}.")

    ventanas_abiertas = obtener_lista_ventanas()
    for ventana in ventanas_abiertas:
        print(f"Ventana en uso: {ventana}")
        info_ventanas.append(f"Ventana en uso: {ventana}")

    # Crear el archivo PDF con la información de las ventanas no utilizadas
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for info in info_ventanas:
        pdf.cell(200, 10, txt=info, ln=True)

    pdf_file = "informe_ventanas.pdf"
    pdf_output_path = f"C:\\Users\\TuUsuario\\Desktop\\{pdf_file}"
    pdf.output(pdf_output_path)
    print(f"Se ha creado el archivo PDF en: {pdf_output_path}")


if __name__ == "__main__":
    sugerir_aplicaciones_no_utilizadas()
