import json
import datetime

class informacion:
    def __init__(self):
        self.archivo = "salonesDisponibles.json"
        self.dia = 0
        self.hora = 0.0
    
    # Función que obtiene el día y hora actuales del dispositivo
    def obtenerDiaHora(self):
        # Obtener la fecha y hora actual
        now = datetime.datetime.now()
        # Obtener el día de la semana
        self.dia = now.weekday() + 1
        # Obtener la hora actual
        hora = now.strftime("%H:%M")
        # Convertir la hora a decimal con dos decimales de presición
        self.hora = round(int(hora.split(':')[0]) + int(hora.split(':')[1])/60, 2)

    # Función que muesra un salón según la búsqueda de disponibilidad

    def mostrarSalonesDispoibles(self):
        # Leer el archivo JSON
        with open(self.archivo) as file:
            data = json.load(file)['data']

        # Verificar qué salones no están siendo ocupados
        salones_disponibles = set()
        for registro in data:
            if registro['dia'] == self.dia and registro['horaInicio'] <= self.hora and self.hora < registro['horaInicio']+1.5:
                salones_disponibles.add(registro['salon'])

        # Imprimir la lista de salones que no están siendo ocupados
        print("Salones disponibles:")
        for salon in sorted(salones_disponibles):
            print(salon)                   
                

info = informacion()
info.obtenerDiaHora()
info.mostrarSalonesDispoibles()

