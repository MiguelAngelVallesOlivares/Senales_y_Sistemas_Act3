"""Diseño y aplicación de filtros FIR mediante ventana de Hamming."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import signal


def _validar_fs(fs: float) -> None:
    if fs <= 0:
        raise ValueError("La frecuencia de muestreo debe ser mayor que cero.")


def _validar_numtaps(numtaps: int) -> None:
    if numtaps < 3:
        raise ValueError("numtaps debe ser al menos 3.")
    if numtaps % 2 == 0:
        raise ValueError("Use un número impar de coeficientes FIR para este proyecto.")


def disenar_fir_pasa_bajos(
    frecuencia_corte: float,
    fs: float,
    numtaps: int = 101,
) -> NDArray[np.float64]:
    """Diseña un filtro FIR pasa bajos con ventana de Hamming."""
    _validar_fs(fs)
    _validar_numtaps(numtaps)
    if not 0 < frecuencia_corte < fs / 2:
        raise ValueError("La frecuencia de corte debe estar entre 0 y Nyquist.")

    return signal.firwin(
        numtaps=numtaps,
        cutoff=frecuencia_corte,
        window="hamming",
        pass_zero="lowpass",
        fs=fs,
    )


def disenar_fir_pasa_altos(
    frecuencia_corte: float,
    fs: float,
    numtaps: int = 101,
) -> NDArray[np.float64]:
    """Diseña un filtro FIR pasa altos con ventana de Hamming."""
    _validar_fs(fs)
    _validar_numtaps(numtaps)
    if not 0 < frecuencia_corte < fs / 2:
        raise ValueError("La frecuencia de corte debe estar entre 0 y Nyquist.")

    return signal.firwin(
        numtaps=numtaps,
        cutoff=frecuencia_corte,
        window="hamming",
        pass_zero="highpass",
        fs=fs,
    )


def disenar_fir_pasa_bandas(
    frecuencia_baja: float,
    frecuencia_alta: float,
    fs: float,
    numtaps: int = 101,
) -> NDArray[np.float64]:
    """Diseña un filtro FIR pasa bandas con ventana de Hamming."""
    _validar_fs(fs)
    _validar_numtaps(numtaps)
    if not 0 < frecuencia_baja < frecuencia_alta < fs / 2:
        raise ValueError(
            "Las frecuencias deben cumplir 0 < baja < alta < frecuencia de Nyquist."
        )

    return signal.firwin(
        numtaps=numtaps,
        cutoff=[frecuencia_baja, frecuencia_alta],
        window="hamming",
        pass_zero="bandpass",
        fs=fs,
    )


def aplicar_filtro_fir(
    coeficientes: ArrayLike,
    senal_entrada: ArrayLike,
) -> NDArray[np.float64]:
    """Aplica un FIR con filtrado hacia adelante y atrás para evitar desfase."""
    b = np.asarray(coeficientes, dtype=float)
    x = np.asarray(senal_entrada, dtype=float)

    if b.ndim != 1 or x.ndim != 1:
        raise ValueError("Los coeficientes y la señal deben ser arreglos unidimensionales.")
    if x.size <= 3 * (b.size - 1):
        raise ValueError("La señal es demasiado corta para aplicar filtfilt con este FIR.")

    return signal.filtfilt(b, [1.0], x)


def respuesta_frecuencia_fir(
    coeficientes: ArrayLike,
    fs: float,
    puntos: int = 4096,
) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
    """Calcula la respuesta compleja en frecuencia de un filtro FIR."""
    _validar_fs(fs)
    b = np.asarray(coeficientes, dtype=float)
    frecuencias, respuesta = signal.freqz(b, worN=puntos, fs=fs)
    return frecuencias, respuesta
