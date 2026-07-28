"""Actividad formativa 3: implementación y evaluación de filtros digitales."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from filtros.filtros_fir import (
    aplicar_filtro_fir,
    disenar_fir_pasa_altos,
    disenar_fir_pasa_bajos,
    disenar_fir_pasa_bandas,
    respuesta_frecuencia_fir,
)
from filtros.filtros_iir import (
    aplicar_filtro_iir,
    disenar_iir_pasa_altos,
    disenar_iir_pasa_bajos,
    disenar_iir_pasa_bandas,
    respuesta_frecuencia_iir,
)
from utilidades.graficas import (
    graficar_comparacion_espectral,
    graficar_comparacion_temporal,
    graficar_espectro_entrada,
    graficar_respuesta_frecuencia,
    graficar_senal_entrada,
)
from utilidades.metricas import crear_registro_metricas, guardar_metricas_csv
from utilidades.senales import generar_senal_compuesta


FS = 2000.0
DURACION = 2.0
NUMTAPS_FIR = 101
ORDEN_IIR = 4
CORTE_PASA_BAJOS = 120.0
CORTE_PASA_ALTOS = 400.0
BANDA = (180.0, 320.0)


def construir_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera señales, aplica filtros FIR/IIR y guarda gráficas y métricas."
    )
    parser.add_argument(
        "--resultados",
        type=Path,
        default=Path(__file__).resolve().parent / "resultados",
        help="Carpeta de salida. Por defecto: ./resultados",
    )
    parser.add_argument(
        "--semilla",
        type=int,
        default=42,
        help="Semilla para reproducir el ruido blanco.",
    )
    return parser.parse_args()


def ejecutar(resultados: Path, semilla: int = 42) -> list[dict[str, str | float]]:
    """Ejecuta el experimento completo y devuelve las métricas calculadas."""
    resultados.mkdir(parents=True, exist_ok=True)

    datos = generar_senal_compuesta(
        fs=FS,
        duracion=DURACION,
        frecuencias=(50.0, 250.0, 700.0),
        amplitudes=(1.0, 0.7, 0.5),
        ruido_std=0.45,
        semilla=semilla,
    )

    graficar_senal_entrada(
        datos.tiempo,
        datos.limpia,
        datos.ruidosa,
        resultados / "señal_entrada.png",
    )
    graficar_espectro_entrada(
        datos.limpia,
        datos.ruidosa,
        FS,
        resultados / "espectro_entrada.png",
    )

    filtros = {
        "pasa_bajos": {
            "fir": disenar_fir_pasa_bajos(CORTE_PASA_BAJOS, FS, NUMTAPS_FIR),
            "iir": disenar_iir_pasa_bajos(CORTE_PASA_BAJOS, FS, ORDEN_IIR),
            "referencia": datos.componentes[50.0],
            "frecuencia_objetivo": 50.0,
            "no_deseadas": (250.0, 700.0),
            "titulo": "Filtro pasa bajos: conservación de 50 Hz",
        },
        "pasa_altos": {
            "fir": disenar_fir_pasa_altos(CORTE_PASA_ALTOS, FS, NUMTAPS_FIR),
            "iir": disenar_iir_pasa_altos(CORTE_PASA_ALTOS, FS, ORDEN_IIR),
            "referencia": datos.componentes[700.0],
            "frecuencia_objetivo": 700.0,
            "no_deseadas": (50.0, 250.0),
            "titulo": "Filtro pasa altos: conservación de 700 Hz",
        },
        "pasa_bandas": {
            "fir": disenar_fir_pasa_bandas(BANDA[0], BANDA[1], FS, NUMTAPS_FIR),
            "iir": disenar_iir_pasa_bandas(BANDA[0], BANDA[1], FS, ORDEN_IIR),
            "referencia": datos.componentes[250.0],
            "frecuencia_objetivo": 250.0,
            "no_deseadas": (50.0, 700.0),
            "titulo": "Filtro pasa bandas: conservación de 250 Hz",
        },
    }

    registros: list[dict[str, str | float]] = []

    for nombre, configuracion in filtros.items():
        salida_fir = aplicar_filtro_fir(configuracion["fir"], datos.ruidosa)
        salida_iir = aplicar_filtro_iir(configuracion["iir"], datos.ruidosa)

        graficar_comparacion_temporal(
            datos.tiempo,
            datos.ruidosa,
            salida_fir,
            salida_iir,
            configuracion["titulo"],
            resultados / f"{nombre}.png",
        )
        graficar_comparacion_espectral(
            datos.ruidosa,
            salida_fir,
            salida_iir,
            FS,
            f"Espectro después del {nombre.replace('_', ' ')}",
            resultados / f"espectro_{nombre}.png",
        )

        frecuencia_fir, respuesta_fir = respuesta_frecuencia_fir(
            configuracion["fir"], FS
        )
        frecuencia_iir, respuesta_iir = respuesta_frecuencia_iir(
            configuracion["iir"], FS
        )
        graficar_respuesta_frecuencia(
            frecuencia_fir,
            respuesta_fir,
            frecuencia_iir,
            respuesta_iir,
            f"Respuesta en frecuencia: {nombre.replace('_', ' ')}",
            resultados / f"respuesta_{nombre}.png",
        )

        registros.append(
            crear_registro_metricas(
                nombre,
                "FIR",
                configuracion["referencia"],
                salida_fir,
                FS,
                configuracion["frecuencia_objetivo"],
                configuracion["no_deseadas"],
            )
        )
        registros.append(
            crear_registro_metricas(
                nombre,
                "IIR Butterworth",
                configuracion["referencia"],
                salida_iir,
                FS,
                configuracion["frecuencia_objetivo"],
                configuracion["no_deseadas"],
            )
        )

    guardar_metricas_csv(registros, resultados / "metricas.csv")
    return registros


def imprimir_resumen(registros: list[dict[str, str | float]], resultados: Path) -> None:
    print("=" * 88)
    print("ACTIVIDAD FORMATIVA 3 - FILTROS DIGITALES")
    print("=" * 88)
    print(f"Frecuencia de muestreo: {FS:.0f} Hz")
    print("Señal: 50 Hz + 250 Hz + 700 Hz + ruido blanco")
    print(f"Resultados: {resultados.resolve()}")
    print("-" * 88)
    print(f"{'Filtro':<16} {'Tecnología':<18} {'MSE':>12} {'SNR [dB]':>12} {'Objetivo':>12} {'Residuo':>12}")
    print("-" * 88)
    for fila in registros:
        print(
            f"{str(fila['filtro']):<16} "
            f"{str(fila['tecnologia']):<18} "
            f"{float(fila['mse']):>12.6f} "
            f"{float(fila['snr_db']):>12.3f} "
            f"{float(fila['amplitud_objetivo']):>12.4f} "
            f"{float(fila['residuo_no_deseado']):>12.4f}"
        )
    print("=" * 88)
    print("Proceso terminado correctamente.")


def main() -> int:
    argumentos = construir_argumentos()
    try:
        registros = ejecutar(argumentos.resultados, argumentos.semilla)
        imprimir_resumen(registros, argumentos.resultados)
        return 0
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
