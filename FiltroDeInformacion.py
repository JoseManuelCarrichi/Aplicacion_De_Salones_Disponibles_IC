import requests
import json

api_GeneradorHorarios = 'https://www.eventos.esimecu.ipn.mx/publicacion?carrera=ic&periodo=2023-2%20-%20Enero%202023%20-%20Julio%202023'
# Función que realiza una consulta a la API http y guarda los datos en un archivo llamado datosAPI.json
class filtrarInformacion:

    def __init__(self, api_GeneradorHorarios):
        self.API_key = api_GeneradorHorarios
    
    def consultaAPI(self):
        # Realizar la petición
        response = requests.get(self.API_key)

        #Obtener los datos en formato JSON
        datos_json = response.json()
        # Guardar los datos en el archivo
        with open('datosAPI.json','w') as archivo:
            json.dump(datos_json, archivo)
        print("¡Datos extraidos exitósamente!")

    # Función que obtiene los salones y horarios en los que un salón está ocupado
    def obtenerSalonesOcupados(self):
        # Abre el achivo con los datos de la API y crea un objeto data
        with open("datosAPI.json", "r") as f:
            data = json.load(f)

        nuevo_data = {"data": []}
        # Se iteran todos los campos "data" del objeto, pero se itera solo 
        # en los elementos pares en el campo 'orden'
        for elemento in data["data"]:
            if elemento["orden"] % 2 == 0:
                count = 1;
                salones = [data["data"][elemento["orden"] + 1]["v_l"],
                        data["data"][elemento["orden"] + 1]["v_m"], 
                        data["data"][elemento["orden"] + 1]["v_x"],
                        data["data"][elemento["orden"] + 1]["v_j"],
                        data["data"][elemento["orden"] + 1] ["v_v"]]
                arr = [elemento["v_l"], elemento["v_m"], elemento["v_x"], elemento["v_j"], elemento["v_v"]]
                # Para cada día se buscan los salones y horarios. Dado que hay horarios sin salón asignado
                # se utiliza un parseo de datos para validar el número de salón, si hay un error, el salón
                # es inválido y no se copia al nuevo archivo
                for dia in arr:
                    if dia != "-": 
                        try:
                            nuevo_elemento = {
                                "dia": count,
                                "horario": dia,
                                "salon": int(salones[count-1])
                            }
                            count = count + 1
                            nuevo_data["data"].append(nuevo_elemento)
                        except:
                            count = count + 1
                    else:
                        count = count + 1  
        # Se guarda el nuevo archivo con los datos de los salones ocupados
        with open("salonesOcupados.json", "w") as f:
            json.dump(nuevo_data, f)
        # Mensaje de confirmación
        print("¡Extracción de salones exitosa!")
    
    # Función que ordena los salones de manera ascendente
    def ordenarSalones(self):
        # Lee el archivo JSON con los salones ocupados
        with open('salonesOcupados.json', 'r') as f:
            data = json.load(f)

        # Itera sobre los elementos y separa la cadena del campo "horario"
        for elemento in data['data']:
            # Separa la cadena en dos partes utilizando el separador "a"
            hora_inicio, hora_fin = elemento['horario'].split('a')
            # Elimina los espacios en blanco al inicio y al final de cada parte
            hora_inicio = hora_inicio.strip()
            hora_fin = hora_fin.strip()
            # Convierte la hora en formato hh:mm a un número decimal
            hora_inicio_decimal = int(hora_inicio.split(':')[0]) + int(hora_inicio.split(':')[1])/60
            hora_fin_decimal = int(hora_fin.split(':')[0]) + int(hora_fin.split(':')[1])/60
            # Guarda los valores en los campos "horaInicio" y "horaFin"
            elemento['horaInicio'] = hora_inicio_decimal
            elemento['horaFin'] = hora_fin_decimal
            # Elimina el campo "horario" original
            del elemento['horario']

        # Ordena los elementos según el número de salón, el número de día y la hora de inicio de clase
        data_ordenado = sorted(data['data'], key=lambda x: (x['salon'], x['dia'], x['horaInicio']))

        # Guarda el resultado en un nuevo archivo JSON
        with open('archivo_ordenado.json', 'w') as f:
            json.dump({'data': data_ordenado}, f)

        # Mensaje de confirmación
        print("¡Ordenamiento exitoso!")
    
    # Función que itera el archivo ordenado para determinar los salones disponibles
    def obtenerSalonesDisponibles(self):
        # Definir las horas de inicio y fin de cada clase
        horas_clase = [7.0, 8.5, 10.0, 11.5, 13.0, 14.5, 16.0, 17.5, 19.0, 20.5]

        # Inicializar el diccionario para almacenar la información de los salones disponibles
        salones_disponibles = {"data": []}

        # Abrir el archivo json con la información de los horarios ocupados
        with open('archivo_ordenado.json') as f:
            data = json.load(f)
        
        listaSalones = [1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110,
                        1111, 1112, 1113, 1114, 1115, 1119, 
                        1201, 1202, 1203, 1204, 1205, 1206,1207, 1208, 1209, 1210,
                        1211, 1212, 1213, 1214, 1215,
                        2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110,
                        2111, 2112,
                        2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210,
                        2211, 2212, 2213, 2214, 2215,
                        3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 
                        3111, 3112, 3113, 3114, 3115,
                        3201, 3202, 3203, 3204, 3205, 3206, 3207, 3208, 3209, 3210,
                        3211, 3212, 3213, 3214, 3215]
        # Iterar a través de cada día, hora y salón
        for dia in range(1, 6):
            for hora in horas_clase:
                #for salon in range(int(salones[0]), int(salones[-1])+1):
                for salon in listaSalones:
                    ocupado = False
                    for horario in data['data']:
                        if horario['dia'] == dia and horario['salon'] == salon and \
                        horario['horaInicio'] <= hora and horario['horaFin'] >= hora + 1.5:
                            ocupado = True
                            break
                    if not ocupado:
                        # Si el horario está disponible, agregarlo a la lista de horarios disponibles para el salón correspondiente
                        if salon not in salones_disponibles:
                            nuevo_elemento = {
                                'salon': salon,
                                'dia': dia,
                                "horaInicio":hora
                            }
                        salones_disponibles["data"].append(nuevo_elemento)
        
        # Escribir la información obtenida en un archivo json
        with open('salonesDisponibles.json', 'w') as f:
            json.dump(salones_disponibles, f)
        # Abrir archivo
        # Lee el archivo JSON con los salones ocupados
        with open('salonesDisponibles.json', 'r') as f:
            data = json.load(f)
        data_ordenado = sorted(data['data'], key=lambda x: (x['salon'], x['dia'], x['horaInicio']))
        # Guardar los datos ordenados
        with open('salonesDisponibles.json', 'w') as f:
            json.dump({'data': data_ordenado}, f)

        print("¡Salones disponibles actualizados exitosamente!")




# Crear un objeto y acceder a los 
obj  = filtrarInformacion(api_GeneradorHorarios)
obj.consultaAPI()
obj.obtenerSalonesOcupados()
obj.ordenarSalones()
obj.salonesDisponibles()