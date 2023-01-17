from fastapi import FastAPI
import py3langid as langid

app = FastAPI()

@app.get("/idioma/{texto}")
def buscar_idioma(texto: str):
    resultado = langid.classify(texto)[0]
    return {"idioma": resultado}


# langid viene pre-entrenado en 97 idiomas (en código ISO 639-1):
# af, am, an, ar, as, az, be, bg, bn, br, bs, ca, cs, cy, da, de, dz, el, en, eo, es, et, eu, fa, fi, fo, fr, ga, gl, gu, he, hi, hr, ht, hu, hy, id, is, it, ja, jv, ka, kk, 
# km, kn, ko, ku, ky, la, lb, lo, lt, lv, mg, mk, ml, mn, mr, ms, mt, nb, ne, nl, nn, no, oc, or, pa, pl, ps, pt, qu, ro, ru, rw, se, si, sk, sl, sq, sr, sv, sw, ta, te, th, 
# tl, tr, ug, uk, ur, vi, vo, wa, xh, zh, zu
