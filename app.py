from datetime import datetime
import html

import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from config import (
    BATTERY_PERCENT,
    CURRENT_MA,
    ROOM_TEMPERATURE_C,
    TEMPERATURE_IS_PLACEHOLDER,
    BATTERY_LOW_PERCENT,
    TEMPERATURE_HIGH_C,
)

st.set_page_config(
    page_title="EcoVolt Smart 2.0",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---- Theme ----
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
      :root { --bg:#080d0b; --panel:#101915; --panel2:#131f19; --line:#25352b; --muted:#91a49a; --green:#a8ff60; --green2:#64d98a; --white:#eff8f1; }
      html, body, [class*="css"] { font-family:'Manrope',sans-serif; }
      .stApp { background:radial-gradient(ellipse at 80% 0%, #17291e 0%, #080d0b 44%); color:var(--white); }
      #MainMenu, footer, header {visibility:hidden;}
      .block-container {max-width:1440px; padding-top:1.5rem; padding-bottom:2.5rem;}
      .topline {display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:1.6rem;}
      .brand {display:flex; align-items:center; gap:13px;}
      .brand-icon {width:48px;height:48px;display:flex;align-items:center;justify-content:center;border-radius:15px;background:linear-gradient(145deg,#c2ff81,#62d78a);color:#0b160d;font-size:25px;box-shadow:0 0 28px #91ff5d22;}
      .brand-name {font-size:1.35rem;font-weight:800;letter-spacing:-.04em;color:#f3fff5;line-height:1.15;}
      .brand-sub {font-size:.72rem;color:#93a99a;letter-spacing:.15em;text-transform:uppercase;margin-top:5px;}
      .system-pill {border:1px solid #315b3b;background:#112319;color:#b9ffc1;border-radius:999px;padding:9px 13px;font-size:.72rem;letter-spacing:.04em;white-space:nowrap;}
      .hero {padding:26px 28px;border:1px solid #29392e;border-radius:24px;background:linear-gradient(115deg,#14231aee,#0c1410ee);position:relative;overflow:hidden;margin-bottom:20px;}
      .hero:after {content:'';position:absolute;width:260px;height:260px;border-radius:50%;right:4%;top:-150px;border:1px solid #a8ff601b;box-shadow:0 0 0 28px #a8ff6008,0 0 0 58px #a8ff6005;pointer-events:none;}
      .eyebrow {font-size:.7rem;color:#a8ff60;text-transform:uppercase;letter-spacing:.19em;font-weight:800;margin-bottom:9px;}
      .hero-title {font-size:clamp(1.65rem,3vw,2.55rem);line-height:1.12;font-weight:800;letter-spacing:-.055em;color:#f3fff5;margin:0 0 10px 0;}
      .hero-copy {color:#9eb2a4;font-size:.92rem;max-width:640px;line-height:1.65;}
      .section-head {display:flex;align-items:center;justify-content:space-between;margin:25px 0 12px;gap:1rem;}
      .section-title {font-size:1rem;font-weight:800;color:#eaf7ed;letter-spacing:-.02em;}
      .section-note {font-size:.75rem;color:#84988a;}
      .metric-card {height:100%;min-height:138px;border:1px solid #26372c;background:linear-gradient(145deg,#131f18,#0d1511);border-radius:19px;padding:18px 19px;position:relative;overflow:hidden;}
      .metric-top {display:flex;align-items:center;justify-content:space-between;color:#a0b2a5;font-size:.77rem;gap:8px;}
      .metric-icon {width:33px;height:33px;border:1px solid #304737;border-radius:11px;display:flex;align-items:center;justify-content:center;color:#a8ff60;background:#1a2a1d;font-size:16px;}
      .metric-value {font-size:2rem;font-weight:800;letter-spacing:-.055em;color:#f2fff4;margin-top:12px;line-height:1.15;}
      .metric-unit {font-size:.85rem;color:#a5b7aa;font-weight:600;letter-spacing:0;}
      .metric-foot {font-size:.72rem;color:#829889;margin-top:7px;}
      .status-dot {display:inline-block;width:7px;height:7px;border-radius:50%;background:#a8ff60;margin-right:6px;box-shadow:0 0 10px #a8ff6080;}
      .panel {border:1px solid #26372c;background:linear-gradient(145deg,#121d16,#0d1410);border-radius:20px;padding:18px 20px;height:100%;}
      .panel-title {font-size:.92rem;font-weight:800;color:#eaf7ed;margin-bottom:3px;}
      .panel-sub {font-size:.73rem;color:#84988a;margin-bottom:10px;}
      .legend-row {display:flex;align-items:center;justify-content:space-between;padding:12px 0;border-bottom:1px solid #243229;color:#9aafa0;font-size:.79rem;gap:10px;}
      .legend-row:last-child {border-bottom:0;}
      .legend-value {color:#f1fff2;font-weight:700;}
      .footer {border-top:1px solid #203026;margin-top:28px;padding-top:15px;color:#708478;font-size:.72rem;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;}
      div[data-testid="stPlotlyChart"] {border:1px solid #26372c;background:#101915;border-radius:18px;padding:7px 7px 0;}
      @media(max-width:700px){.topline{align-items:flex-start}.system-pill{font-size:.62rem;padding:7px 9px}.hero{padding:21px}.metric-value{font-size:1.7rem}}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Header ----
now = datetime.now()
st.markdown(
    f"""
    <div class="topline">
      <div class="brand">
        <div class="brand-icon">☀</div>
        <div><div class="brand-name">EcoVolt <span style="color:#a8ff60">Smart 2.0</span></div>
        <div class="brand-sub">Solar mobility · Energy overview</div></div>
      </div>
      <div class="system-pill"><span class="status-dot"></span> SYSTEM OVERVIEW &nbsp;·&nbsp; {now.strftime('%d %b %Y')}</div>
    </div>
    <div class="hero">
      <div class="eyebrow">Energy management interface</div>
      <div class="hero-title">Power your journey.<br><span style="color:#a8ff60">See every detail.</span></div>
      <div class="hero-copy">A clear view of battery charge, electrical current and cabin environment in one place.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- Summary metrics ----
temperature_label = "Room Temperature · Placeholder" if TEMPERATURE_IS_PLACEHOLDER else "Room Temperature"
temp_note = "Placeholder value — update when specified" if TEMPERATURE_IS_PLACEHOLDER else "Configured temperature value"

st.markdown('<div class="section-head"><div class="section-title">Live overview</div><div class="section-note">Configured readings</div></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    st.markdown(f'''<div class="metric-card"><div class="metric-top"><span>Battery charge</span><span class="metric-icon">▰</span></div><div class="metric-value">{BATTERY_PERCENT}<span class="metric-unit">%</span></div><div class="metric-foot"><span class="status-dot"></span>Charge level</div></div>''', unsafe_allow_html=True)
with c2:
    st.markdown(f'''<div class="metric-card"><div class="metric-top"><span>Electrical current</span><span class="metric-icon">ϟ</span></div><div class="metric-value">{CURRENT_MA}<span class="metric-unit"> mA</span></div><div class="metric-foot"><span class="status-dot"></span>Configured current</div></div>''', unsafe_allow_html=True)
with c3:
    st.markdown(f'''<div class="metric-card"><div class="metric-top"><span>{html.escape(temperature_label)}</span><span class="metric-icon">♨</span></div><div class="metric-value">{ROOM_TEMPERATURE_C}<span class="metric-unit"> °C</span></div><div class="metric-foot">{html.escape(temp_note)}</div></div>''', unsafe_allow_html=True)

st.markdown('<div class="section-head"><div class="section-title">System analytics</div><div class="section-note">Visual indicators · not sensor-connected</div></div>', unsafe_allow_html=True)
left, right = st.columns([1.12, 0.88], gap="medium")

# Gauges use Plotly's native indicator rendering for reliable startup.
def gauge(title, value, suffix, maximum, steps, bar_color="#a8ff60", number_format=None):
    number = {"suffix": suffix, "font": {"size": 33, "color": "#f1fff2", "family": "Manrope"}}
    if number_format:
        number["valueformat"] = number_format
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=number,
        title={"text": title, "font": {"size": 14, "color": "#9fb2a4", "family": "Manrope"}},
        gauge={
            "axis": {"range": [0, maximum], "tickwidth": 0, "tickcolor": "#728678", "tickfont": {"color": "#718578", "size": 10}},
            "bar": {"color": bar_color, "thickness": 0.24},
            "bgcolor": "#18251c",
            "borderwidth": 0,
            "steps": steps,
            "threshold": {"line": {"color": "#eaf8ec", "width": 2}, "thickness": 0.75, "value": value},
        },
        domain={"x": [0.06, 0.94], "y": [0.04, 0.9]},
    ))
    fig.update_layout(
        height=245,
        margin={"l": 18, "r": 18, "t": 36, "b": 10},
        paper_bgcolor="#101915",
        plot_bgcolor="#101915",
        font={"family": "Manrope", "color": "#eff8f1"},
    )
    return fig

with left:
    st.markdown('<div class="panel-title">Performance indicators</div><div class="panel-sub">Configured values shown on instrument-style gauges</div>', unsafe_allow_html=True)
    g1, g2 = st.columns(2, gap="small")
    with g1:
        st.plotly_chart(gauge("BATTERY CHARGE", BATTERY_PERCENT, "%", 100, [{"range": [0, 20], "color": "#2b3025"}, {"range": [20, 100], "color": "#18251c"}]), use_container_width=True, config={"displayModeBar": False, "staticPlot": True})
    with g2:
        st.plotly_chart(gauge("CURRENT", CURRENT_MA, " mA", 1000, [{"range": [0, 1000], "color": "#18251c"}], bar_color="#69dfa0"), use_container_width=True, config={"displayModeBar": False, "staticPlot": True})
    st.plotly_chart(gauge("ROOM TEMPERATURE", ROOM_TEMPERATURE_C, " °C", 60, [{"range": [0, 40], "color": "#18251c"}, {"range": [40, 60], "color": "#30251a"}], bar_color="#c3ff77"), use_container_width=True, config={"displayModeBar": False, "staticPlot": True})

with right:
    st.markdown('<div class="panel-title">Solar vehicle overview</div><div class="panel-sub">Illustrative system layout</div>', unsafe_allow_html=True)
    car_svg = f'''<svg viewBox="0 0 620 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Solar car illustration" style="width:100%;height:auto;display:block">
      <defs><linearGradient id="body" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#caff87"/><stop offset="1" stop-color="#4fcf8a"/></linearGradient><linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#233e32"/><stop offset="1" stop-color="#0a1510"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
      <ellipse cx="310" cy="232" rx="220" ry="23" fill="#a8ff60" opacity=".09"/>
      <path d="M98 195 L135 163 Q158 150 210 146 L270 104 Q291 92 332 97 L409 117 Q432 123 452 151 L501 171 Q521 181 522 199 L512 216 L99 216 Z" fill="url(#body)" stroke="#d5ffad" stroke-width="2"/>
      <path d="M218 143 L277 108 Q293 101 327 105 L390 121 L419 147 Z" fill="url(#glass)" stroke="#8ce9a1" stroke-width="2"/>
      <path d="M284 109 L278 143 L355 143 L347 110" fill="none" stroke="#537d64" stroke-width="2"/>
      <path d="M126 177 L197 169 L201 185 L120 193 Z" fill="#1a2b20" stroke="#92ee9c" stroke-width="1.5"/>
      <path d="M414 160 L490 181 L495 192 L423 181 Z" fill="#efffc9" opacity=".9"/>
      <path d="M260 161 L407 161" stroke="#284b32" stroke-width="2" opacity=".65"/>
      <rect x="239" y="169" width="153" height="31" rx="5" fill="#15251a" stroke="#a8ff60" stroke-width="1.5"/>
      <g stroke="#a8ff60" stroke-width="1" opacity=".8"><path d="M264 170 V199 M289 170 V199 M314 170 V199 M339 170 V199 M364 170 V199 M239 184 H392"/></g>
      <circle cx="190" cy="211" r="32" fill="#080d0b" stroke="#405849" stroke-width="5"/><circle cx="190" cy="211" r="16" fill="#26392c" stroke="#a8ff60" stroke-width="2"/><circle cx="190" cy="211" r="5" fill="#a8ff60"/>
      <circle cx="438" cy="211" r="32" fill="#080d0b" stroke="#405849" stroke-width="5"/><circle cx="438" cy="211" r="16" fill="#26392c" stroke="#a8ff60" stroke-width="2"/><circle cx="438" cy="211" r="5" fill="#a8ff60"/>
      <path d="M72 247 H548" stroke="#354a3b" stroke-width="1" stroke-dasharray="4 8"/><path d="M270 260 H350" stroke="#a8ff60" stroke-width="2" opacity=".65" filter="url(#glow)"/>
      <g font-family="Manrope, sans-serif" font-size="12" fill="#a8ff60"><text x="76" y="83">SOLAR ARRAY</text><path d="M160 88 L273 167" stroke="#a8ff60" stroke-width="1" stroke-dasharray="3 4" fill="none"/><text x="417" y="70">ENERGY STORAGE</text><path d="M474 76 L372 168" stroke="#a8ff60" stroke-width="1" stroke-dasharray="3 4" fill="none"/></g>
    </svg>'''
    components.html(car_svg, height=310, scrolling=False)
    st.markdown(
        f'''<div class="legend-row"><span>Battery charge</span><span class="legend-value">{BATTERY_PERCENT}%</span></div>
        <div class="legend-row"><span>Electrical current</span><span class="legend-value">{CURRENT_MA} mA</span></div>
        <div class="legend-row"><span>{html.escape(temperature_label)}</span><span class="legend-value">{ROOM_TEMPERATURE_C} °C</span></div>
        <div class="legend-row"><span>Dashboard data source</span><span class="legend-value">Local configuration</span></div>''',
        unsafe_allow_html=True,
    )

st.markdown(
    f'''<div class="footer"><span>© EcoVolt Smart 2.0 · Solar mobility dashboard</span><span>Last page refresh: {now.strftime('%H:%M:%S')} · Values are configuration-based</span></div>''',
    unsafe_allow_html=True,
)
