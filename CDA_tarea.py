#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratorio: Comparación de Algoritmos de Ordenamiento

Objetivo: Analizar y comparar el comportamiento de Bubble Sort, Insertion Sort,
QuickSort y HeapSort desde una perspectiva teórica y empírica.

Funcionalidades:
- Ejecución de experiencias para tamaños de entrada únicos o en serie.
- Medición de tiempo de ejecución y conteo de instrucciones.
- Generación de gráficos comparativos para los 4 algoritmos:
  1. Tiempo de ejecución vs. Tamaño de entrada.
  2. Total de instrucciones vs. Tamaño de entrada.
- Opción de escala logarítmica para una mejor visualización comparativa.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import random
import csv
from typing import List, Tuple, Dict
import threading
import math
import statistics

class AlgoritmoOrdenamiento:
    """
    Clase base para almacenar las métricas de un algoritmo de ordenamiento.
    """
    def __init__(self, nombre: str, color: str):
        self.nombre = nombre
        self.color = color
        self.resultados = {}  # {tamanio: (tiempo, instrucciones)}

    def agregar_metricas(self, tamanio: int, tiempo: float, instrucciones: int):
        """Agrega métricas de una ejecución para un tamaño específico."""
        if tamanio not in self.resultados:
            self.resultados[tamanio] = []
        self.resultados[tamanio].append((tiempo, instrucciones))

    def obtener_promedios(self) -> List[Tuple[int, float, int]]:
        """Devuelve una lista de (tamaño, tiempo_promedio, instrucciones_promedio) ordenada por tamaño."""
        promedios = []
        for tamanio, mediciones in sorted(self.resultados.items()):
            if not mediciones:
                continue
            avg_tiempo = sum(m[0] for m in mediciones) / len(mediciones)
            avg_instrucciones = sum(m[1] for m in mediciones) / len(mediciones)
            promedios.append((tamanio, avg_tiempo, int(avg_instrucciones)))
        return promedios

    def limpiar_datos(self):
        """Limpia todos los resultados almacenados."""
        self.resultados.clear()

    def exportar_csv(self, filename: str):
        """Exporta los promedios de las métricas a un archivo CSV."""
        datos = self.obtener_promedios()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Tamaño', 'Tiempo Promedio (s)', 'Instrucciones Promedio'])
            for tamanio, tiempo, instrucciones in datos:
                writer.writerow([tamanio, tiempo, instrucciones])
        return f"📊 Métricas de {self.nombre} exportadas a {filename}"

# --- Implementaciones de Algoritmos de Ordenamiento (conteo de instrucciones) ---

def bubble_sort(arr: List[int]) -> Tuple[List[int], int]:
    n = len(arr)
    total_instrucciones = 0
    arr_copy = arr.copy()
    total_instrucciones += 1
    for i in range(n):
        total_instrucciones += 1
        for j in range(0, n - i - 1):
            total_instrucciones += 1
            if arr_copy[j] > arr_copy[j + 1]:
                total_instrucciones += 1
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                total_instrucciones += 1
    return arr_copy, total_instrucciones

def heapify(arr: List[int], n: int, i: int, contador: int) -> int:
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    contador += 3
    if left < n and arr[left] > arr[largest]:
        largest = left
        contador += 1
    if right < n and arr[right] > arr[largest]:
        largest = right
        contador += 1
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        contador += 1
        contador = heapify(arr, n, largest, contador)
    return contador

