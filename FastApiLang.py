from fastapi import FastAPI
from pydantic import BaseModel, Field
import py3langid as langid
import python_weather
import pyjokes
import wikipedia

app = FastAPI()

@app.get("/")
def indice():
    return {
        "saludo": "Esta es una Api donde se encontraran varios servicios",
        "servicio-1": "Es un servicio que permite saber en que idioma esta una frase, admite hasta 97 idiomas en código ISO 639-1, se accede por GET en /idioma/<texto>",
        "servicio-2": "Da la información del clima de una ciudad, se accede mediante GET en /clima/<ciudad>",
        "servicio-3": "Devuelve bromas (chistes), funciona mediante GET y recibe el idioma en ISO 639-1, /bromas/<idioma>",
        "servicio-4": "Busqueda en wikipedia mediante POST, recibe 2 parametros, el idioma (ISO 639-1) y lo que se va a buscar, /wikipedia/",
        "documentación": "Se accede mediante /docs o /redocs"
    }

@app.get("/idioma/{texto}")
def buscar_idioma(texto: str):
    resultado = langid.classify(texto)[0]
    return {"idioma": resultado}

# langid viene pre-entrenado en 97 idiomas (en código ISO 639-1):
# af, am, an, ar, as, az, be, bg, bn, br, bs, ca, cs, cy, da, de, dz, el, en, eo, es, et, eu, fa, fi, fo, fr, ga, gl, gu, he, hi, hr, ht, hu, hy, id, is, it, ja, jv, ka, kk, 
# km, kn, ko, ku, ky, la, lb, lo, lt, lv, mg, mk, ml, mn, mr, ms, mt, nb, ne, nl, nn, no, oc, or, pa, pl, ps, pt, qu, ro, ru, rw, se, si, sk, sl, sq, sr, sv, sw, ta, te, th, 
# tl, tr, ug, uk, ur, vi, vo, wa, xh, zh, zu

@app.get("/clima/{ciudad}") #brinda información del clima de la ciudad dada
async def clima_ciudad(ciudad):
    iniciar = python_weather.Client(format=python_weather.METRIC)
    clima = await iniciar.get(ciudad)
    for forecast in clima.forecasts:
        return {
            "fecha": forecast.date,
            "temperatura": forecast.temperature,
            "temperatura minima": forecast.lowest_temperature,
            "temperatura maxima": forecast.highest_temperature,
            "temperatura-actual": clima.current.temperature,
            "indice UV": forecast.uv_index,
            "rayos de sol": forecast.sun_shines
        }
    await iniciar.close()

@app.get("/bromas/{idioma}") #genera bromas (chistes) al azar, según el idioma indicado (idiomas soportados: en, de, es, gl, eus)
def generar_broma(idioma: str):
    broma = pyjokes.get_joke(language= idioma)
    return {"broma": broma}

class ItemsWikipedia(BaseModel): #clase para validar datos y agregar ejemplo a la documentación
    idioma: str = Field(example= "es")
    busqueda: str = Field(example= "Python")

@app.post("/wikipedia/")
async def buscar_wikipedia(ItemWiki: ItemsWikipedia):
    wikipedia.set_lang(ItemWiki.idioma)
    buscar = wikipedia.summary(ItemWiki.busqueda, sentences=2)
    return {"busqueda": buscar}
