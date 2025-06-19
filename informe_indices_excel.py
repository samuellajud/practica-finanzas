
import os
import pytz
import datetime as dt
import yfinance as yf
import pandas as pd

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
def obtener_datos_indice(ticker):
    try:
        datos = yf.Ticker(ticker).history(period="2d")
        if len(datos) >= 2:
            ayer = datos.iloc[-2]
            hoy = datos.iloc[-1]
            precio = hoy["Close"]
            variacion = ((hoy["Close"] - ayer["Close"]) / ayer["Close"]) * 100
            volumen = hoy["Volume"]
            return round(precio, 2), round(variacion, 2), int(volumen)
    except:
        return None, None, None

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
        "Volumen Operado": []
    }

    for nombre, ticker in indices_yf.items():
        precio, variacion, volumen = obtener_datos_indice(ticker)
        data["Índice"].append(nombre)
        data["Ticker"].append(ticker)
        data["Precio Actual"].append(precio)
        data["Variación %"].append(variacion)
        data["Volumen Operado"].append(volumen)

    # Crear DataFrame y exportar a Excel
    df = pd.DataFrame(data)
    df.to_excel(nombre_archivo, index=False)
    print(f"✅ Informe Excel generado: {nombre_archivo}")

if __name__ == "__main__":
    generar_excel_indices()
