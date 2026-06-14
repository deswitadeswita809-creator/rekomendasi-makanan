# ============================================================
#  SISTEM REKOMENDASI MAKANAN BERBASIS DESKRIPSI + GRAPH
#  Tugas UAS - Struktur Data (Enhanced Interactive Web Version)
# ============================================================

import streamlit as st
from collections import defaultdict
import requests
from streamlit_lottie import st_lottie

# ─────────────────────────────────────────────
#  CONFIG & KONFIGURASI TEMA VISUAL (CSS CUSTOM)
# ─────────────────────────────────────────────
st.set_page_config(page_title="WarmBites - Rekomendasi Makanan", page_icon="🍴", layout="wide")

# Suntikan CSS untuk mengubah tampilan dasar Streamlit agar lebih interaktif
st.markdown("""
    <style>
    /* Latar belakang aplikasi dengan gradasi lembut bertema kuliner hangat */
    .stApp {
        background: linear-gradient(135deg, #FFF9F2 0%, #FFEAD2 100%);
    }
    
    /* Desain kartu rekomendasi makanan utama */
    .food-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(224, 169, 109, 0.15);
        margin-bottom: 20px;
        border-left: 6px solid #FF7A00;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    /* Efek interaktif hover saat mouse berada di atas kartu */
    .food-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(224, 169, 109, 0.3);
    }
    
    /* Badge skor kesesuaian persenan di pojok kanan kartu */
    .match-badge {
        float: right;
        font-size: 15px;
        font-weight: bold;
        background-color: #E3FCEF;
        color: #006644;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #ABF5D1;
    }
    </style>
""", unsafe_allow_html=True)


# Fungsi untuk memuat berkas animasi Lottie secara online
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Memuat aset animasi koki memasak
lottie_chef = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ig9g9w3b.json")


