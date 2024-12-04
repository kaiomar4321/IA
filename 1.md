import numpy as np
import matplotlib.pyplot as plt


# Inicializar listas para almacenar los datos
X = []
y = []

# Generar 100 datos
for _ in range(100):
    # Generar precio relativo (X[0]) entre 0 y 1
    precio_relativo = np.random.uniform(0, 1)
    
    # Generar calidad percibida (X[1]) entre 0 y 1
    calidad_percibida = np.random.uniform(0, 1)
    
    # Agregar los datos a la lista
    X.append([precio_relativo, calidad_percibida])
    
    # Determinar si el producto es aceptado o rechazado
    if precio_relativo <= 0.6 and calidad_percibida >= 0.7:
        y.append(1)  # Aceptado
    else:
        y.append(0)  # Rechazado

# Convertir listas a arrays de NumPy
X = np.array(X)
y = np.array(y)

# Mostrar los primeros 5 datos generados para verificación
print("Matriz X:")
print(X[:5])
print("Vector y:")
print(y[:5])

# Inicialización de parámetros
w = np.random.rand(2)  # Pesos iniciales
b = np.random.rand()   # Sesgo inicial
alpha = 0.1            # Tasa de aprendizaje

# Entrenamiento del perceptrón
max_epochs = 500
for epoch in range(max_epochs):
    errors = 0
    for i in range(len(X)):
        x_i = X[i]
        y_pred = 1 if np.dot(w, x_i) + b >= 0 else 0
        if y_pred != y[i]:
            errors += 1
            w += alpha * (y[i] - y_pred) * x_i
            b += alpha * (y[i] - y_pred)
    if errors == 0:
        break

# Frontera de decisión
x1 = np.linspace(0, 1, 100)
x2 = -(w[0] * x1 + b) / w[1]

# Graficar
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='bwr', label='Datos')
plt.plot(x1, x2, label='Frontera de decisión', color='green')
plt.xlabel('Precio relativo')
plt.ylabel('Calidad percibida')
plt.legend()
plt.show()

print(f"Pesos finales: {w}, Sesgo: {b}")
