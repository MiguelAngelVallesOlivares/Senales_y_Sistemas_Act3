"""Diseño y aplicación de filtros IIR Butterworth."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import signal


def _validar_parametros(fs: float, orden: int) -> None:
    if fs <= 0:
        raise ValueError("La frecuencia de muestreo debe ser mayor que cero.")
    if orden < 1:
        raise ValueError("El orden del filtro debe ser al menos 1.")


def disenar_iir_pasa_bajos(
    frecuencia_corte: float,
    fs: float,
    orden: int = 4,
) -> NDArray[np.float64]:
    """Diseña un IIR Butterworth pasa bajos en secciones de segundo orden."""
    _validar_parametros(fs, orden)
    if not 0 < frecuencia_corte < fs / 2:
        raise ValueError("La frecuencia de corte debe estar entre 0 y Nyquist.")

    return signal.butter(
        N=orden,
        Wn=frecuencia_corte,
        btype="lowpass",
        fs=fs,
        output="sos",
    )


def disenar_iir_pasa_altos(
    frecuencia_corte: float,
    fs: float,
    orden: int = 4,
) -> NDArray[np.float64]:
    """Diseña un IIR Butterworth pasa altos en secciones de segundo orden."""
    _validar_parametros(fs, orden)
    if not 0 < frecuencia_corte < fs / 2:
        raise ValueError("La frecuencia de corte debe estar entre 0 y Nyquist.")

    return signal.butter(
        N=orden,
        Wn=frecuencia_corte,
        btype="highpass",
        fs=fs,
        output="sos",
    )


def disenar_iir_pasa_bandas(
    frecuencia_baja: float,
    frecuencia_alta: float,
    fs: float,
    orden: int = 4,
) -> NDArray[np.float64]:
    """Diseña un IIR Butterworth pasa bandas en secciones de segundo orden."""
    _validar_parametros(fs, orden)
    if not 0 < frecuencia_baja < frecuencia_alta < fs / 2:
        raise ValueError(
            "Las frecuencias deben cumplir 0 < baja < alta < frecuencia de Nyquist."
        )

    return signal.butter(
        N=orden,
        Wn=[frecuencia_baja, frecuencia_alta],
        btype="bandpass",
        fs=fs,
        output="sos",
    )


def aplicar_filtro_iir(
    secciones: ArrayLike,
    senal_entrada: ArrayLike,
) -> NDArray[np.float64]:
    """Aplica el IIR con sosfiltfilt para evitar desfase y mejorar estabilidad."""
    sos = np.asarray(secciones, dtype=float)
    x = np.asarray(senal_entrada, dtype=float)

    if sos.ndim != 2 or sos.shape[1] != 6:
        raise ValueError("El filtro IIR debe estar en formato SOS con seis columnas.")
    if x.ndim != 1:
        raise ValueError("La señal debe ser un arreglo unidimensional.")

    return signal.sosfiltfilt(sos, x)


def respuesta_frecuencia_iir(
    secciones: ArrayLike,
    fs: float,
    puntos: int = 4096,
) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
    """Calcula la respuesta compleja en frecuencia de un filtro IIR SOS."""
    if fs <= 0:
        raise ValueError("La frecuencia de muestreo debe ser mayor que cero.")
    sos = np.asarray(secciones, dtype=float)
    frecuencias, respuesta = signal.sosfreqz(sos, worN=puntos, fs=fs)
    return frecuencias, respuesta
