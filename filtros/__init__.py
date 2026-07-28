"""Funciones para diseñar y aplicar filtros digitales FIR e IIR."""

from .filtros_fir import (
    aplicar_filtro_fir,
    disenar_fir_pasa_altos,
    disenar_fir_pasa_bajos,
    disenar_fir_pasa_bandas,
    respuesta_frecuencia_fir,
)
from .filtros_iir import (
    aplicar_filtro_iir,
    disenar_iir_pasa_altos,
    disenar_iir_pasa_bajos,
    disenar_iir_pasa_bandas,
    respuesta_frecuencia_iir,
)

__all__ = [
    "aplicar_filtro_fir",
    "disenar_fir_pasa_altos",
    "disenar_fir_pasa_bajos",
    "disenar_fir_pasa_bandas",
    "respuesta_frecuencia_fir",
    "aplicar_filtro_iir",
    "disenar_iir_pasa_altos",
    "disenar_iir_pasa_bajos",
    "disenar_iir_pasa_bandas",
    "respuesta_frecuencia_iir",
]
