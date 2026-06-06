import streamlit as st

st.title("📜 Reglas")

st.markdown("""
# ⚽ Reglas de la Polla Mundialista EICG 2026

## 🎯 Objetivo

Cada participante deberá pronosticar:

- El marcador del partido.
- El goleador del encuentro.

Los puntos obtenidos en cada partido se acumularán para conformar el ranking general.

---

## 🔒 Cierre de pronósticos

Los pronósticos podrán modificarse libremente hasta 10 minutos antes del inicio oficial de cada partido.

Una vez iniciado el encuentro, el pronóstico quedará bloqueado y no podrá ser modificado.

---

## 🏆 Sistema de puntuación

### ✅ Marcador exacto

Si se acierta exactamente el marcador del partido, se obtendrán:

**5 puntos**

Ejemplo:

- Resultado oficial: 2-1
- Pronóstico: 2-1

Puntaje: **5 puntos**

---

### ✅ Ganador o empate

Si no se acierta el marcador exacto, pero sí el resultado del partido (victoria local, empate o victoria visitante), se obtendrán:

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

### ⚽ Goleador del partido

Si se acierta el goleador del encuentro, se obtendrá:

**1 punto adicional**

Este punto se suma a los puntos obtenidos por el resultado.

Ejemplo:

- Resultado oficial: 2-1
- Goleador real: Julián Álvarez
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