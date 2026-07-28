"""Funciones para crear y guardar las gráficas del proyecto."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike

from .senales import calcular_espectro


def _preparar_ruta(ruta: str | Path) -> Path:
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    return destino


def graficar_senal_entrada(
    tiempo: ArrayLike,
    limpia: ArrayLike,
    ruidosa: ArrayLike,
    ruta: str | Path,
    ventana_segundos: float = 0.10,
) -> Path:
    """Grafica un fragmento de la señal limpia y la señal con ruido."""
    t = np.asarray(tiempo)
    y_limpia = np.asarray(limpia)
    y_ruidosa = np.asarray(ruidosa)
    mascara = t <= ventana_segundos
    destino = _preparar_ruta(ruta)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(t[mascara], y_limpia[mascara], label="Señal limpia", linewidth=2)
    ax.plot(t[mascara], y_ruidosa[mascara], label="Señal con ruido", alpha=0.75)
    ax.set_title("Señal compuesta antes del filtrado")
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Amplitud")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(destino, dpi=160)
    plt.close(fig)
    return destino


def graficar_espectro_entrada(
    limpia: ArrayLike,
    ruidosa: ArrayLike,
    fs: float,
    ruta: str | Path,
) -> Path:
    """Compara los espectros de la señal limpia y la señal ruidosa."""
    f_limpia, a_limpia = calcular_espectro(limpia, fs)
    f_ruidosa, a_ruidosa = calcular_espectro(ruidosa, fs)
    destino = _preparar_ruta(ruta)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(f_limpia, a_limpia, label="Señal limpia", linewidth=2)
    ax.plot(f_ruidosa, a_ruidosa, label="Señal con ruido", alpha=0.75)
    ax.set_xlim(0, fs / 2)
    ax.set_title("Espectro de la señal de entrada")
    ax.set_xlabel("Frecuencia [Hz]")
    ax.set_ylabel("Amplitud")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(destino, dpi=160)
    plt.close(fig)
    return destino


def graficar_comparacion_temporal(
    tiempo: ArrayLike,
    entrada: ArrayLike,
    salida_fir: ArrayLike,
    salida_iir: ArrayLike,
    titulo: str,
    ruta: str | Path,
    ventana_segundos: float = 0.10,
) -> Path:
    """Compara entrada, salida FIR y salida IIR en el dominio del tiempo."""
    t = np.asarray(tiempo)
    mascara = t <= ventana_segundos
    destino = _preparar_ruta(ruta)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(t[mascara], np.asarray(entrada)[mascara], label="Entrada ruidosa", alpha=0.45)
    ax.plot(t[mascara], np.asarray(salida_fir)[mascara], label="Salida FIR", linewidth=2)
    ax.plot(t[mascara], np.asarray(salida_iir)[mascara], label="Salida IIR", linewidth=1.7)
    ax.set_title(titulo)
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Amplitud")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(destino, dpi=160)
    plt.close(fig)
    return destino


def graficar_comparacion_espectral(
    entrada: ArrayLike,
    salida_fir: ArrayLike,
    salida_iir: ArrayLike,
    fs: float,
    titulo: str,
    ruta: str | Path,
) -> Path:
    """Compara entrada, FIR e IIR en el dominio de la frecuencia."""
    f_entrada, a_entrada = calcular_espectro(entrada, fs)
    f_fir, a_fir = calcular_espectro(salida_fir, fs)
    f_iir, a_iir = calcular_espectro(salida_iir, fs)
    destino = _preparar_ruta(ruta)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(f_entrada, a_entrada, label="Entrada ruidosa", alpha=0.45)
    ax.plot(f_fir, a_fir, label="Salida FIR", linewidth=2)
    ax.plot(f_iir, a_iir, label="Salida IIR", linewidth=1.7)
    ax.set_xlim(0, fs / 2)
    ax.set_title(titulo)
    ax.set_xlabel("Frecuencia [Hz]")
    ax.set_ylabel("Amplitud")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(destino, dpi=160)
    plt.close(fig)
    return destino


def graficar_respuesta_frecuencia(
    frecuencias_fir: ArrayLike,
    respuesta_fir: ArrayLike,
    frecuencias_iir: ArrayLike,
    respuesta_iir: ArrayLike,
    titulo: str,
    ruta: str | Path,
) -> Path:
    """Compara en decibeles las respuestas en frecuencia FIR e IIR."""
    magnitud_fir = 20.0 * np.log10(np.maximum(np.abs(respuesta_fir), 1e-10))
    magnitud_iir = 20.0 * np.log10(np.maximum(np.abs(respuesta_iir), 1e-10))
    destino = _preparar_ruta(ruta)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(frecuencias_fir, magnitud_fir, label="FIR - ventana Hamming", linewidth=2)
    ax.plot(frecuencias_iir, magnitud_iir, label="IIR - Butterworth", linewidth=1.7)
    ax.set_ylim(-100, 5)
    ax.set_title(titulo)
    ax.set_xlabel("Frecuencia [Hz]")
    ax.set_ylabel("Magnitud [dB]")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(destino, dpi=160)
    plt.close(fig)
    return destino
