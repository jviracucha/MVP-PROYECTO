import psutil
import time
import pygetwindow as gw

def obtener_lista_procesos():
    """Obtiene la lista de procesos en ejecución."""
    return [p.info for p in psutil.process_iter(['pid', 'name', 'create_time', 'cpu_percent', 'memory_percent'])]

def obtener_lista_ventanas():
    """Obtiene la lista de ventanas abiertas."""
    return gw.getAllTitles()

def sugerir_aplicaciones_no_utilizadas(tiempo_limite=1800):  # 1800 segundos = 30 minutos
    """Sugiere aplicaciones que no se han utilizado en un tiempo específico."""
    tiempo_actual = time.time()

    for proceso in obtener_lista_procesos():
        tiempo_inicio = proceso['create_time']
        tiempo_transcurrido = tiempo_actual - tiempo_inicio

        if tiempo_transcurrido > tiempo_limite and proceso['memory_percent'] < 5:
            print(f"Sugerencia: La aplicación '{proceso['name']}' se ejecuta en segundo plano o no se ha utilizado recientemente.")

    ventanas_abiertas = obtener_lista_ventanas()
    for ventana in ventanas_abiertas:
        print(f"Ventana en uso: {ventana}")

if __name__ == "__main__":
    sugerir_aplicaciones_no_utilizadas()