# ─────────────────────────────────────────────
#  1. DATABASE MAKANAN LENGKAP
# ─────────────────────────────────────────────
MAKANAN = {
    "Bakso": {
        "deskripsi"  : ["berkuah", "hangat", "gurih", "daging"],
        "tekstur"    : "berkuah",
        "rasa"       : ["gurih", "asin"],
        "pedas"      : False,
        "kategori"   : "Berat",
        "kalori"     : 350,
        "harga"      : 15,
        "budget"     : "murah",
    },
    "Soto Ayam": {
        "deskripsi"  : ["berkuah", "hangat", "ayam", "segar"],
        "tekstur"    : "berkuah",
        "rasa"       : ["gurih", "segar"],
        "pedas"      : False,
        "kategori"   : "Ringan",
        "kalori"     : 310,
        "harga"      : 18,
        "budget"     : "murah",
    },
    "Mie Ayam": {
        "deskripsi"  : ["berkuah", "mie", "ayam", "gurih"],
        "tekstur"    : "berkuah",
        "rasa"       : ["gurih", "asin"],
        "pedas"      : False,
        "kategori"   : "Berat",
        "kalori"     : 420,
        "harga"      : 16,
        "budget"     : "murah",
    },
    "Nasi Goreng": {
        "deskripsi"  : ["kering", "nasi", "gurih", "populer"],
        "tekstur"    : "kering",
        "rasa"       : ["gurih", "asin", "manis"],
        "pedas"      : True,
        "kategori"   : "Berat",
        "kalori"     : 520,
        "harga"      : 20,
        "budget"     : "murah",
    },
    "Mie Goreng": {
        "deskripsi"  : ["kering", "mie", "gurih", "populer"],
        "tekstur"    : "kering",
        "rasa"       : ["gurih", "asin"],
        "pedas"      : True,
        "kategori"   : "Berat",
        "kalori"     : 490,
        "harga"      : 15,
        "budget"     : "murah",
    },
    "Nasi Padang": {
        "deskripsi"  : ["kering", "nasi", "pedas", "lauk"],
        "tekstur"    : "kering",
        "rasa"       : ["gurih", "pedas"],
        "pedas"      : True,
        "kategori"   : "Berat",
        "kalori"     : 650,
        "harga"      : 25,
        "budget"     : "sedang",
    },
    "Rendang": {
        "deskripsi"  : ["kering", "daging", "pedas", "gurih"],
        "tekstur"    : "kering",
        "rasa"       : ["gurih", "pedas"],
        "pedas"      : True,
        "kategori"   : "Berat",
        "kalori"     : 420,
        "harga"      : 30,
        "budget"     : "sedang",
    },
    "Pecel Lele": {
        "deskripsi"  : ["kering", "ikan", "goreng", "pedas"],
        "tekstur"    : "kering",
        "rasa"       : ["gurih", "pedas"],
        "pedas"      : True,
        "kategori"   : "Berat",
        "kalori"     : 480,
        "harga"      : 17,
        "budget"     : "murah",
    },
    "Gado-gado": {
        "deskripsi"  : ["sehat", "sayur", "segar", "kacang"],
        "tekstur"    : "kering",
        "rasa"       : ["manis", "gurih"],
        "pedas"      : False,
        "kategori"   : "Ringan",
        "kalori"     : 280,
        "harga"      : 13,
        "budget"     : "murah",
    },
    "Siomay": {
        "deskripsi"  : ["sehat", "kukus", "kacang", "segar"],
        "tekstur"    : "kukus",
        "rasa"       : ["gurih", "manis"],
        "pedas"      : False,
        "kategori"   : "Camilan",
        "kalori"     : 200,
        "harga"      : 12,
        "budget"     : "murah",
    },
    "Martabak": {
        "deskripsi"  : ["manis", "gurih", "goreng", "tebal"],
        "tekstur"    : "kering",
        "rasa"       : ["manis", "gurih"],
        "pedas"      : False,
        "kategori"   : "Camilan",
        "kalori"     : 380,
        "harga"      : 22,
        "budget"     : "sedang",
    },
    "Pisang Goreng": {
        "deskripsi"  : ["manis", "goreng", "ringan", "cemilan"],
        "tekstur"    : "kering",
        "rasa"       : ["manis"],
        "pedas"      : False,
        "kategori"   : "Camilan",
        "kalori"     : 150,
        "harga"      : 8,
        "budget"     : "murah",
    },
    "Es Teh": {
        "deskripsi"  : ["minuman", "segar", "dingin", "manis"],
        "tekstur"    : "minuman",
        "rasa"       : ["manis", "segar"],
        "pedas"      : False,
        "kategori"   : "Minuman",
        "kalori"     : 80,
        "harga"      : 5,
        "budget"     : "murah",
    },
    "Jus Alpukat": {
        "deskripsi"  : ["minuman", "segar", "manis", "sehat"],
        "tekstur"    : "minuman",
        "rasa"       : ["manis", "creamy"],
        "pedas"      : False,
        "kategori"   : "Minuman",
        "kalori"     : 200,
        "harga"      : 12,
        "budget"     : "murah",
    },
    "Rawon": {
        "deskripsi"  : ["berkuah", "daging", "hitam", "gurih"],
        "tekstur"    : "berkuah",
        "rasa"       : ["gurih", "asin"],
        "pedas"      : False,
        "kategori"   : "Berat",
        "kalori"     : 400,
        "harga"      : 22,
        "budget"     : "sedang",
    },
    "Opor Ayam": {
        "deskripsi"  : ["berkuah", "ayam", "santan", "gurih"],
        "tekstur"    : "berkuah",
        "rasa"       : ["gurih", "manis"],
        "pedas"      : False,
        "kategori"   : "Berat",
        "kalori"     : 380,
        "harga"      : 20,
        "budget"     : "murah",
    },
}

# Kamus pemetaan kata kunci input bebas
KATA_KUNCI = {
    "berkuah"  : {"tekstur": "berkuah"},
    "kuah"     : {"tekstur": "berkuah"},
    "sup"      : {"tekstur": "berkuah"},
    "kering"   : {"tekstur": "kering"},
    "goreng"   : {"deskripsi": "goreng"},
    "kukus"    : {"tekstur": "kukus"},
    "pedas"    : {"pedas": True},
    "tidak pedas": {"pedas": False},
    "ga pedas" : {"pedas": False},
    "nggak pedas": {"pedas": False},
    "manis"    : {"rasa": "manis"},
    "gurih"    : {"rasa": "gurih"},
    "segar"    : {"rasa": "segar"},
    "sehat"    : {"deskripsi": "sehat"},
    "sayur"    : {"deskripsi": "sayur"},
    "daging"   : {"deskripsi": "daging"},
    "ayam"     : {"deskripsi": "ayam"},
    "ikan"     : {"deskripsi": "ikan"},
    "mie"      : {"deskripsi": "mie"},
    "nasi"     : {"deskripsi": "nasi"},
    "minuman"  : {"tekstur": "minuman"},
    "murah"    : {"budget": "murah"},
    "hemat"    : {"budget": "murah"},
    "sedang"   : {"budget": "sedang"},
    "mahal"    : {"budget": "mahal"},
    "ringan"   : {"kategori": "Ringan"},
    "cemilan"  : {"kategori": "Camilan"},
    "camilan"  : {"kategori": "Camilan"},
    "berat"    : {"kategori": "Berat"},
    "hangat"   : {"deskripsi": "hangat"},
    "dingin"   : {"deskripsi": "dingin"},
    "creamy"   : {"rasa": "creamy"},
    "santan"   : {"deskripsi": "santan"},
}

