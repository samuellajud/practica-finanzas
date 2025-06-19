#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-

import sys
print("🧠 Ejecutando con:", sys.executable)

try:
    import yfinance as yf
except ImportError:
    print("⚠️ yfinance no está instalado. Algunos datos no podrán obtenerse.")
    yf = None  # Para permitir validación en tiempo de ejecución

import pytz
import datetime as dt
import pandas as pd
import numpy as np

# Configuración de zona horaria
zona_ar = pytz.timezone("America/Argentina/Buenos_Aires")

# Lista de índices a consultar
indices_yf = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW JONES": "^DJI",
    "FTSE 100": "^FTSE",
    "DAX": "^GDAXI",
    "CAC 40": "^FCHI",
    "NIKKEI 225": "^N225",
    "Bovespa": "^BVSP",
    "MERVAL": "^MERV"
}

# Función principal
def obtener_datos_indice(ticker, benchmark="^GSPC"):
    if yf is None:
        return None, None, None, None, None, None

    try:
        datos_indice = yf.Ticker(ticker).history(period="180d")
        datos_benchmark = yf.Ticker(benchmark).history(period="180d")

        if len(datos_indice) >= 90 and len(datos_benchmark) >= 90:
            ultimos = datos_indice.iloc[-2:]
            ayer = ultimos.iloc[0]
            hoy = ultimos.iloc[1]
            precio = hoy["Close"]
            variacion = ((hoy["Close"] - ayer["Close"]) / ayer["Close"]) * 100
            volumen = hoy["Volume"]

            # Cálculo de retornos
            retornos_indice = np.log(datos_indice["Close"] / datos_indice["Close"].shift(1)).dropna()
            retornos_benchmark = np.log(datos_benchmark["Close"] / datos_benchmark["Close"].shift(1)).dropna()

            df = pd.DataFrame({
                "indice": retornos_indice,
                "benchmark": retornos_benchmark
            }).dropna()

            def calcular_beta(df_tramo):
                cov = np.cov(df_tramo["indice"], df_tramo["benchmark"])[0][1]
                var = np.var(df_tramo["benchmark"])
                return round(cov / var, 3)

            beta_hist = calcular_beta(df)
            beta_mensual = calcular_beta(df.tail(30))
            beta_trimestral = calcular_beta(df.tail(90))

            return round(precio, 2), round(variacion, 2), int(volumen), beta_hist, beta_mensual, beta_trimestral

        else:
            print(f"⚠️ Datos insuficientes para {ticker}")
            return None, None, None, None, None, None

    except Exception as e:
        print(f"⚠️ Error en {ticker}: {e}")
        return None, None, None, None, None, None

# Generar Excel
def generar_excel_indices():
    fecha_hora = dt.datetime.now(zona_ar).strftime("%Y-%m-%d %H:%M")
    nombre_archivo = f"informe_indices_{dt.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

    data = {
        "Índice": [],
        "Ticker": [],
        "Precio Actual": [],
        "Variación %": [],
        "Volumen Operado": [],
        "Beta Histórica": [],
        "Beta Mensual (30d)": [],
        "Beta Trimestral (90d)": []
    }

    for nombre, ticker in indices_yf.items():
        resultado = obtener_datos_indice(ticker)
        if resultado is None or any(x is None for x in resultado):
            print(f"❌ Saltando {nombre} ({ticker}) por error o falta de datos.")
            continue

        precio, variacion, volumen, beta_hist, beta_mensual, beta_trimestral = resultado

        data["Índice"].append(nombre)
        data["Ticker"].append(ticker)
        data["Precio Actual"].append(precio)
        data["Variación %"].append(variacion)
        data["Volumen Operado"].append(volumen)
        data["Beta Histórica"].append(beta_hist)
        data["Beta Mensual (30d)"].append(beta_mensual)
        data["Beta Trimestral (90d)"].append(beta_trimestral)

    df = pd.DataFrame(data)
    df.to_excel(nombre_archivo, index=False)
    print(f"✅ Informe generado: {nombre_archivo}")

if __name__ == "__main__":
    generar_excel_indices()
