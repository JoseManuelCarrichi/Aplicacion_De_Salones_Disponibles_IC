import datetime


# Obtener la fecha y hora actual
now = datetime.datetime.now()
# Obtener el día de la semana
dia = now.weekday() + 1
# Obtener la hora actual
hora = now.strftime("%H:%M")
# Convertir la hora a decimal con dos decimales de presición
hora_decimal = round(int(hora.split(':')[0]) + int(hora.split(':')[1])/60, 2)
# imprimir el día, y hora actuales
print("Día: " + str(dia))
print("Hora: " + hora)
print("Hora decimal: " + str(hora_decimal))
