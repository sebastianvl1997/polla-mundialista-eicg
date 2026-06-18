from collections import defaultdict


def obtener_resultado_partido(gl, gv):
    """
    Retorna:
    L = gana local
    V = gana visitante
    E = empate
    """
    if gl > gv:
        return "L"
    elif gv > gl:
        return "V"
    return "E"


def calcular_puntos_pronostico(pronostico, resultado):
    """
    pronostico: dict
    resultado: dict
    """

    puntos = 0

    p_gl = int(pronostico["goles_local"])
    p_gv = int(pronostico["goles_visitante"])

    r_gl = int(resultado["goles_local"])
    r_gv = int(resultado["goles_visitante"])

    # Marcador exacto
    if p_gl == r_gl and p_gv == r_gv:
        puntos = 5

    else:
        p_res = obtener_resultado_partido(p_gl, p_gv)
        r_res = obtener_resultado_partido(r_gl, r_gv)

        if p_res == r_res:
            puntos = 3

    # Goleador
    # Caso especial: empate 0-0
# Caso especial: empate 0-0
    if r_gl == 0 and r_gv == 0 and p_gl == 0 and p_gv == 0:
        puntos += 1
    
    else:
    
        goleador_pron = str(
            pronostico.get("goleador", "")
        ).strip()
    
        goleador_real = str(
            resultado.get("goleador_final", "")
        ).strip()
    
        goleador_pron = str(
            pronostico.get("goleador", "")
        ).strip().lower()
        
        goleadores_reales = [
        
            x.strip().lower()
        
            for x in str(
                resultado.get(
                    "goleador_final",
                    ""
                )
            ).split(";")
        
            if x.strip()
        ]
        
        if (
            goleador_pron
            and goleador_pron in goleadores_reales
        ):
            puntos += 1

    return puntos


def evaluar_pronostico(pronostico, resultado):

    p_gl = int(pronostico["goles_local"])
    p_gv = int(pronostico["goles_visitante"])

    r_gl = int(resultado["goles_local"])
    r_gv = int(resultado["goles_visitante"])

    exacto = False
    resultado_correcto = False
    goleador_correcto = False

    puntos = 0

    if p_gl == r_gl and p_gv == r_gv:

        exacto = True
        puntos = 5

    else:

        p_res = obtener_resultado_partido(
            p_gl,
            p_gv
        )

        r_res = obtener_resultado_partido(
            r_gl,
            r_gv
        )

        if p_res == r_res:

            resultado_correcto = True
            puntos = 3

    # Caso especial: empate 0-0
    if r_gl == 0 and r_gv == 0 and p_gl == 0 and p_gv == 0:
        
        goleador_correcto = True
        puntos += 1
        
    else:
        
        goleador_pron = str(
            pronostico.get("goleador", "")
        ).strip()
        
        goleador_real = str(
            resultado.get("goleador_final", "")
        ).strip()
        
        goleador_pron = str(
            pronostico.get("goleador", "")
        ).strip().lower()
        
        goleadores_reales = [
        
            x.strip().lower()
        
            for x in str(
                resultado.get(
                    "goleador_final",
                    ""
                )
            ).split(";")
        
            if x.strip()
        ]
        
        if (
            goleador_pron
            and goleador_pron in goleadores_reales
        ):
            goleador_correcto = True
            puntos += 1

    return {
        "puntos": puntos,
        "exacto": exacto,
        "resultado": resultado_correcto,
        "goleador": goleador_correcto
    }

def calcular_ranking(pronosticos, resultados):
    """
    pronosticos: lista de dicts
    resultados: lista de dicts
    """

    resultados_map = {
        str(r["partido_id"]): r
        for r in resultados
    }

    ranking = defaultdict(
        lambda: {
            "puntos": 0,
            "exactos": 0,
            "resultados": 0,
            "goleadores": 0
        }
    )

    for pron in pronosticos:

        partido_id = str(pron["partido_id"])

        if partido_id not in resultados_map:
            continue

        user_id = str(pron["user_id"])

        evaluacion = evaluar_pronostico(
            pron,
            resultados_map[partido_id]
        )

        ranking[user_id]["puntos"] += evaluacion["puntos"]

        if evaluacion["exacto"]:
            ranking[user_id]["exactos"] += 1

        if evaluacion["resultado"]:
            ranking[user_id]["resultados"] += 1

        if evaluacion["goleador"]:
            ranking[user_id]["goleadores"] += 1

    ranking_final = []

    for user_id, datos in ranking.items():

        ranking_final.append(
            {
                "user_id": user_id,
                "puntos": datos["puntos"],
                "exactos": datos["exactos"],
                "resultados": datos["resultados"],
                "goleadores": datos["goleadores"]
            }
        )

    ranking_final.sort(
        key=lambda x: (
            x["puntos"],
            x["exactos"],
            x["resultados"],
            x["goleadores"]
        ),
        reverse=True
    )

    return ranking_final