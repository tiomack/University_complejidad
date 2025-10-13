# 🚀 Laboratorio de Comparación de Algoritmos de Ordenamiento

Aplicación interactiva con interfaz gráfica para analizar y comparar el comportamiento de cuatro algoritmos de ordenamiento clásicos desde una perspectiva teórica y empírica.

## 📋 Descripción

Este laboratorio permite ejecutar experiencias para medir y comparar:
- **Bubble Sort**
- **Insertion Sort**
- **Quick Sort**
- **Heap Sort**

### Características principales

✨ **Análisis Empírico**
- Medición precisa del tiempo de ejecución
- Conteo de instrucciones ejecutadas
- Soporte para múltiples tamaños de entrada (ej: 1k, 5k, 10k, etc.)

📊 **Visualización**
- Gráficos comparativos interactivos
- Tiempo de ejecución vs. Tamaño de entrada
- Total de instrucciones vs. Tamaño de entrada
- Opción de escala logarítmica para mejor visualización

📖 **Análisis Teórico**
- Explicación de complejidad temporal de cada algoritmo
- Comparación de notación Big O
- Casos peor, promedio y mejor

💾 **Exportación de Datos**
- Exportación de resultados en formato CSV
- Promedios automáticos de múltiples ejecuciones

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.6 o superior
- Tkinter (usualmente viene incluido con Python)

### Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/TU_USUARIO/complejidad-algoritmos.git
cd complejidad-algoritmos
```

2. (Opcional) Crea un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Ejecución

```bash
python3 CDA_tarea.py
```

O si tienes permisos de ejecución:
```bash
chmod +x CDA_tarea.py
./CDA_tarea.py
```

## 📖 Cómo usar la aplicación

1. **Configurar tamaños de entrada**: Ingresa una serie de tamaños separados por comas (ej: `1000, 5000, 10000, 50000`)
   - Puedes usar sufijos: `1k` = 1000, `5k` = 5000, `1m` = 1,000,000

2. **Ejecutar experimentos**: Haz clic en "🚀 Ejecutar Serie"
   - La aplicación generará arrays aleatorios y ejecutará los 4 algoritmos
   - Los resultados se mostrarán en el log de ejecución

3. **Ver gráficos**: Haz clic en "📊 Ver Gráficos Comparativos"
   - Pestaña 1: Tiempo de ejecución vs. Tamaño
   - Pestaña 2: Instrucciones vs. Tamaño
   - Checkbox para escala logarítmica

4. **Exportar resultados**: Haz clic en "💾 Exportar Resultados"
   - Genera archivos CSV con los promedios de cada algoritmo

5. **Análisis teórico**: Consulta la pestaña "Análisis Teórico de Complejidad"
   - Explicación detallada de la complejidad de cada algoritmo

## 📊 Complejidades Temporales

| Algoritmo | Mejor Caso | Caso Promedio | Peor Caso | Espacio |
|-----------|-----------|---------------|-----------|---------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |

## 🛠️ Tecnologías Utilizadas

- **Python 3**: Lenguaje de programación principal
- **Tkinter**: Interfaz gráfica de usuario
- **Threading**: Ejecución asíncrona para no bloquear la UI
- **CSV**: Exportación de resultados

## 📝 Estructura del Código

```
CDA_tarea.py
├── Clase AlgoritmoOrdenamiento: Almacena métricas de cada algoritmo
├── Implementaciones de algoritmos:
│   ├── bubble_sort()
│   ├── insertion_sort()
│   ├── quick_sort()
│   └── heap_sort()
├── Clase AplicacionLaboratorio: Interfaz gráfica principal
│   ├── Panel de configuración
│   ├── Panel de resultados
│   ├── Sistema de gráficos
│   └── Exportación de datos
└── main(): Punto de entrada
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 👤 Autor

Proyecto creado para el análisis de complejidad de algoritmos.

## 🙏 Agradecimientos

- Implementaciones basadas en algoritmos clásicos de ordenamiento
- Interfaz diseñada para fines educativos

