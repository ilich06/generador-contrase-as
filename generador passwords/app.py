import re
import secrets
import string
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="KeyShield - Generador y Evaluador",
    page_icon="🛡️",
    layout="centered",
)

# Estilo personalizado sutil
st.markdown(
    """
    <style>
    .stButton button {
        width: 100%;
        border-radius: 10px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- 1. LÓGICA CRIPTOGRÁFICA (PYTHON PURO) ---
def generar_3_sugerencias(base: str) -> list[dict]:
    palabra = "".join(ch for ch in base if ch.isalnum()) or "Seguridad"
    simbolos = "!@#$%&*_-+="
    digitos = string.digits
    letras = string.ascii_letters

    # Variante 1: LeetSpeak
    leet_map = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$", "t": "7"}
    leet = "".join(leet_map.get(ch.lower(), ch) for ch in palabra)
    sufijo = "".join(secrets.choice(digitos) for _ in range(2)) + secrets.choice(
        simbolos
    )
    op1 = leet.capitalize() + sufijo
    while len(op1) < 13:
        op1 += secrets.choice(letras + simbolos)

    # Variante 2: Passphrase / Bloques
    sep = secrets.choice(["-", "_", ".", "#"])
    bloque = "".join(secrets.choice(letras) for _ in range(4))
    num = secrets.choice(range(100, 999))
    op2 = f"{palabra.capitalize()}{sep}{bloque}{sep}{num}{secrets.choice(simbolos)}"

    # Variante 3: Híbrida / Entrelazada de alta entropía
    azar = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(digitos),
        secrets.choice(simbolos),
        secrets.choice(digitos),
        secrets.choice(simbolos),
    ]
    secrets.SystemRandom().shuffle(azar)
    op3 = f"{palabra[:3].upper()}_{''.join(azar)}_{palabra[3:].lower()}"
    while len(op3) < 15:
        op3 += secrets.choice(letras + digitos)

    return [
        {"pwd": op1, "tipo": "LeetSpeak (Transformación)"},
        {"pwd": op2, "tipo": "Passphrase (Bloques con separador)"},
        {"pwd": op3, "tipo": "Híbrida (Alta entropía)"},
    ]


def evaluar_clave(pwd: str) -> dict:
    return {
        "len": len(pwd) >= 12,
        "upper": bool(re.search(r"[A-Z]", pwd)),
        "lower": bool(re.search(r"[a-z]", pwd)),
        "digit": bool(re.search(r"[0-9]", pwd)),
        "symbol": bool(re.search(r"[^A-Za-z0-9]", pwd)),
    }


# --- CABECERA ---
st.title("Generador de Contraseñas Seguras")
st.divider()

# --- SECCIÓN 1: GENERADOR ---
st.subheader("Genera una contraseña desde una palabra base")

col_input, col_btn = st.columns([3, 1])
with col_input:
    palabra_base = st.text_input(
        "Palabra o tema base:", value="Seguridad", label_visibility="collapsed"
    )
with col_btn:
    generar = st.button("Generar", type="primary")

sugerencias = generar_3_sugerencias(palabra_base)

st.write("##### Sugerencias seguras:")

for item in sugerencias:
    st.code(item["pwd"], language="text")
    st.caption(f"Estilo: {item['tipo']}")

st.divider()

# --- SECCIÓN 2: EVALUADOR EN VIVO ---
st.subheader("Evalúa la contraseña")

pwd_input = st.text_input(
    "Escribe o pega una contraseña para analizar:",
    placeholder="Introduce tu clave aquí...",
)

checks = evaluar_clave(pwd_input)
puntuacion = sum(checks.values())

# Nivel de seguridad
niveles = {
    0: ("Muy Débil", 0.0),
    1: ("Muy Débil", 0.2),
    2: ("Débil", 0.4),
    3: ("Aceptable", 0.6),
    4: ("Buena", 0.8),
    5: ("Excelente (Muy Segura)", 1.0),
}
nivel_txt, progreso_val = niveles[puntuacion] if pwd_input else ("Vacía", 0.0)

st.progress(progreso_val)
st.metric(
    label="Nivel de Fortaleza",
    value=nivel_txt,
    delta=f"{puntuacion}/5 requisitos",
)

# Requisitos en vivo
st.write("##### Criterios de seguridad:")
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.write(
        f"{'✅' if checks['len'] else '❌'} Longitud mínima de 12 caracteres"
    )
    st.write(f"{'✅' if checks['upper'] else '❌'} Al menos una mayúscula (A-Z)")
    st.write(f"{'✅' if checks['lower'] else '❌'} Al menos una minúscula (a-z)")

with col_c2:
    st.write(f"{'✅' if checks['digit'] else '❌'} Al menos un número (0-9)")
    st.write(
        f"{'✅' if checks['symbol'] else '❌'} Al menos un carácter especial (!@#$...)"
    )