# ─────────────────────────────────────────────
#  2. GRAPH KEMIRIPAN (Adjacency List)
# ─────────────────────────────────────────────
RELASI = [
    ("Bakso",       "Soto Ayam",    9),
    ("Bakso",       "Mie Ayam",     8),
    ("Bakso",       "Rawon",        7),
    ("Soto Ayam",   "Opor Ayam",    8),
    ("Soto Ayam",   "Rawon",        7),
    ("Mie Ayam",    "Mie Goreng",   8),
    ("Mie Ayam",    "Bakso",        8),
    ("Nasi Goreng", "Mie Goreng",   9),
    ("Nasi Goreng", "Nasi Padang",  7),
    ("Nasi Goreng", "Pecel Lele",   6),
    ("Nasi Padang", "Rendang",      9),
    ("Nasi Padang", "Pecel Lele",   6),
    ("Rendang",     "Pecel Lele",   5),
    ("Gado-gado",   "Siomay",       8),
    ("Gado-gado",   "Jus Alpukat",  5),
    ("Siomay",      "Gado-gado",    8),
    ("Martabak",    "Pisang Goreng",7),
    ("Pisang Goreng","Es Teh",      6),
    ("Es Teh",      "Jus Alpukat",  8),
    ("Rawon",       "Opor Ayam",    7),
    ("Opor Ayam",   "Nasi Padang",  6),
]

def buat_graf():
    adj = defaultdict(dict)
    for a, b, w in RELASI:
        if a in MAKANAN and b in MAKANAN:
            adj[a][b] = w
            adj[b][a] = w
    return adj

# ─────────────────────────────────────────────
#  3. PARSER QUERY
# ─────────────────────────────────────────────
def parse_query(query: str) -> dict:
    q = query.lower()
    filters = {}

    if "tidak pedas" in q or "ga pedas" in q or "nggak pedas" in q:
        filters["pedas"] = False
    elif "pedas" in q:
        filters["pedas"] = True

    for kata, filter_val in KATA_KUNCI.items():
        if kata in ["pedas", "tidak pedas", "ga pedas", "nggak pedas"]:
            continue
        if kata in q:
            for k, v in filter_val.items():
                if k not in filters:
                    filters[k] = v
    return filters

# ─────────────────────────────────────────────
#  4. MESIN PENCARI
# ─────────────────────────────────────────────
def cari_makanan(filters: dict) -> list:
    hasil = []
    for nama, info in MAKANAN.items():
        skor = 0
        total = len(filters)
        if total == 0:
            hasil.append((nama, 100, info))
            continue

        for key, val in filters.items():
            if key == "tekstur" and info.get("tekstur") == val:
                skor += 1
            elif key == "pedas" and info.get("pedas") == val:
                skor += 1
            elif key == "budget" and info.get("budget") == val:
                skor += 1
            elif key == "kategori" and info.get("kategori") == val:
                skor += 1
            elif key == "rasa" and val in info.get("rasa", []):
                skor += 1
            elif key == "deskripsi" and val in info.get("deskripsi", []):
                skor += 1

        persen = round((skor / total) * 100)
        if persen > 0:
            hasil.append((nama, persen, info))

    # Pengurutan ganda: Skor persen tertinggi, lalu kalori terendah
    hasil.sort(key=lambda x: (-x[1], x[2]["kalori"]))
    return hasil

def rekomendasi_graph(nama_awal: str, adj: dict, top_n=4):
    tetangga = adj.get(nama_awal, {})
    diurutkan = sorted(tetangga.items(), key=lambda x: x[1], reverse=True)
    return diurutkan[:top_n]


# ─────────────────────────────────────────────
#  5. INTERFACE WEB STREAMLIT
# ─────────────────────────────────────────────

# --- PANEL SIDEBAR UTAMA (MULTIMEDIA) ---
with st.sidebar:
    st.header("🍳 Ruang Kreatif")
    
    # Menampilkan animasi koki jika pemuatan online berhasil
    if lottie_chef:
        st_lottie(lottie_chef, height=220, key="chef_anim")
    else:
        st.title("🍳👨‍🍳")
        
    st.divider()
    st.subheader("🎵 Musik Latar Belakang")
    st.caption("Putar instrumen lo-fi santai ini agar presentasi sistem lebih berkesan:")
    # Menyediakan backsound instrumental publik yang stabil
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
    
    st.divider()
    st.info("📊 **Statistik Struktur Data Graf:**\n"
            f"- Total Nodes (Simpul Makanan): `{len(MAKANAN)}` \n"
            f"- Total Edges (Relasi Kedekatan): `{len(RELASI)}` ")

