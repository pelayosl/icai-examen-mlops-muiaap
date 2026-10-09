from pathlib import Path
import joblib
from .contracts import Entrada, Salida
import pandas as pd
from pydantic import ValidationError


ENTRADA_COLUMNS = [
    "id_paquete",
    "peso_kg",
    "distancia_km"
]

OUTPUT_COLUMNS = [
    "id_paquete",
    "categoria",
    "confianza"
]

def leer_csv(ruta: Path) -> list[Entrada]:
    df = pd.read_csv(ruta)
    if df.empty:
        raise ValueError("El CSV no contiene filas de datos")

    entradas = []
    for i, row in df.iterrows():
        try:
            entrada = Entrada(**row.to_dict())
            entradas.append(entrada)
        except ValidationError as e:
            raise ValueError(e)
    return entradas


def preprocesar(entrada: Entrada) -> list[float]:
    peso_rounded = round(entrada.peso_kg, ndigits=1)
    return [peso_rounded, entrada.distancia_km]


def cargar_modelo(ruta: Path):
    model = joblib.load(ruta)
    return model


def predecir(entrada: Entrada, modelo) -> Salida:
    matriz = [preprocesar(entrada)]
    result_categoria = modelo.predict(matriz)[0]
    probabilidades = modelo.predict_proba(matriz)[0]
    return Salida(
        id_paquete=entrada.id_paquete,
        categoria=result_categoria,
        confianza=max(probabilidades)
    )


def guardar_csv(resultados: list[Salida], ruta: Path) -> None:
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", newline="", encoding="utf-8") as f:
            rows = [resultado.model_dump() for resultado in resultados]
            df = pd.DataFrame(rows, columns=OUTPUT_COLUMNS)
            df.to_csv(f, index=False)
    except ValueError as e:
        raise ValueError(f"Error saving to csv: {e}")


def ejecutar(entrada: Path, modelo: Path, salida: Path) -> None:
    entradas = leer_csv(entrada)
    model = cargar_modelo(modelo)
    salidas = [predecir(entrada, model) for entrada in entradas]

    guardar_csv(salidas, salida)
    print(f"El archivo se ha guardado correctamente en: {salida}")



if __name__ == "__main__":
    ejecutar(
        Path("data/raw/paquetes.csv"),
        Path("models/modelo.joblib"),
        Path("resultados.csv"),
    )
