import os
from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage
from main import app


st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide",
)

# ── Sidebar: global controls ────────────────────────────────────────────────
with st.sidebar:
    theme_mode = st.radio(
        "🎨 Theme Mode",
        ["Dark Mode", "Light Mode"],
        index=0,
        horizontal=True,
    )

# ── Theme tokens ────────────────────────────────────────────────────────────
if theme_mode == "Dark Mode":
    COLORS = {
        "app_bg": "#080d14",
        "sidebar_bg": "#090e18",
        "card_bg": "#0e1623",
        "card_bg_2": "#0a1520",
        "chip_bg": "#0e1a2b",
        "chip_hover": "#1a2e47",
        "border": "#1e2e44",
        "border_2": "#1e3050",
        "text": "#e8f4ff",
        "muted": "#94adc8",
        "muted_2": "#7aa8cc",
        "accent": "#3a7bd5",
        "accent_2": "#4ea8f0",
        "button_start": "#1a6bbf",
        "button_mid": "#0d4a8a",
        "button_end": "#0a3d75",
        "hero_filter": "brightness(0.35)",
        "final_gradient": "linear-gradient(160deg, #0c1a2e 0%, #0a1520 100%)",
    }
else:
    COLORS = {
        "app_bg": "#f7f9fc",
        "sidebar_bg": "#eef3f8",
        "card_bg": "#ffffff",
        "card_bg_2": "#f5f8fc",
        "chip_bg": "#ffffff",
        "chip_hover": "#e9f2ff",
        "border": "#d9e2ec",
        "border_2": "#c9d8ea",
        "text": "#1b2733",
        "muted": "#52677a",
        "muted_2": "#4e6f8f",
        "accent": "#2563eb",
        "accent_2": "#1d4ed8",
        "button_start": "#2563eb",
        "button_mid": "#1d4ed8",
        "button_end": "#1e40af",
        "hero_filter": "brightness(0.55)",
        "final_gradient": "linear-gradient(160deg, #ffffff 0%, #f5f8fc 100%)",
    }

# ── Styling ─────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {{
    font-family: 'Inter', sans-serif;
    background-color: {COLORS['app_bg']};
    color: {COLORS['text']};
}}

/* ── Hero ── */
.hero-wrapper {{
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 2rem;
    min-height: 340px;
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow: 0 22px 70px rgba(0,0,0,0.34);
}}
.hero-wrapper::before {{
    content: "";
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at 15% 20%, rgba(78,168,240,0.32), transparent 28%),
        linear-gradient(120deg, rgba(3,7,18,0.82) 0%, rgba(8,13,20,0.68) 48%, rgba(37,99,235,0.25) 100%);
    z-index: 1;
}}
.hero-wrapper::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.34) 100%);
    z-index: 1;
}}
.hero-bg {{
    width: 100%;
    height: 100%;
    min-height: 340px;
    object-fit: cover;
    display: block;
    filter: {COLORS['hero_filter']};
    position: absolute;
    top: 0; left: 0;
    transform: scale(1.02);
}}
.hero-content {{
    position: relative;
    z-index: 2;
    min-height: 340px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    text-align: left;
    padding: 2.6rem 3rem;
}}
.hero-panel {{
    max-width: 760px;
    padding: 1.6rem 1.8rem;
    border-radius: 22px;
    background: rgba(8, 13, 20, 0.46);
    border: 1px solid rgba(255,255,255,0.16);
    backdrop-filter: blur(10px);
}}
.hero-badge {{
    background: rgba(58,123,213,0.22);
    border: 1px solid rgba(122,184,245,0.48);
    color: #dbeafe !important;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.38rem 0.95rem;
    border-radius: 999px;
    margin-bottom: 1rem;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}}
.hero-title {{
    font-size: clamp(2rem, 4vw, 3.25rem);
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.75rem;
    line-height: 1.08;
    letter-spacing: -0.04em;
    text-shadow: 0 8px 28px rgba(0,0,0,0.45);
}}
.hero-sub {{
    color: #e6f1ff;
    font-size: 1.05rem;
    max-width: 690px;
    line-height: 1.65;
}}
.hero-feature-row {{
    display: flex;
    gap: 0.7rem;
    flex-wrap: wrap;
    margin-top: 1.2rem;
}}
.hero-feature-pill {{
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.16);
    color: #ffffff;
    border-radius: 999px;
    padding: 0.48rem 0.82rem;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}}