def heap_sort(arr: List[int]) -> Tuple[List[int], int]:
    n = len(arr)
    total_instrucciones = 0
    arr_copy = arr.copy()
    for i in range(n // 2 - 1, -1, -1):
        total_instrucciones += 1
        total_instrucciones = heapify(arr_copy, n, i, total_instrucciones)
    for i in range(n - 1, 0, -1):
        total_instrucciones += 1
        arr_copy[0], arr_copy[i] = arr_copy[i], arr_copy[0]
        total_instrucciones += 1
        total_instrucciones = heapify(arr_copy, i, 0, total_instrucciones)
    return arr_copy, total_instrucciones

def quick_sort(arr: List[int]) -> Tuple[List[int], int]:
    arr_copy = arr.copy()
    total_instrucciones = [0]
    def _partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        total_instrucciones[0] += 2
        for j in range(low, high):
            total_instrucciones[0] += 1
            if arr[j] <= pivot:
                total_instrucciones[0] += 1
                i += 1
                total_instrucciones[0] += 1
                arr[i], arr[j] = arr[j], arr[i]
                total_instrucciones[0] += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        total_instrucciones[0] += 1
        return i + 1
    def _quick_sort_helper(arr, low, high):
        if low < high:
            total_instrucciones[0] += 1
            pi = _partition(arr, low, high)
            total_instrucciones[0] += 1
            _quick_sort_helper(arr, low, pi - 1)
            _quick_sort_helper(arr, pi + 1, high)
    _quick_sort_helper(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy, total_instrucciones[0]

def insertion_sort(arr: List[int]) -> Tuple[List[int], int]:
    arr_copy = arr.copy()
    total_instrucciones = 0
    for i in range(1, len(arr_copy)):
        total_instrucciones += 1
        key = arr_copy[i]
        total_instrucciones += 1
        j = i - 1
        total_instrucciones += 1
        while j >= 0 and arr_copy[j] > key:
            total_instrucciones += 2
            arr_copy[j + 1] = arr_copy[j]
            total_instrucciones += 1
            j -= 1
            total_instrucciones += 1
        arr_copy[j + 1] = key
        total_instrucciones += 1
    return arr_copy, total_instrucciones

def generar_array_aleatorio(n: int) -> List[int]:
    """Genera un array de n enteros aleatorios."""
    return [random.randint(1, 100000) for _ in range(n)]

class AplicacionLaboratorio:
    """
    Aplicación principal con interfaz gráfica para el laboratorio.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Laboratorio de Comparación de Algoritmos de Ordenamiento")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        self.algoritmos = {
            'Bubble Sort': AlgoritmoOrdenamiento('Bubble Sort', '#e55353'),
            'Insertion Sort': AlgoritmoOrdenamiento('Insertion Sort', '#f9b115'),
            'Heap Sort': AlgoritmoOrdenamiento('Heap Sort', '#3399ff'),
            'Quick Sort': AlgoritmoOrdenamiento('Quick Sort', '#2eb85c')
        }
        self.funciones_ordenamiento = {
            'Bubble Sort': bubble_sort, 'Insertion Sort': insertion_sort,
            'Heap Sort': heap_sort, 'Quick Sort': quick_sort
        }
        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        self.crear_panel_configuracion(main_frame)
        self.crear_panel_resultados(main_frame)

    def crear_panel_configuracion(self, parent):
        config_frame = ttk.LabelFrame(parent, text="📝 CONFIGURACIÓN Y EJECUCIÓN", padding="10")
        config_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)

        # Entradas para tamaños
        ttk.Label(config_frame, text="Serie de tamaños (ej: 1k, 5k, 10k):").grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        self.entrada_serie = ttk.Entry(config_frame, width=40)
        self.entrada_serie.grid(row=0, column=1, padx=(0, 20), sticky=(tk.W, tk.E))
        self.entrada_serie.insert(0, "1000, 5000, 10000, 20000, 50000")

        # Botones de acción
        btn_frame = ttk.Frame(config_frame)
        btn_frame.grid(row=0, column=2, padx=(10, 0))

        self.btn_ejecutar_serie = ttk.Button(btn_frame, text="🚀 Ejecutar Serie", command=self.ejecutar_serie)
        self.btn_ejecutar_serie.pack(side=tk.LEFT, padx=5)

        self.btn_graficos = ttk.Button(btn_frame, text="📊 Ver Gráficos Comparativos", command=self.abrir_ventana_graficos)
        self.btn_graficos.pack(side=tk.LEFT, padx=5)
        
        self.btn_exportar = ttk.Button(btn_frame, text="💾 Exportar Resultados", command=self.exportar_resultados, state='disabled')
        self.btn_exportar.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="🧹 Limpiar Datos", command=self.limpiar_datos).pack(side=tk.LEFT, padx=5)

        self.progress = ttk.Progressbar(config_frame, mode='determinate')
        self.progress.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

    def crear_panel_resultados(self, parent):
        resultados_frame = ttk.LabelFrame(parent, text="📋 LOG DE EJECUCIÓN Y ANÁLISIS", padding="10")
        resultados_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        resultados_frame.rowconfigure(0, weight=1)
        resultados_frame.columnconfigure(0, weight=1)

        notebook = ttk.Notebook(resultados_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Pestaña de Log
        log_frame = ttk.Frame(notebook)
        self.log_text = scrolledtext.ScrolledText(log_frame, font=('Consolas', 9), height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        notebook.add(log_frame, text="Log de Ejecución")

        # Pestaña de Análisis Teórico
        complejidad_frame = ttk.Frame(notebook)
        texto_complejidad = scrolledtext.ScrolledText(complejidad_frame, wrap=tk.WORD, font=('Consolas', 10))
        texto_complejidad.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        texto_complejidad.insert(tk.END, self.obtener_texto_complejidad())
        texto_complejidad.config(state=tk.DISABLED)
        notebook.add(complejidad_frame, text="Análisis Teórico de Complejidad")

    def ejecutar_serie(self):
        try:
            serie_str = self.entrada_serie.get()
            if not serie_str:
                messagebox.showerror("Error", "La serie de tamaños no puede estar vacía.")
                return
            
            tamanos_str = serie_str.replace(' ', '').lower().split(',')
            tamanos = []
            for s in tamanos_str:
                if 'm' in s:
                    tamanos.append(int(float(s.replace('m', '')) * 1_000_000))
                elif 'k' in s:
                    tamanos.append(int(float(s.replace('k', '')) * 1_000))
                else:
                    tamanos.append(int(s))
            
            if any(n <= 0 for n in tamanos):
                messagebox.showerror("Error", "Todos los tamaños deben ser mayores a 0.")
                return
            
            self.bloquear_controles(True)
            thread = threading.Thread(target=self._ejecutar_serie_worker, args=(tamanos,), daemon=True)
            thread.start()

        except (ValueError, TypeError):
            messagebox.showerror("Error", "Formato de serie inválido. Use números separados por comas (ej: 1000, 5k, 10k).")
        
    def _ejecutar_serie_worker(self, tamanos: List[int]):
        total_pasos = len(tamanos) * len(self.algoritmos)
        paso_actual = 0
        self.progress['maximum'] = total_pasos
        
        try:
            for n in sorted(tamanos):
                self.log(f"\n--- INICIANDO EXPERIENCIA PARA n = {n:,} ---")
                array_original = generar_array_aleatorio(n)
                
                for nombre, func in self.funciones_ordenamiento.items():
                    paso_actual += 1
                    self.progress['value'] = paso_actual
                    self.log(f"🔄 Ejecutando {nombre}...")
                    
                    tiempo_inicio = time.perf_counter()
                    _, instrucciones = func(array_original)
                    tiempo_total = time.perf_counter() - tiempo_inicio
                    
                    self.algoritmos[nombre].agregar_metricas(n, tiempo_total, instrucciones)
                    self.log(f"  ✅ Tiempo: {tiempo_total:.6f}s | Instrucciones: {instrucciones:,}")

            self.log("\n✅✅✅ SERIE DE EXPERIENCIAS COMPLETADA ✅✅✅")
        except Exception as e:
            self.log(f"❌ ERROR: {e}")
            messagebox.showerror("Error en Ejecución", str(e))
        finally:
            self.bloquear_controles(False)

    def abrir_ventana_graficos(self):
        if not any(alg.resultados for alg in self.algoritmos.values()):
            messagebox.showwarning("Sin Datos", "Debe ejecutar al menos una experiencia antes de generar gráficos.")
            return

        win = tk.Toplevel(self.root)
        win.title("📊 Gráficos Comparativos de Algoritmos")
        win.geometry("1100x750")

        notebook = ttk.Notebook(win)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pestaña 1: Tiempo vs Tamaño
        frame_tiempo = ttk.Frame(notebook)
        notebook.add(frame_tiempo, text="Tiempo de Ejecución vs. Tamaño")
        self.crear_panel_grafico(frame_tiempo, 'tiempo')

        # Pestaña 2: Instrucciones vs Tamaño
        frame_inst = ttk.Frame(notebook)
        notebook.add(frame_inst, text="Instrucciones vs. Tamaño")
        self.crear_panel_grafico(frame_inst, 'instrucciones')

    def crear_panel_grafico(self, parent, data_type: str):
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        log_scale_var = tk.BooleanVar(value=(data_type == 'instrucciones'))
        ttk.Checkbutton(top_frame, text="Usar Escala Logarítmica (Eje Y)", variable=log_scale_var,
                        command=lambda: self.dibujar_grafico_comparativo(canvas, data_type, log_scale_var.get())).pack(side=tk.LEFT)

        canvas = tk.Canvas(parent, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dibujar el gráfico cuando el canvas esté listo
        canvas.bind("<Configure>", lambda e: self.dibujar_grafico_comparativo(e.widget, data_type, log_scale_var.get()))

    def dibujar_grafico_comparativo(self, canvas: tk.Canvas, data_type: str, use_log_scale: bool):
        canvas.delete("all")
        
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        m_left, m_right, m_top, m_bottom = 100, 50, 50, 80
        plot_w = width - m_left - m_right
        plot_h = height - m_top - m_bottom

        if plot_w <= 0 or plot_h <= 0: return

        all_data = {}
        min_x, max_x, min_y, max_y = float('inf'), 0, float('inf'), 0

        for nombre, alg in self.algoritmos.items():
            promedios = alg.obtener_promedios()
            if not promedios: continue
            
            tamanos = [p[0] for p in promedios]
            valores = [p[1] if data_type == 'tiempo' else p[2] for p in promedios]
            all_data[nombre] = (tamanos, valores, alg.color)

            min_x = min(min_x, min(tamanos))
            max_x = max(max_x, max(tamanos))
            min_y = min(min_y, min(v for v in valores if v > 0)) # Mínimo > 0 para log
            max_y = max(max_y, max(valores))

        if not all_data: return

        if min_x == max_x: max_x = min_x + 1
        min_y_final = 1 if use_log_scale and min_y == float('inf') else (min_y if use_log_scale else 0)
        if min_y_final >= max_y: max_y = min_y_final + 1
        
        # Funciones de mapeo
        def map_x(x): return m_left + (x - min_x) / (max_x - min_x) * plot_w
        def map_y(y):
            if use_log_scale:
                if y <= 0: return m_top + plot_h
                log_min = math.log10(min_y_final)
                log_max = math.log10(max_y)
                if log_max == log_min: return m_top + plot_h
                return m_top + (1 - (math.log10(y) - log_min) / (log_max - log_min)) * plot_h
            else:
                return m_top + (1 - (y - min_y_final) / (max_y - min_y_final)) * plot_h

        # Dibujar ejes, ticks y título
        self._dibujar_ejes(canvas, m_left, m_top, plot_w, plot_h, min_x, max_x, min_y_final, max_y, map_x, map_y, data_type, use_log_scale)

        # Dibujar datos y leyenda
        legend_y_start = m_top + 10
        for i, (nombre, (tamanos, valores, color)) in enumerate(all_data.items()):
            coords = []
            for x, y in zip(tamanos, valores):
                px, py = map_x(x), map_y(y)
                coords.extend([px, py])
                canvas.create_oval(px - 3, py - 3, px + 3, py + 3, fill=color, outline=color)
            if len(coords) >= 4:
                canvas.create_line(coords, fill=color, width=2)
            
            # Leyenda
            canvas.create_rectangle(width - 220, legend_y_start + i*20 - 5, width-215, legend_y_start + i*20 + 5, fill=color, outline=color)
            canvas.create_text(width - 210, legend_y_start + i*20, text=nombre, anchor=tk.W)

    def _dibujar_ejes(self, canvas, m_l, m_t, p_w, p_h, min_x, max_x, min_y, max_y, map_x, map_y, data_type, use_log_scale):
        # Ejes
        canvas.create_line(m_l, m_t, m_l, m_t + p_h, width=2)
        canvas.create_line(m_l, m_t + p_h, m_l + p_w, m_t + p_h, width=2)

        # Título
        y_label = "Tiempo de Ejecución (s)" if data_type == 'tiempo' else "Total de Instrucciones"
        if use_log_scale: y_label += " (Escala Logarítmica)"
        canvas.create_text(m_l + p_w / 2, m_t / 2, text=f"{y_label} vs. Tamaño de Entrada", font=("Arial", 14, "bold"))
        canvas.create_text(m_l + p_w / 2, m_t + p_h + 45, text="Tamaño de Entrada (n)", font=("Arial", 11))
        canvas.create_text(25, m_t + p_h / 2, text=y_label, angle=90, font=("Arial", 11))

        # Ticks X
        for i in range(6):
            val = min_x + i * (max_x - min_x) / 5
            px = map_x(val)
            canvas.create_line(px, m_t + p_h, px, m_t + p_h + 5)
            canvas.create_text(px, m_t + p_h + 15, text=f"{val:,.0f}", anchor=tk.N)

        # Ticks Y
        if use_log_scale:
            exp_start = math.floor(math.log10(min_y))
            exp_end = math.ceil(math.log10(max_y))
            for exp in range(exp_start, exp_end + 1):
                val = 10**exp
                if min_y <= val <= max_y:
                    py = map_y(val)
                    canvas.create_line(m_l - 5, py, m_l, py)
                    canvas.create_text(m_l - 10, py, text=f"1e{exp}", anchor=tk.E)
        else:
            for i in range(6):
                val = min_y + i * (max_y - min_y) / 5
                py = map_y(val)
                canvas.create_line(m_l - 5, py, m_l, py)
                canvas.create_text(m_l - 10, py, text=f"{val:,.2f}" if val < 10 else f"{val:,.0f}", anchor=tk.E)

    def log(self, mensaje: str):
        self.root.after(0, self._log_thread_safe, mensaje)
    
    def _log_thread_safe(self, mensaje: str):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.log_text.see(tk.END)

    def bloquear_controles(self, bloquear: bool):
        state = 'disabled' if bloquear else 'normal'
        self.btn_ejecutar_serie.config(state=state)
        self.btn_graficos.config(state=state if bloquear else 'normal') # Habilitar siempre al terminar
        self.btn_exportar.config(state=state if bloquear else ('normal' if any(a.resultados for a in self.algoritmos.values()) else 'disabled'))
        
        if not bloquear:
            self.progress['value'] = 0

    def limpiar_datos(self):
        if messagebox.askokcancel("Confirmar", "Esto borrará todos los datos de las experiencias acumuladas. ¿Desea continuar?"):
            for alg in self.algoritmos.values():
                alg.limpiar_datos()
            self.log("🧹 Datos de todas las experiencias limpiados.")
            self.bloquear_controles(False)

    def exportar_resultados(self):
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            for nombre, alg in self.algoritmos.items():
                if alg.resultados:
                    filename = f"resultados_{nombre.lower().replace(' ', '_')}_{timestamp}.csv"
                    msg = alg.exportar_csv(filename)
                    self.log(msg)
            messagebox.showinfo("Éxito", "Archivos CSV exportados correctamente.")
        except Exception as e:
            messagebox.showerror("Error de Exportación", str(e))
            self.log(f"❌ Error al exportar: {e}")

    def obtener_texto_complejidad(self) -> str:
        return """
ANÁLISIS DE COMPLEJIDAD TEMPORAL (PEOR CASO)

El análisis de complejidad nos permite predecir cómo crecerá el tiempo de ejecución de un algoritmo a medida que aumenta el tamaño de la entrada ('n'), sin depender de la velocidad del hardware.

• Ecuación de Tiempo: Representa el número de operaciones en función de 'n'.
• Notación Big O: Simplifica la ecuación al término dominante, describiendo el comportamiento asintótico.

----------------------------------------------------
🔹 BUBBLE SORT
----------------------------------------------------
• Ecuación (aproximada): T(n) = c₁n² + c₂n + c₃
  - Posee dos bucles anidados que recorren la entrada. El bucle interno realiza aproximadamente n, n-1, n-2, ... comparaciones.
  - La suma 1 + 2 + ... + (n-1) es igual a n(n-1)/2, lo que resulta en un término cuadrático (n²).
• Complejidad: O(n²) (Cuadrática)
  - El tiempo de ejecución crece proporcionalmente al cuadrado del tamaño de la entrada. Es ineficiente para grandes conjuntos de datos.

----------------------------------------------------
🔹 INSERTION SORT
----------------------------------------------------
• Ecuación (aproximada): T(n) = c₁n² + c₂n + c₃
  - En el peor caso (array en orden inverso), para cada elemento (bucle externo), debe compararse con todos los elementos ya ordenados a su izquierda (bucle interno).
  - Esto también resulta en una suma de serie aritmética, llevando a un comportamiento cuadrático.
• Complejidad: O(n²) (Cuadrática)
  - Similar a Bubble Sort en el peor caso, pero a menudo más rápido en la práctica para datos casi ordenados (mejor caso O(n)).

----------------------------------------------------
🔹 HEAP SORT
----------------------------------------------------
• Ecuación (aproximada): T(n) = c₁n·log(n) + c₂n
  - La construcción inicial del heap (heapify) toma tiempo O(n).
  - Luego, se realizan 'n' extracciones del elemento máximo. Cada extracción y posterior reordenamiento del heap (sift-down) toma O(log n) tiempo.
  - El total es n * O(log n), que domina sobre el O(n) inicial.
• Complejidad: O(n log n) (Log-lineal)
  - Mucho más escalable que los algoritmos cuadráticos. El tiempo de ejecución crece de manera muy controlada.

----------------------------------------------------
🔹 QUICK SORT
----------------------------------------------------
• Ecuación (peor caso): T(n) = T(n-1) + O(n)  =>  O(n²)
  - El peor caso ocurre cuando el pivote elegido es consistentemente el elemento más pequeño o más grande (ej. en un array ya ordenado).
  - Esto resulta en particiones desbalanceadas (una de tamaño n-1 y otra de 0), degradando el rendimiento a cuadrático.
• Ecuación (caso promedio): T(n) = 2T(n/2) + O(n)  =>  O(n log n)
  - En el caso promedio, el pivote divide el array en dos mitades aproximadamente iguales. El problema se divide recursivamente.
• Complejidad (Peor Caso): O(n²) (Cuadrática)
• Complejidad (Caso Promedio): O(n log n) (Log-lineal)
  - A pesar de su peor caso, en la práctica es a menudo el más rápido debido a constantes bajas y buen uso de la caché.
"""

def main():
    root = tk.Tk()
    app = AplicacionLaboratorio(root)
    root.mainloop()

if __name__ == "__main__":
    main()