# --- KONTEN HALAMAN UTAMA ---
st.title("🍕 WarmBites: Smart Food Finder")
st.caption("Aplikasi Sistem Rekomendasi Pintar Menggunakan Atribut Parsing & Traversal Struktur Data Graf")

# Contoh panduan kriteria pencarian untuk user
st.info("💡 **Contoh Kalimat Kriteria:** "
        "'*saya mau makanan berkuah yang hangat dan murah*', "
        "'*cari cemilan manis yang digoreng*', atau "
        "'*minuman segar dingin*'")

# Input teks pencarian interaktif
query = st.text_input("🔍 Bingung Mau Makan Apa? Tulis Kriteria Impianmu Di Sini:", 
                      placeholder="Ketik kriteria makanan di sini...",
                      value="makanan berkuah yang tidak pedas")

adj = buat_graf()

if query:
    filters = parse_query(query)
    
    if not filters:
        st.warning("⚠️ Kata kunci tidak dikenali sistem. Coba gunakan istilah baku: *berkuah, kering, pedas, manis, gurih, murah, sehat, ayam, daging, mie, dll.*")
    else:
        # Menampilkan badge data penanda token filter yang aktif
        st.write("✨ **Atribut Filter Terdeteksi Komputer:**")
        cols_filter = st.columns(len(filters))
        for idx, (k, v) in enumerate(filters.items()):
            cols_filter[idx].info(f"**{k.upper()}**: `{v}`")
            
        hasil = cari_makanan(filters)
        
        if not hasil:
            st.error("❌ Maaf, menu kuliner yang pas dengan kriteria tersebut tidak ditemukan di database.")
        else:
            st.divider()
            st.subheader(f"🎯 Hasil Rekomendasi Utama Teratas")
            
            tampil = hasil[:5]  # Mengambil 5 menu teratas
            
            # Efek selebrasi partikel balon jika ditemukan kecocokan mutlak (100%)
            if tampil[0][1] == 100:
                st.balloons()
                st.toast("🎉 Menemukan kecocokan rasa sempurna 100%!", icon="🔥")
            
            # Render kartu makanan bergaya modern dengan HTML/CSS
            for i, (nama, skor, info) in enumerate(tampil, 1):
                rasa_str = ", ".join(info['rasa'])
                pedas_str = "Ya" if info['pedas'] else "Tidak"
                
                card_html = f"""
                <div class="food-card">
                    <span class="match-badge">🎯 Kesesuaian: {skor}%</span>
                    <h3 style="margin: 0 0 10px 0; color: #333;">{i}. {nama}</h3>
                    <p style="margin: 0; color: #555; font-size: 14px; line-height: 1.6;">
                        • 📦 <b>Kategori:</b> {info['kategori']} | 
                        • 🔥 <b>Energi:</b> {info['kalori']} Kkal | 
                        • 💰 <b>Estimasi Harga:</b> Rp{info['harga']}.000 ({info['budget'].capitalize()}) <br>
                        • 🌶️ <b>Karakteristik Rasa:</b> {rasa_str} (Pedas: {pedas_str})
                    </p>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
            if len(hasil) > 5:
                st.caption(f"*...dan {len(hasil)-5} pilihan menu lain yang juga cocok tersedia di sistem.*")
                
            # ─────────────────────────────────────────────
            #  LOGIKA PENELUSURAN GRAF LANJUTAN (BFS NEIGHBORS)
            # ─────────────────────────────────────────────
            makanan_terbaik = tampil[0][0]
            rek_graph = rekomendasi_graph(makanan_terbaik, adj)
            
            # Memfilter rekomendasi graf agar tidak duplikat dengan menu utama di atas
            menu_utama_names = [x[0] for x in tampil]
            rek_graph_filtered = [r for r in rek_graph if r[0] not in menu_utama_names]
            
            if rek_graph_filtered:
                st.write("")
                st.subheader(f"✨ Hubungan Jaringan Graf: Karena Kamu Suka {makanan_terbaik}")
                st.caption("Menu alternatif di bawah ini disarankan berdasarkan jalur konektivitas terkuat (bobot kedekatan tertinggi) pada struktur data graf:")
                
                cols_graph = st.columns(len(rek_graph_filtered))
                for idx_col, (nama_rek, bobot) in enumerate(rek_graph_filtered):
                    info_rek = MAKANAN.get(nama_rek, {})
                    if info_rek:
                        with cols_graph[idx_col]:
                            st.success(f"🍱 **{nama_rek}**")
                            st.markdown(f"• 🤝 Kemiripan Graf: `{bobot}/10`  \n"
                                        f"• 🔥 Energi: `{info_rek['kalori']} Kkal`  \n"
                                        f"• 💰 Harga: `Rp{info_rek['harga']}.000`")
