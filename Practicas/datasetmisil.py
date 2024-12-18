import pandas as pd
import random

# Variables constantes
altura_salto_sujeto = 1.5  # en metros
velocidad_salto_sujeto = 3  # m/s
distancia_proyectil = 10  # metros

# Función para determinar si esquiva el proyectil
def esquiva_proyectil(vel_proyectil, distancia, altura_salto):
    tiempo_llegada = distancia / vel_proyectil
    altura_alcanzada = velocidad_salto_sujeto * tiempo_llegada
    return 1 if altura_alcanzada >= altura_salto else 0

# Generar dataset
data = []
for _ in range(1000):  # Por ejemplo, 1000 filas
    vel_proyectil = random.uniform(5, 30)  # Velocidad variable entre 5 y 30 m/s
    tiempo_llegada = distancia_proyectil / vel_proyectil
    exito = esquiva_proyectil(vel_proyectil, distancia_proyectil, altura_salto_sujeto)
    data.append([vel_proyectil, distancia_proyectil, tiempo_llegada, exito])

# Crear DataFrame
df = pd.DataFrame(data, columns=['Velocidad_Proyectil', 'Distancia', 'Tiempo_Llegada', 'Exito'])

# Guardar el dataset
df.to_csv('salto_proyectil_dataset.csv', index=False)
