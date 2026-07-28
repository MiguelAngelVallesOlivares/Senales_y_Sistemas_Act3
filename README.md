# Actividad formativa 3: Implementación y evaluación de filtros digitales

Proyecto de **Señales y Sistemas** desarrollado en Python para diseñar, aplicar y comparar filtros digitales:

- FIR con ventana de Hamming.
- IIR Butterworth.
- Pasa bajos.
- Pasa altos.
- Pasa bandas.

El programa genera una señal compuesta por frecuencias de **50 Hz**, **250 Hz** y **700 Hz**, añade ruido blanco y evalúa qué tan bien recupera cada filtro la componente deseada.

## Requisitos

- Python 3.10 o superior.
- `numpy`.
- `scipy`.
- `matplotlib`.

## Estructura

```text
actividad_filtros_digitales/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── filtros/
│   ├── __init__.py
│   ├── filtros_fir.py
│   └── filtros_iir.py
│
├── utilidades/
│   ├── __init__.py
│   ├── senales.py
│   ├── graficas.py
│   └── metricas.py
│
└── resultados/
    ├── señal_entrada.png
    ├── espectro_entrada.png
    ├── pasa_bajos.png
    ├── pasa_altos.png
    ├── pasa_bandas.png
    ├── espectro_pasa_bajos.png
    ├── espectro_pasa_altos.png
    ├── espectro_pasa_bandas.png
    ├── respuesta_pasa_bajos.png
    ├── respuesta_pasa_altos.png
    ├── respuesta_pasa_bandas.png
    └── metricas.csv
```

## Preparación en Windows PowerShell

Desde la carpeta del proyecto:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Si PowerShell bloquea temporalmente la activación del entorno virtual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

También puede ejecutarse sin activar el entorno:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Ejecución

```powershell
python main.py
```

Para cambiar la carpeta de resultados:

```powershell
python main.py --resultados .\mis_resultados
```

Para usar otra semilla de ruido:

```powershell
python main.py --semilla 100
```

## Diseño del experimento

| Parámetro | Valor |
|---|---:|
| Frecuencia de muestreo | 2000 Hz |
| Duración | 2 s |
| Componentes de la señal | 50, 250 y 700 Hz |
| Desviación estándar del ruido | 0.45 |
| FIR | 101 coeficientes, ventana Hamming |
| IIR | Butterworth de orden 4 |
| Corte pasa bajos | 120 Hz |
| Corte pasa altos | 400 Hz |
| Banda de paso | 180 a 320 Hz |

La frecuencia de Nyquist es de **1000 Hz**, por lo que todas las componentes elegidas pueden representarse sin aliasing.

## Resultados esperados

- El filtro pasa bajos conserva principalmente la componente de 50 Hz.
- El filtro pasa altos conserva principalmente la componente de 700 Hz.
- El filtro pasa bandas conserva principalmente la componente de 250 Hz.
- Los filtros FIR requieren más coeficientes, pero ofrecen una respuesta de fase más controlable.
- Los filtros IIR logran transiciones eficientes con un orden menor.

El programa usa `filtfilt` y `sosfiltfilt` para aplicar filtrado de fase cero. Esto facilita la comparación temporal porque evita un desplazamiento apreciable entre la referencia y la salida.

## Métricas

El archivo `resultados/metricas.csv` contiene:

- **MSE:** error cuadrático medio respecto a la componente ideal.
- **SNR:** relación señal-ruido de la salida respecto a la referencia.
- **Amplitud objetivo:** amplitud conservada en la frecuencia deseada.
- **Residuo no deseado:** suma de amplitudes restantes en las otras dos frecuencias principales.

Un MSE menor, un SNR mayor y un residuo menor indican un mejor resultado.



## Archivos principales

- `main.py`: coordina todo el experimento.
- `filtros/filtros_fir.py`: diseño y aplicación de filtros FIR.
- `filtros/filtros_iir.py`: diseño y aplicación de filtros IIR Butterworth.
- `utilidades/senales.py`: generación de señales y espectros.
- `utilidades/graficas.py`: creación de gráficas.
- `utilidades/metricas.py`: evaluación cuantitativa y exportación CSV.