@media (max-width: 768px) {{
    .hero-content {{
        padding: 1.5rem;
        text-align: center;
        justify-content: center;
    }}
    .hero-panel {{
        padding: 1.25rem;
    }}
    .hero-feature-row {{
        justify-content: center;
    }}
}}

/* ── Cards and sections ── */
.input-card, .preference-card, .metric-box, .save-bar {{
    background: {COLORS['card_bg']};
    border: 1px solid {COLORS['border']};
    border-radius: 16px;
    color: {COLORS['text']};
}}
.preference-card {{
    padding: 1.25rem 1.4rem;
    margin-bottom: 1.4rem;
}}
.input-label {{
    color: {COLORS['accent_2']};
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 1rem 0 0.5rem;
}}
.sec-head {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid {COLORS['border']};
}}
.sec-head span {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {COLORS['text']};
}}

/* ── Destination strip ── */
.destination-tile {{
    border-radius: 10px;
    overflow: hidden;
    position: relative;
    height: 90px;
    cursor: pointer;
    border: 1px solid {COLORS['border']};
}}
.destination-tile img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.58);
}}
.destination-tile div {{
    position:absolute;
    bottom:8px;
    left:0;
    right:0;
    text-align:center;
    color:#fff;
    font-size:0.8rem;
    font-weight:700;
}}

/* ── Buttons ── */
div[data-testid="stButton"] > button {{
    background: linear-gradient(135deg, {COLORS['button_start']} 0%, {COLORS['button_mid']} 50%, {COLORS['button_end']} 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2.5rem !important;
    font-size: 1.02rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    box-shadow: 0 0 24px rgba(37,99,235,0.28), 0 4px 15px rgba(0,0,0,0.22) !important;
    transition: all 0.3s ease !important;
}}
div[data-testid="stButton"] > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 0 36px rgba(37,99,235,0.45), 0 6px 20px rgba(0,0,0,0.28) !important;
}}

/* ── Agent status cards ── */
[data-testid="stStatusWidget"] {{
    background: {COLORS['card_bg']} !important;
    border: 1px solid {COLORS['border_2']} !important;
    border-radius: 12px !important;
}}
[data-testid="stStatusWidget"] > div:first-child {{
    background: {COLORS['card_bg']} !important;
    border-radius: 12px 12px 0 0 !important;
}}
[data-testid="stStatusWidget"] details,
[data-testid="stStatusWidget"] details > div,
[data-testid="stStatusWidget"] [data-testid="stVerticalBlock"] {{
    background: {COLORS['card_bg_2']} !important;
    color: {COLORS['text']} !important;
    padding: 0.25rem 0.5rem !important;
}}
[data-testid="stStatusWidget"] * {{ color: {COLORS['text']} !important; }}
[data-testid="stStatusWidget"] a {{ color: {COLORS['accent_2']} !important; }}
[data-testid="stStatusWidget"] hr {{ border-color: {COLORS['border_2']} !important; }}

