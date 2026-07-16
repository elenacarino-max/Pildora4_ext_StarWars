from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).resolve().parents[1]


def _asset_data(name: str) -> str:
    path = APP_DIR / "assets" / name
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def apply_theme() -> None:
    hero = _asset_data("hero-library.png")
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
        :root {{ --void:#050913; --panel:#0c1826; --cyan:#58d8e8; --gold:#e7bd64; --red:#e2715b; --ink:#eaf7f8; --muted:#9bb1bd; }}
        .stApp {{
          background:
            radial-gradient(circle at 20% 0%, rgba(39,110,139,.20), transparent 34rem),
            radial-gradient(circle at 90% 20%, rgba(179,125,50,.14), transparent 28rem),
            linear-gradient(180deg, #07101c 0%, #030710 100%);
          color: var(--ink); font-family: Inter, sans-serif;
        }}
        .stApp::before {{ content:""; position:fixed; inset:0; pointer-events:none; opacity:.18;
          background-image:linear-gradient(rgba(75,174,194,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(75,174,194,.08) 1px,transparent 1px);
          background-size:42px 42px; mask-image:linear-gradient(to bottom,black,transparent 82%); }}
        h1,h2,h3,.jedi-title {{ font-family:'Chakra Petch',sans-serif !important; letter-spacing:.035em; }}
        h1 {{ color:#f6df9d !important; text-shadow:0 0 22px rgba(231,189,100,.22); }}
        h2,h3 {{ color:#b8f4f5 !important; }}
        p,li,label {{ color:#d7e6e8; }}
        [data-testid="stHeader"] {{ background:rgba(3,7,16,.72); backdrop-filter:blur(12px); }}
        [data-testid="stSidebar"] {{ background:linear-gradient(180deg,#07111d,#050a12); border-right:1px solid rgba(88,216,232,.18); }}
        .block-container {{ max-width:1240px; padding-top:2rem; padding-bottom:4rem; }}
        .hero {{ position:relative; min-height:390px; border:1px solid rgba(88,216,232,.32); border-radius:24px; overflow:hidden; padding:54px; display:flex; align-items:flex-end;
          background:linear-gradient(90deg,rgba(2,8,16,.94) 0%,rgba(3,12,22,.72) 48%,rgba(3,8,15,.28)),url('{hero}') center/cover;
          box-shadow:0 26px 70px rgba(0,0,0,.38),inset 0 0 70px rgba(49,184,204,.08); }}
        .hero::after {{ content:""; position:absolute; inset:14px; border:1px solid rgba(231,189,100,.16); border-radius:16px; pointer-events:none; }}
        .hero-copy {{ max-width:720px; position:relative; z-index:2; }}
        .eyebrow {{ color:var(--cyan); text-transform:uppercase; letter-spacing:.22em; font:600 12px 'Chakra Petch'; }}
        .hero h1 {{ margin:.5rem 0 .8rem; font-size:clamp(2.4rem,5.8vw,5.2rem); line-height:.94; }}
        .hero p {{ max-width:610px; font-size:1.05rem; color:#c8d9dc; }}
        .jedi-card {{ background:linear-gradient(145deg,rgba(15,31,47,.92),rgba(7,17,29,.94)); border:1px solid rgba(88,216,232,.22); border-radius:18px; padding:22px; min-height:100%; box-shadow:inset 0 1px rgba(255,255,255,.035),0 16px 40px rgba(0,0,0,.18); }}
        .jedi-card.gold {{ border-color:rgba(231,189,100,.32); }}
        .jedi-card.red {{ border-color:rgba(226,113,91,.34); }}
        .jedi-card .kicker {{ color:var(--gold); font:600 11px 'Chakra Petch'; letter-spacing:.16em; text-transform:uppercase; }}
        .jedi-card h3 {{ margin:.35rem 0 .5rem; }}
        .metric-rune {{ font:700 2.2rem 'Chakra Petch'; color:#f4dc97; }}
        .term-pair {{ display:flex; gap:.7rem; align-items:center; flex-wrap:wrap; margin:.5rem 0 1rem; }}
        .term-pair span {{ border:1px solid rgba(88,216,232,.25); border-radius:999px; padding:.28rem .65rem; color:#b9eef2; font:500 12px 'Chakra Petch'; }}
        .map-node {{ display:flex; gap:16px; align-items:center; padding:16px 18px; border-radius:14px; border:1px solid rgba(88,216,232,.18); background:rgba(7,21,34,.74); margin:10px 0; }}
        .map-node.active {{ border-color:var(--gold); box-shadow:0 0 24px rgba(231,189,100,.10); }}
        .map-node.locked {{ opacity:.48; filter:saturate(.55); }}
        .map-index {{ width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:#112c3b;color:var(--cyan);font:700 16px 'Chakra Petch'; }}
        .map-node.active .map-index {{ background:#4d3d1f;color:#ffe4a0; }}
        .seal-row {{ display:flex; gap:8px; flex-wrap:wrap; margin:14px 0; }}
        .seal {{ width:36px;height:36px;border-radius:50%;display:grid;place-items:center;border:1px solid rgba(88,216,232,.35);color:#7bbbc4;background:#07131f; }}
        .seal.won {{ color:#ffe09a;border-color:#d9a441;background:#392f1b;box-shadow:0 0 18px rgba(217,164,65,.18); }}
        .stButton > button, .stDownloadButton > button {{ border-radius:12px !important; border:1px solid rgba(88,216,232,.42) !important; background:linear-gradient(180deg,#173849,#102733) !important; color:#eaffff !important; font-family:'Chakra Petch' !important; font-weight:600 !important; min-height:44px; }}
        .stButton > button:hover, .stDownloadButton > button:hover {{ border-color:#e7bd64 !important; color:#ffe8ac !important; transform:translateY(-1px); }}
        textarea,input {{ background:#07121e !important; color:#ddf7f7 !important; border-color:rgba(88,216,232,.26) !important; }}
        code,pre,textarea {{ font-family:'Chakra Petch',Consolas,monospace !important; }}
        [data-testid="stMetric"] {{ background:rgba(10,26,40,.74);border:1px solid rgba(88,216,232,.16);border-radius:14px;padding:14px; }}
        [data-testid="stDataFrame"] {{ border:1px solid rgba(88,216,232,.18); border-radius:14px; overflow:hidden; }}
        .status-banner {{ border-left:3px solid var(--cyan); background:rgba(18,53,65,.5); padding:13px 16px; border-radius:0 12px 12px 0; color:#d9f5f5; margin:12px 0; }}
        .holocron {{ border:1px solid rgba(231,189,100,.45); background:radial-gradient(circle at 50% 0%,rgba(231,189,100,.18),transparent 45%),#0a1723; border-radius:22px; padding:28px; text-align:center; }}
        .holocron-symbol {{ font-size:4rem;color:#ffe19b;text-shadow:0 0 28px rgba(255,210,105,.45); }}
        @media (max-width:720px) {{ .hero {{ min-height:340px;padding:30px 24px; }} .block-container {{ padding-left:1rem;padding-right:1rem; }} }}
        @media (prefers-reduced-motion:reduce) {{ * {{ scroll-behavior:auto !important; transition:none !important; }} }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero() -> None:
    st.markdown(
        """
        <section class="hero">
          <div class="hero-copy">
            <div class="eyebrow">Archivo 04 · Protocolo de recuperación</div>
            <h1>La Cámara de los Experimentos Perdidos</h1>
            <p>La Biblioteca ha sido saboteada. Reconstruye las runs, recupera sus evidencias y demuestra ante el Consejo qué modelo merece conservarse.</p>
            <div class="term-pair"><span>Scikit-learn entrena</span><span>MLflow registra</span><span>El Consejo decide</span></div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str, kicker: str = "Archivo Jedi", tone: str = "") -> None:
    st.markdown(
        f'<div class="jedi-card {tone}"><div class="kicker">{kicker}</div><h3>{title}</h3><p>{body}</p></div>',
        unsafe_allow_html=True,
    )


def seals(completed: int) -> None:
    symbols = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ"]
    html = "".join(f'<span class="seal {"won" if i < completed else ""}">{symbol}</span>' for i, symbol in enumerate(symbols))
    st.markdown(f'<div class="seal-row">{html}</div>', unsafe_allow_html=True)


def map_node(index: int, title: str, concept: str, state: str) -> None:
    lock = "◇" if state == "locked" else ("✓" if state == "done" else "✦")
    st.markdown(
        f'<div class="map-node {state}"><div class="map-index">{lock}</div><div><strong>{index}. {title}</strong><br><small>{concept}</small></div></div>',
        unsafe_allow_html=True,
    )
