import streamlit as st
import json
import datetime
import pandas as pd

st.set_page_config(
    page_title="🚦 Sistemi i Vonesave",
    page_icon="🏫",
    layout="wide"
)

# CSS për stilizim
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 24px;
        width: 100%;
    }
    .alert-yellow {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    .alert-orange {
        background-color: #fdebd0;
        border: 1px solid #fdcb6e;
        color: #e67e22;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    .alert-red {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Titulli
st.title("🏫 SISTEMI I MENAXHIMIT TË VONESAVE")
st.markdown("---")

# Database e thjeshtë
if 'data' not in st.session_state:
    st.session_state.data = {"nxenesit": [], "historiku": []}

def save_data():
    with open('vonesat.json', 'w') as f:
        json.dump(st.session_state.data, f)

def load_data():
    try:
        with open('vonesat.json', 'r') as f:
            st.session_state.data = json.load(f)
    except:
        st.session_state.data = {"nxenesit": [], "historiku": []}

# Ngarko të dhënat
load_data()

# Kolonat
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Regjistro Vonesë")
    
    emri = st.text_input("Emri i Nxënësit")
    klasa = st.text_input("Klasa (opsionale)")
    
    if st.button("✅ Regjistro Vonesën", type="primary"):
        if emri:
            # Gjej ose krijo nxënës
            nxenesi_gjetur = None
            for n in st.session_state.data["nxenesit"]:
                if n["emri"].lower() == emri.lower():
                    nxenesi_gjetur = n
                    break
            
            if nxenesi_gjetur:
                nxenesi_gjetur["vonesa"] += 1
                vonesa = nxenesi_gjetur["vonesa"]
            else:
                nxenesi_gjetur = {
                    "id": len(st.session_state.data["nxenesit"]) + 1,
                    "emri": emri,
                    "klasa": klasa,
                    "vonesa": 1,
                    "data_regjistrimit": str(datetime.date.today())
                }
                st.session_state.data["nxenesit"].append(nxenesi_gjetur)
                vonesa = 1
            
            # Shto në historik
            historik = {
                "id": len(st.session_state.data["historiku"]) + 1,
                "nxenesi_id": nxenesi_gjetur["id"],
                "emri": emri,
                "data_vonese": str(datetime.date.today()),
                "koha": str(datetime.datetime.now().time()),
                "paralajmerimi": vonesa
            }
            st.session_state.data["historiku"].append(historik)
            
            # Shfaq paralajmërimin
            save_data()
            st.success(f"✅ {emri} u regjistrua me sukses!")
            
            # Paralajmërimi me ngjyrë
            if vonesa == 1:
                st.markdown('<div class="alert-yellow">🟡 PARALAJMËRIMI I PARË<br>Nxënësi ka 1 vonesë</div>', unsafe_allow_html=True)
            elif vonesa == 2:
                st.markdown('<div class="alert-orange">🟠 PARALAJMËRIMI I DYTË<br>Nxënësi ka 2 vonesa</div>', unsafe_allow_html=True)
            elif vonesa >= 3:
                st.markdown('<div class="alert-red">🔴 NUK LEJOHET HYRJA!<br>Nxënësi ka 3 ose më shumë vonesa</div>', unsafe_allow_html=True)
        else:
            st.error("❌ Ju lutem shkruani emrin e nxënësit!")

with col2:
    st.header("📋 Lista e Nxënësve")
    
    if st.session_state.data["nxenesit"]:
        # Krijo DataFrame
        df_data = []
        for n in st.session_state.data["nxenesit"]:
            status = "Pa vonesa"
            if n["vonesa"] == 1:
                status = "Paralajmërim 1 🟡"
            elif n["vonesa"] == 2:
                status = "Paralajmërim 2 🟠"
            elif n["vonesa"] >= 3:
                status = "I BLLOKUAR 🔴"
            
            df_data.append({
                "ID": n["id"],
                "Emri": n["emri"],
                "Klasa": n.get("klasa", ""),
                "Vonesa": n["vonesa"],
                "Statusi": status
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Statistika
        st.subheader("📊 Statistika")
        total = len(st.session_state.data["nxenesit"])
        me_vonesa = sum(1 for n in st.session_state.data["nxenesit"] if n["vonesa"] > 0)
        te_bllokuar = sum(1 for n in st.session_state.data["nxenesit"] if n["vonesa"] >= 3)
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("Total Nxënës", total)
        with col_stat2:
            st.metric("Me Vonesa", me_vonesa)
        with col_stat3:
            st.metric("Të Bllokuar", te_bllokuar)
    else:
        st.info("ℹ️ Nuk ka nxënës të regjistruar akoma.")

# Reset vonesash
st.markdown("---")
st.header("🔄 Reset Vonesash")

reset_col1, reset_col2 = st.columns([3, 1])
with reset_col1:
    reset_emri = st.text_input("Shkruani emrin për të resetuar vonesat")
with reset_col2:
    if st.button("Reset", type="secondary"):
        if reset_emri:
            for n in st.session_state.data["nxenesit"]:
                if n["emri"].lower() == reset_emri.lower():
                    n["vonesa"] = 0
                    save_data()
                    st.success(f"✅ Vonesat u resetuan për {reset_emri}")
                    st.rerun()
            else:
                st.error(f"❌ Nxënësi '{reset_emri}' nuk u gjet")
