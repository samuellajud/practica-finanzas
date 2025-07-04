import sys
print("🧠 Ejecutando con:", sys.executable)


import os
import pytz
import datetime as dt
import pandas as pd
import numpy as np 
import yfinance as yf  
# Configuración
zona_ar = pytz.timezone("America/Argentina/Buenos_Aires")

# Tickers de los principales índices bursátiles en Yahoo Finance
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

# Obtener datos de cada índice
def obtener_datos_indice(ticker, benchmark="^GSPC"):
    try:
        # Obtener 180 días de datos para cubrir todo (trimestral y más)
        datos_indice = yf.Ticker(ticker).history(period="180d")
        datos_benchmark = yf.Ticker(benchmark).history(period="180d")

        if len(datos_indice) >= 90 and len(datos_benchmark) >= 90:
            # Últimos 2 días para precio y variación
            ultimos = datos_indice.iloc[-2:]
            ayer = ultimos.iloc[0]
            hoy = ultimos.iloc[1]
            precio = hoy["Close"]
            variacion = ((hoy["Close"] - ayer["Close"]) / ayer["Close"]) * 100
            volumen = hoy["Volume"]
            
            # Calcular retornos logarítmicos diarios
            retornos_indice = np.log(datos_indice["Close"] / datos_indice["Close"].shift(1)).dropna()
            retornos_benchmark = np.log(datos_benchmark["Close"] / datos_benchmark["Close"].shift(1)).dropna()
           
            # Crear dataframe alineado por fecha
            df = pd.DataFrame({
                "indice": retornos_indice,
                "benchmark": retornos_benchmark
            }).dropna()
           
            # Función auxiliar para calcular Beta de un tramo
            def calcular_beta(df_tramo):
                cov = np.cov(df_tramo["indice"], df_tramo["benchmark"])[0][1]
                var = np.var(df_tramo["benchmark"])
                return round(cov / var, 3)
           
           
             # Históricos completos
             
            beta_hist = calcular_beta(df)

             # Últimos 30 días (mensual)
             
            beta_mensual = calcular_beta(df[-30:])

             # Últimos 90 días (trimestral)
             
            beta_trimestral = calcular_beta(df[-90:])

    except Exception as e:
     print(f"⚠️ Error en {ticker}: {e}")
     return None, None, None, None, None, None

# Crear archivo Excel
def generar_excel_indices():
    fecha_hora = dt.datetime.now(zona_ar).strftime("%Y-%m-%d %H:%M")
    nombre_archivo = f"informe_indices_{dt.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

    # Preparar estructura de datos
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
        precio, variacion, volumen, beta_hist, beta_mensual, beta_trimestral = obtener_datos_indice(ticker)


        data["Índice"].append(nombre)
        data["Ticker"].append(ticker)
        data["Precio Actual"].append(precio)
        data["Variación %"].append(variacion)
        data["Volumen Operado"].append(volumen)
        data["Beta Histórica"].append(beta_hist)
        data["Beta Mensual (30d)"].append(beta_mensual)
        data["Beta Trimestral (90d)"].append(beta_trimestral)

    # Crear DataFrame y exportar a Excel
    df = pd.DataFrame(data)
    df.to_excel(nombre_archivo, index=False)
    print(f"✅ Informe Excel generado: {nombre_archivo}")

if __name__ == "__main__":
    generar_excel_indices()
