"""Generación de señales sintéticas y cálculo de espectros."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class SenalCompuesta:
    """Contenedor inmutable para la señal limpia, ruidosa y sus componentes."""

    tiempo: NDArray[np.float64]
    limpia: NDArray[np.float64]
    ruidosa: NDArray[np.float64]
    componentes: dict[float, NDArray[np.float64]]
    fs: float


def generar_senal_compuesta(
    fs: float = 2000.0,
    duracion: float = 2.0,
    frecuencias: tuple[float, ...] = (50.0, 250.0, 700.0),
    amplitudes: tuple[float, ...] = (1.0, 0.7, 0.5),
    ruido_std: float = 0.45,
    semilla: int = 42,
) -> SenalCompuesta:
    """Genera una suma de senoidales y añade ruido blanco gaussiano."""
    if fs <= 0 or duracion <= 0:
        raise ValueError("fs y duración deben ser mayores que cero.")
    if len(frecuencias) != len(amplitudes) or not frecuencias:
        raise ValueError("Frecuencias y amplitudes deben tener la misma longitud.")
    if ruido_std < 0:
        raise ValueError("La desviación estándar del ruido no puede ser negativa.")
    if any(f <= 0 or f >= fs / 2 for f in frecuencias):
        raise ValueError("Cada frecuencia debe estar entre 0 y Nyquist.")

    muestras = int(round(fs * duracion))
    tiempo = np.arange(muestras, dtype=float) / fs

    componentes: dict[float, NDArray[np.float64]] = {}
    for frecuencia, amplitud in zip(frecuencias, amplitudes, strict=True):
        componentes[frecuencia] = amplitud * np.sin(2.0 * np.pi * frecuencia * tiempo)

    limpia = np.sum(np.stack(tuple(componentes.values())), axis=0)
    generador = np.random.default_rng(semilla)
    ruido = generador.normal(loc=0.0, scale=ruido_std, size=muestras)
    ruidosa = limpia + ruido

    return SenalCompuesta(
        tiempo=tiempo,
        limpia=limpia,
        ruidosa=ruidosa,
        componentes=componentes,
        fs=fs,
    )


def calcular_espectro(
    senal_entrada: ArrayLike,
    fs: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Calcula el espectro unilateral de amplitud usando una ventana Hann."""
    x = np.asarray(senal_entrada, dtype=float)
    if x.ndim != 1 or x.size < 2:
        raise ValueError("La señal debe ser un vector con al menos dos muestras.")
    if fs <= 0:
        raise ValueError("fs debe ser mayor que cero.")

    ventana = np.hanning(x.size)
    ganancia_coherente = ventana.mean()
    transformada = np.fft.rfft(x * ventana)
    frecuencias = np.fft.rfftfreq(x.size, d=1.0 / fs)
    amplitud = (2.0 / (x.size * ganancia_coherente)) * np.abs(transformada)
    amplitud[0] /= 2.0
    if x.size % 2 == 0:
        amplitud[-1] /= 2.0
    return frecuencias, amplitud
