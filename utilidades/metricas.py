"""Métricas cuantitativas para evaluar el resultado de los filtros."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from numpy.typing import ArrayLike

from .senales import calcular_espectro


def error_cuadratico_medio(referencia: ArrayLike, estimada: ArrayLike) -> float:
    """Calcula el error cuadrático medio entre dos señales."""
    ref = np.asarray(referencia, dtype=float)
    est = np.asarray(estimada, dtype=float)
    if ref.shape != est.shape:
        raise ValueError("Las señales deben tener la misma forma.")
    return float(np.mean(np.square(ref - est)))


def snr_db(referencia: ArrayLike, estimada: ArrayLike) -> float:
    """Calcula la relación señal-ruido usando la referencia como señal ideal."""
    ref = np.asarray(referencia, dtype=float)
    est = np.asarray(estimada, dtype=float)
    if ref.shape != est.shape:
        raise ValueError("Las señales deben tener la misma forma.")

    potencia_senal = np.mean(np.square(ref))
    potencia_error = np.mean(np.square(ref - est))
    if potencia_error == 0:
        return float("inf")
    if potencia_senal == 0:
        return float("-inf")
    return float(10.0 * np.log10(potencia_senal / potencia_error))


def amplitud_en_frecuencia(senal_entrada: ArrayLike, fs: float, frecuencia: float) -> float:
    """Obtiene la amplitud del bin espectral más cercano a una frecuencia dada."""
    frecuencias, amplitudes = calcular_espectro(senal_entrada, fs)
    indice = int(np.argmin(np.abs(frecuencias - frecuencia)))
    return float(amplitudes[indice])


def crear_registro_metricas(
    nombre_filtro: str,
    tecnologia: str,
    referencia: ArrayLike,
    salida: ArrayLike,
    fs: float,
    frecuencia_objetivo: float,
    frecuencias_no_deseadas: tuple[float, ...],
) -> dict[str, str | float]:
    """Construye una fila de métricas lista para impresión o exportación CSV."""
    amplitud_objetivo = amplitud_en_frecuencia(salida, fs, frecuencia_objetivo)
    amplitud_residual = sum(
        amplitud_en_frecuencia(salida, fs, frecuencia)
        for frecuencia in frecuencias_no_deseadas
    )

    return {
        "filtro": nombre_filtro,
        "tecnologia": tecnologia,
        "mse": error_cuadratico_medio(referencia, salida),
        "snr_db": snr_db(referencia, salida),
        "amplitud_objetivo": amplitud_objetivo,
        "residuo_no_deseado": amplitud_residual,
    }


def guardar_metricas_csv(
    registros: list[dict[str, str | float]],
    ruta: str | Path,
) -> Path:
    """Guarda las métricas en formato CSV."""
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    campos = [
        "filtro",
        "tecnologia",
        "mse",
        "snr_db",
        "amplitud_objetivo",
        "residuo_no_deseado",
    ]

    with destino.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)

    return destino
