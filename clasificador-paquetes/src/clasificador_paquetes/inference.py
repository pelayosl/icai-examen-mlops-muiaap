import csv
from pathlib import Path
import joblib
from .contracts import Entrada, Salida


def leer_csv(ruta: Path) -> list[Entrada]:
    # TODO
    raise NotImplementedError


def preprocesar(entrada: Entrada) -> list[float]:
    # TODO
    raise NotImplementedError


def cargar_modelo(ruta: Path):
    # TODO
    raise NotImplementedError


def predecir(entrada: Entrada, modelo) -> Salida:
    # TODO
    raise NotImplementedError


def guardar_csv(resultados: list[Salida], ruta: Path) -> None:
    # TODO
    raise NotImplementedError


def ejecutar(entrada: Path, modelo: Path, salida: Path) -> None:
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    ejecutar(
        Path("data/raw/paquetes.csv"),
        Path("models/modelo.joblib"),
        Path("resultados.csv"),
    )