/* ── Metrics ── */
.metric-row {{
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
}}
.metric-box {{
    flex: 1;
    padding: 1rem 1.2rem;
    text-align: center;
}}
.metric-val {{
    font-size: 1.55rem;
    font-weight: 800;
    color: {COLORS['accent_2']};
}}
.metric-lbl {{
    font-size: 0.76rem;
    color: {COLORS['muted_2']} !important;
    margin-top: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}

/* ── Final plan ── */
.final-card {{
    background: {COLORS['final_gradient']};
    border: 1px solid {COLORS['border_2']};
    border-left: 4px solid {COLORS['accent']};
    border-radius: 14px;
    padding: 1.8rem;
    line-height: 1.8;
    color: {COLORS['text']};
    font-size: 0.95rem;
}}
.save-bar {{
    padding: 0.85rem 1.2rem;
    color: {COLORS['muted_2']};
    font-size: 0.88rem;
    margin-top: 0.5rem;
}}
.save-bar code {{
    color: {COLORS['accent_2']} !important;
    background: {COLORS['card_bg_2']} !important;
    padding: 0.15em 0.4em;
    border-radius: 4px;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: {COLORS['sidebar_bg']} !important;
    border-right: 1px solid {COLORS['border']} !important;
}}
.sidebar-chip {{
    background: {COLORS['chip_bg']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 0.45rem 0.75rem;
    margin-bottom: 0.4rem;
    font-size: 0.83rem;
    color: {COLORS['muted_2']};
}}
.sidebar-title {{
    color: {COLORS['text']};
    font-size: 1rem;
    font-weight: 700;
    margin: 1rem 0 0.5rem;
}}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown {{ color: {COLORS['muted_2']} !important; }}
section[data-testid="stSidebar"] hr {{ border-color: {COLORS['border']} !important; }}

/* ── Inputs ── */
.stTextArea textarea,
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div,
.stDateInput input {{
    background: {COLORS['card_bg_2']} !important;
    border: 1px solid {COLORS['border']} !important;
    border-radius: 10px !important;
    color: {COLORS['text']} !important;
}}
.stTextArea textarea:focus,
.stTextInput input:focus,
.stNumberInput input:focus,
.stDateInput input:focus {{
    border-color: {COLORS['accent']} !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,0.2) !important;
}}
.stTextArea textarea::placeholder,
.stTextInput input::placeholder {{ color: {COLORS['muted']} !important; }}
.stTextInput label, .stTextArea label,
.stSelectbox label, .stNumberInput label, .stDateInput label {{
    color: {COLORS['accent_2']} !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
}}

/* General markdown */
.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th {{
    color: {COLORS['muted']} !important;
}}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{ color: {COLORS['text']} !important; }}
.stMarkdown code {{
    background: {COLORS['card_bg_2']} !important;
    color: {COLORS['accent_2']} !important;
    padding: 0.15em 0.4em;
    border-radius: 4px;
}}
.stAlert {{
    background: {COLORS['card_bg']} !important;
    border-radius: 10px !important;
}}
.stAlert p, .stAlert div {{ color: {COLORS['text']} !important; }}
div[data-testid="stDownloadButton"] > button {{
    background: {COLORS['chip_bg']} !important;
    color: {COLORS['text']} !important;
    border: 1px solid {COLORS['border_2']} !important;
    border-radius: 10px !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
</style>
""",
    unsafe_allow_html=True,
)

# ── Sidebar content ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🌍 AI Travel Planner</div>", unsafe_allow_html=True)
    st.markdown("---")

    thread_id = st.text_input(
        "👤 User ID",
        value="Akhilesh_Trivedi",
        help="Your session ID — keeps travel history across queries",
    )

    st.markdown("<div class='sidebar-title'>Powered by</div>", unsafe_allow_html=True)
    for tech in [
        "🔗 LangGraph",
        "🧠 Groq · LLaMA 3.3 70B",
        "🐘 PostgreSQL",
        "🔍 Tavily Search",
        "✈️ AviationStack",
    ]:
        st.markdown(f"<div class='sidebar-chip'>{tech}</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Agent Pipeline</div>", unsafe_allow_html=True)
    for step in [
        "① Flight Agent",
        "② Hotel Agent",
        "③ Itinerary Agent",
        "④ Travel Advisory Agent",
        "⑤ Final Agent",
    ]:
        st.markdown(f"<div class='sidebar-chip'>{step}</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Suggested Enhancements</div>", unsafe_allow_html=True)
    for item in [
        "🎯 Structured preferences",
        "💰 Budget split summary",
        "🛂 Visa & travel advisory",
        "🌓 Dark / Light mode",
    ]:
        st.markdown(f"<div class='sidebar-chip'>{item}</div>", unsafe_allow_html=True)

# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero-wrapper">
    <img class="hero-bg"
         src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1600&q=85"
         alt="premium travel landscape"/>
    <div class="hero-content">
        <div class="hero-panel">
            <div class="hero-badge">✦ Multi-Agent AI System</div>
            <div class="hero-title">✈️ AI Travel Booking System</div>
            <div class="hero-sub">Five travel capabilities work together — flights, hotels, itinerary, advisory checks, and a final customer-ready trip plan.</div>
            <div class="hero-feature-row">
                <div class="hero-feature-pill">✈️ Flight Discovery</div>
                <div class="hero-feature-pill">🏨 Hotel Matching</div>
                <div class="hero-feature-pill">🗓️ Smart Itinerary</div>
                <div class="hero-feature-pill">🛂 Advisory Checks</div>
            </div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ── Destination image strip ─────────────────────────────────────────────────
DESTINATIONS = [
    ("🇯🇵 Tokyo", "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),
    ("🇫🇷 Paris", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70"),
    ("🇹🇭 Bangkok", "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70"),
    ("🇮🇹 Rome", "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=300&q=70"),
    ("🇦🇪 Dubai", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70"),
]

cols = st.columns(5)
for col, (name, img_url) in zip(cols, DESTINATIONS):
    with col:
        st.markdown(
            f"""
        <div class="destination-tile">
            <img src="{img_url}" />
            <div>{name}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Travel preferences ──────────────────────────────────────────────────────
st.markdown("<div class='input-label'>🎯 Travel Preferences</div>", unsafe_allow_html=True)

with st.container():
    pref_col1, pref_col2, pref_col3 = st.columns(3)
    with pref_col1:
        budget = st.number_input(
            "Total Budget ₹",
            min_value=10000,
            max_value=2000000,
            value=200000,
            step=10000,
        )
    with pref_col2:
        travelers = st.number_input(
            "Number of Travelers",
            min_value=1,
            max_value=20,
            value=2,
            step=1,
        )
    with pref_col3:
        duration = st.number_input(
            "Trip Duration - Days",
            min_value=1,
            max_value=45,
            value=7,
            step=1,
        )

    pref_col4, pref_col5, pref_col6 = st.columns(3)
    with pref_col4:
        travel_class = st.selectbox(
            "Flight Class",
            ["Economy", "Premium Economy", "Business", "First Class"],
        )
    with pref_col5:
        hotel_category = st.selectbox(
            "Hotel Category",
            ["Budget", "3 Star", "4 Star", "5 Star", "Luxury"],
            index=2,
        )
    with pref_col6:
        trip_type = st.selectbox(
            "Trip Type",
            ["Family", "Couple", "Solo", "Business", "Adventure", "Honeymoon", "Pilgrimage"],
        )

    pref_col7, pref_col8, pref_col9 = st.columns(3)
    with pref_col7:
        food_preference = st.selectbox(
            "Food Preference",
            ["No Preference", "Vegetarian", "Vegan", "Indian Food Preferred", "Halal", "Jain Food"],
        )
    with pref_col8:
        travel_month = st.selectbox(
            "Travel Month",
            [
                "Flexible",
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December",
            ],
        )
    with pref_col9:
        pace = st.selectbox(
            "Travel Pace",
            ["Balanced", "Relaxed", "Fast-paced", "Luxury Comfort", "Budget Optimized"],
        )

# ── Input ───────────────────────────────────────────────────────────────────
st.markdown("<div class='input-label'>🗺️ Describe your trip</div>", unsafe_allow_html=True)

QUICK = [
    "7-day Japan under ₹2L",
    "Paris trip for 5 days",
    "Dubai weekend trip",
    "Bali backpacking 10 days",
]
qcols = st.columns(len(QUICK))
quick_fill = st.session_state.get("quick_fill", "")
for qc, label in zip(qcols, QUICK):
    with qc:
        if st.button(label, key=f"q_{label}"):
            st.session_state["quick_fill"] = label
            quick_fill = label

user_query = st.text_area(
    "Travel query",
    value=quick_fill,
    placeholder="e.g. Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs",
    height=110,
    label_visibility="collapsed",
)

generate = st.button("🚀 Generate My Travel Plan", use_container_width=True)

# ── Agent pipeline ──────────────────────────────────────────────────────────
AGENT_META = {
    "flight_agent": ("✈️", "Flight Agent"),
    "hotel_agent": ("🏨", "Hotel Agent"),
    "itinerary_agent": ("🗓️", "Itinerary Agent"),
    "advisory_agent": ("🛂", "Travel Advisory Agent"),
    "travel_advisory_agent": ("🛂", "Travel Advisory Agent"),
    "final_agent": ("🧠", "Final Agent"),
}

if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
    else:
        enhanced_query = f"""
User Query:
{user_query}

Structured Travel Preferences:
- Total Budget: ₹{budget:,}
- Number of Travelers: {travelers}
- Duration: {duration} days
- Flight Class: {travel_class}
- Hotel Category: {hotel_category}
- Trip Type: {trip_type}
- Food Preference: {food_preference}
- Travel Month: {travel_month}
- Travel Pace: {pace}

Please prepare a practical travel plan considering flights, hotels, itinerary, approximate budget split, local transport, food preference, and travel advisory points such as visa, weather, safety, insurance, and passport validity where applicable.
""".strip()

        config = {"configurable": {"thread_id": thread_id}}
        collected = {
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "advisory": "",
            "final_response": "",
            "llm_calls": 0,
        }

        st.markdown("---")
        st.markdown(
            "<div class='sec-head'><span>🤖 Agent Pipeline — Live</span></div>",
            unsafe_allow_html=True,
        )

        initial_state = {
            "messages": [HumanMessage(content=enhanced_query)],
            "user_query": enhanced_query,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "advisory": "",
            "llm_calls": 0,
        }

        for chunk in app.stream(initial_state, config=config, stream_mode="updates"):
            for node_name, state_update in chunk.items():
                icon, label = AGENT_META.get(node_name, ("🔧", node_name))

                with st.status(f"{icon}  {label}", state="complete", expanded=True):
                    if node_name == "flight_agent":
                        text = state_update.get("flight_results", "")
                        collected["flight_results"] = text
                        st.markdown(text or "_No flight data returned._")

                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text or "_No hotel data returned._")

                    elif node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text or "_No itinerary generated._")

                    elif node_name in ["advisory_agent", "travel_advisory_agent"]:
                        text = state_update.get("advisory", "") or state_update.get("travel_advisory", "")
                        collected["advisory"] = text
                        st.markdown(text or "_No travel advisory generated._")

                    elif node_name == "final_agent":
                        msgs = state_update.get("messages", [])
                        text = msgs[-1].content if msgs else ""
                        collected["final_response"] = text
                        st.markdown(text or "_No final response._")

                    collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

        # Execution metrics
        agent_count = 5 if collected["advisory"] else 4
        st.markdown(
            f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">{agent_count}</div><div class="metric-lbl">Agents Run</div></div>
            <div class="metric-box"><div class="metric-val">{collected['llm_calls']}</div><div class="metric-lbl">LLM Calls</div></div>
            <div class="metric-box"><div class="metric-val">✅</div><div class="metric-lbl">Status</div></div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Budget split summary
        st.markdown(
            "<div class='sec-head'><span>💰 Estimated Budget Summary</span></div>",
            unsafe_allow_html=True,
        )
        flight_cost = int(budget * 0.40)
        hotel_cost = int(budget * 0.35)
        local_transport_cost = int(budget * 0.10)
        food_cost = int(budget * 0.10)
        buffer_cost = int(budget * 0.05)

        st.markdown(
            f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">₹{flight_cost:,}</div><div class="metric-lbl">Flights</div></div>
            <div class="metric-box"><div class="metric-val">₹{hotel_cost:,}</div><div class="metric-lbl">Hotels</div></div>
            <div class="metric-box"><div class="metric-val">₹{local_transport_cost:,}</div><div class="metric-lbl">Local Transport</div></div>
        </div>
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">₹{food_cost:,}</div><div class="metric-lbl">Food</div></div>
            <div class="metric-box"><div class="metric-val">₹{buffer_cost:,}</div><div class="metric-lbl">Buffer</div></div>
            <div class="metric-box"><div class="metric-val">₹{budget:,}</div><div class="metric-lbl">Total Budget</div></div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Advisory section - shown if backend returns it
        if collected["advisory"]:
            st.markdown(
                "<div class='sec-head'><span>🛂 Travel Advisory</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"<div class='final-card'>{collected['advisory']}</div>", unsafe_allow_html=True)

        # Final plan card
        if collected["final_response"]:
            st.markdown(
                "<div class='sec-head'><span>🧠 Final Travel Plan</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"<div class='final-card'>{collected['final_response']}</div>", unsafe_allow_html=True)

        # Save and download
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}.md"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Travel Plan

**Query:** {user_query}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**User ID:** {thread_id}

---

## 🎯 Travel Preferences
- Total Budget: ₹{budget:,}
- Number of Travelers: {travelers}
- Duration: {duration} days
- Flight Class: {travel_class}
- Hotel Category: {hotel_category}
- Trip Type: {trip_type}
- Food Preference: {food_preference}
- Travel Month: {travel_month}
- Travel Pace: {pace}

---

## 💰 Estimated Budget Summary
- Flights: ₹{flight_cost:,}
- Hotels: ₹{hotel_cost:,}
- Local Transport: ₹{local_transport_cost:,}
- Food: ₹{food_cost:,}
- Buffer: ₹{buffer_cost:,}
- Total Budget: ₹{budget:,}

---

## ✈️ Flight Information
{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information
{collected['hotel_results'] or 'N/A'}

---

## 🗓️ Itinerary
{collected['itinerary'] or 'N/A'}

---

## 🛂 Travel Advisory
{collected['advisory'] or 'N/A'}

---

## 🧠 Final Travel Plan
{collected['final_response'] or 'N/A'}

---

*LLM Calls: {collected['llm_calls']}*
"""

        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button(
                "⬇️ Download Plan",
                data=file_content,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True,
            )
        with info_col:
            st.markdown(
                f"<div class='save-bar'>📁 Auto-saved → <code>travel_plans/{filename}</code></div>",
                unsafe_allow_html=True,
            )
