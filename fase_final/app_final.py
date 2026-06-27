from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

print("ROOT =", ROOT)
print("Existe services:", (ROOT / "services").exists())
print(sys.path)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
print(ROOT)
print(sys.path)
import streamlit as st
from services.auth import supabase
from database.sheets import connect
from database.users import (
    get_user_by_email,
    create_user,
    update_last_activity
)

from datetime import datetime, timedelta

    
    

if "user" in st.session_state:

    last = st.session_state.get("last_activity")

    if last and datetime.now() - last > timedelta(minutes=30):

        st.session_state.clear()
        st.warning("Sesión expirada por inactividad")
        st.stop()

    st.session_state["last_activity"] = datetime.now()

st.title("LOGIN (Siempre iniciar sesión con el mismo correo)")

# --------------------
# CALLBACK OAUTH
# --------------------
params = st.query_params

if "code" in params:

    try:

        
        session = supabase.auth.exchange_code_for_session({
            "auth_code": params["code"]
        })

        st.session_state["session"] = session
        st.session_state["user"] = session.user
        st.session_state["last_activity"] = datetime.now()

        # -------------------------
        # Guardar en Google Sheets
        # -------------------------

        spreadsheet = connect()

        usuarios_sheet = spreadsheet.worksheet(
            "Usuarios_Final"
        )

        email = session.user.email

        nombre = session.user.user_metadata.get(
            "full_name",
            email
        )

        user_sheet = get_user_by_email(
            usuarios_sheet,
            email
        )

        if not user_sheet:

            create_user(
                usuarios_sheet,
                nombre,
                email
            )

        else:

            update_last_activity(
                usuarios_sheet,
                email
            )

    except Exception:
        pass

    st.query_params.clear()
    st.rerun()

# --------------------
# USER
# --------------------
user = st.session_state.get("user")

if user:

    st.success(
        f"Logueado: {user.email}"
    )

    st.stop()

# --------------------
# LOGIN
# --------------------
if st.button("Login con Google"):

    data = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to":
            "https://polla-mundialista-eicg-fase-final.streamlit.app"
        }
    })

    st.markdown(
        f"[Continuar con Google]({data.url})"
    )

st.title("📜 Reglas")

st.markdown("""
# ⚽ Reglas de la Polla Mundialista EICG 2026 - FASE FINAL

## 🎯 Objetivo

Cada participante deberá pronosticar:

- El campeón (se cierra el domingo 28/06/26 a la hora del comienzo del primer partido.
- El marcador de cada partido.
- Un jugador que marque al menos un gol durante el encuentro.

Los puntos obtenidos en cada partido se acumularán para conformar el ranking general.

---

## 🔒 Cierre de pronósticos

Los pronósticos podrán modificarse libremente hasta 1 minuto antes del inicio oficial de cada partido.

Una vez iniciado el encuentro, el pronóstico quedará bloqueado y no podrá ser modificado.

---

## 🏆 Sistema de puntuación

### 🏆 Campeón acertado

Si se acierta el campeón del mundial se le otrogarán 20 puntos

### ✅ Marcador exacto (durante los 90 minutos en caso de haber un ganador, o durante los 120 minutos en caso de haber tiempo extra)

Si se acierta exactamente el marcador del partido, se obtendrán:

**5 puntos**

Ejemplo:

- Resultado oficial: 2-1
- Pronóstico: 2-1

Puntaje: **5 puntos**

---

### ✅ Equipo Clasificado

Si no se acierta el marcador exacto, pero sí el equipo ganador, se obtendrán:

**3 puntos**

En caso de acertar un empate durante los 120 minutos se le otorgarán:
    
**3 puntos**

Ejemplos:

- Resultado oficial: 3-1
- Pronóstico: 1-0

Puntaje: **3 puntos**

---

- Resultado oficial: 1-1
- Pronóstico: 0-0

Puntaje: **3 puntos**

---

### ✅ Caso especial: Partido por el tercer lugar

En este caso no hay equipo clasificado, por lo cual se obtendrán los 5 puntos de marcador exacto o 3 puntos por resultado acertado: Ganador o empate.

### ⚽ Goleador del partido

Si se acierta cualquier jugador que haga al menos un gol en el encuentro, se obtendrá:

**1 punto adicional**

Este punto se suma a los puntos obtenidos por el resultado.

Ejemplo:

- Resultado oficial: 2-1
- Goleadores reales: Julián Álvarez, Lionel Messi
- Pronóstico: 2-1
- Goleador pronosticado: Julián Álvarez

Puntaje:

- Marcador exacto: 5 puntos
- Goleador: 1 punto

**Total: 6 puntos**

---

## ⚪ Partidos que terminan 0-0

En los empates 0-0 se considera acertado el "goleador inexistente".

Por tanto:

- Acertar exactamente el 0-0 otorga 5 puntos.
- Se suma 1 punto adicional correspondiente al goleador inexistente.

**Puntaje total: 6 puntos.**

---

## 📈 Ranking general

Los puntos obtenidos en todos los partidos se acumularán para conformar el ranking general de la competencia.

---

## 🔮 Transparencia

Todos los participantes podrán consultar los pronósticos realizados por los demás usuarios mediante la pestaña **Pronósticos**, garantizando la transparencia y el juego limpio.

---

## 🤝 Espíritu de la competencia

La finalidad principal de la Polla Mundialista EICG 2026 es fomentar la integración, la diversión y la sana competencia entre todos los participantes.
""")