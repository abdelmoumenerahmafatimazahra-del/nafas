# ============================================================
#  🌬️ NAFAS — E-commerce configurable (v1.0)
#  ✓ Titre d'accueil + identité + description modifiables
#  ✓ Accès vendeur secret ✓ Sauvegarde ✓ Commandes ✓ Livraison
# ============================================================
import streamlit as st
import base64, os, json
from datetime import datetime

st.set_page_config(page_title="NAFAS — Ma Boutique", page_icon="🌿",
                   layout="wide", initial_sidebar_state="expanded")

# ─────────────────────────────────────────────
#  PARAMÈTRES  (à personnaliser avant de livrer)
# ─────────────────────────────────────────────
VENDOR_PASSWORD = "nafas2024"          # 🔑 mot de passe vendeur
VENDOR_URL_KEY  = "nafas"              # 🔗 lien secret : .../?v=nafas
DATA_DIR = "/content/drive/MyDrive/NAFAS" if os.path.isdir("/content/drive/MyDrive/NAFAS") else "."
PRODUCTS_FILE = os.path.join(DATA_DIR, "produits.json")
ORDERS_FILE   = os.path.join(DATA_DIR, "commandes.json")
DELIVERY_FILE = os.path.join(DATA_DIR, "livraison.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

WILAYAS = [
 "01 Adrar","02 Chlef","03 Laghouat","04 Oum El Bouaghi","05 Batna","06 Béjaïa",
 "07 Biskra","08 Béchar","09 Blida","10 Bouira","11 Tamanrasset","12 Tébessa",
 "13 Tlemcen","14 Tiaret","15 Tizi Ouzou","16 Alger","17 Djelfa","18 Jijel",
 "19 Sétif","20 Saïda","21 Skikda","22 Sidi Bel Abbès","23 Annaba","24 Guelma",
 "25 Constantine","26 Médéa","27 Mostaganem","28 M'Sila","29 Mascara","30 Ouargla",
 "31 Oran","32 El Bayadh","33 Illizi","34 Bordj Bou Arréridj","35 Boumerdès",
 "36 El Tarf","37 Tindouf","38 Tissemsilt","39 El Oued","40 Khenchela","41 Souk Ahras",
 "42 Tipaza","43 Mila","44 Aïn Defla","45 Naâma","46 Aïn Témouchent","47 Ghardaïa",
 "48 Relizane","49 El M'Ghair","50 El Meniaa","51 Ouled Djellal","52 Bordj Badji Mokhtar",
 "53 Béni Abbès","54 Timimoun","55 Touggourt","56 Djanet","57 In Salah","58 In Guezzam",
]

# ─────────────────────────────────────────────
#  SAUVEGARDE / CHARGEMENT
# ─────────────────────────────────────────────
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_products():
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.products, f, ensure_ascii=False, indent=2)

def save_order(order):
    orders = load_json(ORDERS_FILE, [])
    orders.append(order)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def load_delivery():
    data = load_json(DELIVERY_FILE, None)
    if data and "prices" in data:
        prices = {w: int(data["prices"].get(w, 500)) for w in WILAYAS}
        return prices, int(data.get("threshold", 5000))
    return {w: 500 for w in WILAYAS}, 5000

def save_delivery():
    with open(DELIVERY_FILE, "w", encoding="utf-8") as f:
        json.dump({"prices": st.session_state.delivery,
                   "threshold": st.session_state.free_threshold},
                  f, ensure_ascii=False, indent=2)

def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump({"name": st.session_state.shop_name,
                   "slogan": st.session_state.shop_slogan,
                   "description": st.session_state.shop_description,
                   "hero_main": st.session_state.shop_hero_main,
                   "hero_accent": st.session_state.shop_hero_accent,
                   "logo_b64": st.session_state.shop_logo},
                  f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
:root{
  --forest:#1E3A14; --sage:#5A8A3C; --mint:#8FBB6E; --ivory:#F8F4EC;
  --parchment:#EDE8DD; --amber:#C9914A; --amber-lt:#F5E6C8;
  --text:#2A2A2A; --muted:#7A7A6A; --card-bg:#FFFFFF; --border:#DDD8CC;
}
*{box-sizing:border-box;}
html,.stApp{background:var(--ivory); font-family:'Lato',sans-serif; color:var(--text);}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#EBF0E3 0%,#E0EBD5 100%); border-right:1px solid #C5D8B0;}
.hero-wrap{position:relative; background:var(--forest); border-radius:22px; overflow:hidden; padding:64px 52px; margin-bottom:40px;}
.hero-eyebrow{font-size:0.72em; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:var(--mint); margin-bottom:18px;}
.hero-title{font-family:'Playfair Display',serif; font-size:clamp(2.4em,5vw,4em); font-weight:700; color:var(--ivory); line-height:1.1; margin-bottom:18px;}
.hero-title em{color:var(--amber); font-style:italic;}
.hero-rule{width:56px; height:2px; background:var(--amber); margin-bottom:20px;}
.hero-body{font-size:1em; font-weight:300; color:#A8C898; max-width:480px; line-height:1.8;}
.about-box{background:white; border:1px solid var(--border); border-radius:18px; padding:34px 40px; margin-bottom:42px; text-align:center;}
.about-text{font-family:'Lato'; color:var(--text); font-size:1.02em; line-height:1.9; max-width:720px; margin:0 auto; white-space:pre-line;}
.sec-eyebrow{font-size:0.72em; font-weight:700; letter-spacing:4px; text-transform:uppercase; color:var(--sage); text-align:center; margin-bottom:8px;}
.sec-title{font-family:'Playfair Display',serif; font-size:2em; color:var(--forest); text-align:center; font-weight:600; margin-bottom:12px;}
.sec-rule{width:44px; height:2px; background:linear-gradient(to right,var(--sage),var(--amber)); margin:0 auto 34px; border-radius:1px;}
.prod-card{background:var(--card-bg); border:1px solid var(--border); border-radius:18px; overflow:hidden; transition:all .3s; margin-bottom:6px;}
.prod-card:hover{box-shadow:0 12px 36px rgba(30,58,20,.13); transform:translateY(-5px);}
.prod-thumb{background:linear-gradient(135deg,#E8F2DC,#D0E4B8); display:flex; align-items:center; justify-content:center; height:170px; font-size:4.6em; overflow:hidden;}
.prod-thumb img{width:100%; height:100%; object-fit:cover;}
.prod-cat-pill{position:absolute; top:12px; left:12px; background:rgba(255,255,255,.88); color:var(--sage); font-size:.68em; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; padding:4px 11px; border-radius:20px;}
.prod-body{padding:18px 20px 20px;}
.prod-name{font-family:'Playfair Display',serif; font-size:1.12em; color:var(--forest); font-weight:600; margin-bottom:8px;}
.prod-desc{color:var(--muted); font-size:.84em; line-height:1.7; margin-bottom:12px;}
.prod-price-da{font-family:'Playfair Display',serif; font-size:1.4em; font-weight:700; color:var(--forest);}
.cart-total-box{background:linear-gradient(135deg,var(--forest),var(--sage)); border-radius:16px; padding:22px 26px; margin-top:18px; color:white;}
.ctl-row{display:flex; justify-content:space-between; font-size:.9em; padding:3px 0; opacity:.92;}
.ct-amount{font-family:'Playfair Display',serif; font-size:2.1em; font-weight:700; text-align:right; margin-top:8px; border-top:1px solid rgba(255,255,255,.25); padding-top:8px;}
.success-wrap{background:linear-gradient(135deg,#EAF4D8,#D8EEC0); border:2px solid var(--sage); border-radius:20px; padding:40px 34px; text-align:center;}
.empty-cart{text-align:center; padding:55px 20px; color:var(--muted);}
.order-card{background:var(--card-bg); border:1px solid var(--border); border-radius:14px; padding:18px 20px; margin-bottom:12px;}
.stButton>button{background:linear-gradient(135deg,var(--forest),var(--sage))!important; color:#F0ECE4!important; border:none!important; border-radius:30px!important; padding:10px 24px!important; font-weight:700!important; letter-spacing:1.2px!important; text-transform:uppercase!important; width:100%!important; transition:all .25s!important;}
.stButton>button:hover{background:linear-gradient(135deg,var(--sage),var(--mint))!important; transform:translateY(-2px)!important;}
.amber-pill{display:inline-block; background:var(--amber-lt); color:var(--amber); font-size:.72em; font-weight:700; letter-spacing:1px; padding:3px 12px; border-radius:20px; border:1px solid rgba(201,145,74,.25);}
</style>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE  (charge l'identité sauvegardée)
# ─────────────────────────────────────────────
_settings = load_json(SETTINGS_FILE, {})

if "shop_name" not in st.session_state:
    st.session_state.shop_name = _settings.get("name", "NAFAS")
if "shop_slogan" not in st.session_state:
    st.session_state.shop_slogan = _settings.get("slogan", "Respirez la nature, vivez l'harmonie")
if "shop_hero_main" not in st.session_state:
    st.session_state.shop_hero_main = _settings.get("hero_main", "La nature, source de")
if "shop_hero_accent" not in st.session_state:
    st.session_state.shop_hero_accent = _settings.get("hero_accent", "bien-être")
if "shop_description" not in st.session_state:
    st.session_state.shop_description = _settings.get("description",
        "Bienvenue chez NAFAS 🌿\n\n"
        "Nous proposons des produits naturels d'aromathérapie et de bien-être, "
        "sélectionnés avec soin pour prendre soin de votre corps et de votre esprit. "
        "Huiles essentielles, tisanes, soins naturels… respirez la nature, vivez l'harmonie.")

if "shop_logo" not in st.session_state:
    if _settings.get("logo_b64"):
        st.session_state.shop_logo = _settings["logo_b64"]
    elif os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            st.session_state.shop_logo = base64.b64encode(f.read()).decode()
    else:
        st.session_state.shop_logo = None

if "products" not in st.session_state:
    st.session_state.products = load_json(PRODUCTS_FILE, [])
if "next_id" not in st.session_state:
    st.session_state.next_id = max([p["id"] for p in st.session_state.products], default=0) + 1
if "delivery" not in st.session_state:
    st.session_state.delivery, st.session_state.free_threshold = load_delivery()

if "cart" not in st.session_state: st.session_state.cart = {}
if "page" not in st.session_state: st.session_state.page = "🏠 Accueil"
if "order_confirmed" not in st.session_state: st.session_state.order_confirmed = False
if "order_data" not in st.session_state: st.session_state.order_data = None
if "vendor_unlocked" not in st.session_state: st.session_state.vendor_unlocked = False

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def get_product(pid): return next((p for p in st.session_state.products if p["id"] == pid), None)
def cart_count(): return sum(st.session_state.cart.values())
def cart_total():
    return sum(get_product(pid)["price"] * qty
               for pid, qty in st.session_state.cart.items() if get_product(pid))
def add_to_cart(pid): st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
def remove_item(pid): st.session_state.cart.pop(pid, None)
def set_qty(pid, qty):
    if qty <= 0: remove_item(pid)
    else: st.session_state.cart[pid] = qty
def file_to_b64(f): return base64.b64encode(f.read()).decode() if f else None
def thumb_html(p):
    if p.get("img_b64"):
        return f'<img src="data:image/png;base64,{p["img_b64"]}">'
    return p.get("emoji", "🌿")

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    logo = st.session_state.shop_logo
    logo_html = (f'<img src="data:image/png;base64,{logo}" style="width:72px;height:72px;'
                 f'object-fit:contain;margin-bottom:8px;">' if logo else
                 '<div style="font-size:2.4em;margin-bottom:8px;">🌿</div>')
    st.markdown(f"""
    <div style="padding:26px 20px 22px; text-align:center;">
        {logo_html}
        <div style="font-family:'Playfair Display',serif; color:#1E3A14;
                    font-size:1.35em; font-weight:700;">{st.session_state.shop_name}</div>
        <div style="font-size:0.64em; letter-spacing:2px; color:#5A8A3C;
                    font-weight:700; margin-top:4px;">{st.session_state.shop_slogan}</div>
    </div>
    <hr style="border:none; border-top:1px solid #C5D8B0; margin:0 16px 16px;">
    """, unsafe_allow_html=True)

    n = cart_count()
    nav = ["🏠 Accueil", "🌱 Catalogue", f"🛒 Panier ({n})"]
    if st.session_state.vendor_unlocked:
        nav += ["⚙️ Espace Vendeur", "📩 Commandes"]
    st.session_state.page = st.radio("nav", nav, label_visibility="collapsed")

    show_access = (st.query_params.get("v") == VENDOR_URL_KEY) or st.session_state.vendor_unlocked
    if show_access:
        st.markdown("<hr style='border:none; border-top:1px solid #C5D8B0; margin:18px 16px;'>", unsafe_allow_html=True)
        with st.expander("🔒 Accès vendeur", expanded=not st.session_state.vendor_unlocked):
            if st.session_state.vendor_unlocked:
                st.success("✅ Connecté en mode vendeur")
                if st.button("🚪 Se déconnecter"):
                    st.session_state.vendor_unlocked = False
                    st.session_state.page = "🏠 Accueil"
                    st.rerun()
            else:
                pwd = st.text_input("Mot de passe", type="password", key="vendor_pwd")
                if st.button("Entrer"):
                    if pwd == VENDOR_PASSWORD:
                        st.session_state.vendor_unlocked = True
                        st.rerun()
                    else:
                        st.error("❌ Mot de passe incorrect")

# ═════════════════════════════════════════════
#  PAGE — ESPACE VENDEUR
# ═════════════════════════════════════════════
if "Espace Vendeur" in st.session_state.page:
    st.markdown("""<div class="sec-eyebrow">Configuration</div>
    <div class="sec-title">⚙️ Espace Vendeur</div><div class="sec-rule"></div>""", unsafe_allow_html=True)
    st.info("Configurez votre boutique. Pensez à cliquer sur Enregistrer après vos modifications.")

    # ── 🏷️ IDENTITÉ, TITRE & DESCRIPTION ──
    st.markdown("### 🏷️ Identité & page d'accueil")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.shop_name = st.text_input("Nom de la boutique", st.session_state.shop_name)
        st.session_state.shop_slogan = st.text_input("Slogan", st.session_state.shop_slogan)
    with c2:
        up_logo = st.file_uploader("Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if up_logo:
            st.session_state.shop_logo = file_to_b64(up_logo)
        if st.session_state.shop_logo:
            st.image(base64.b64decode(st.session_state.shop_logo), width=90)

    st.markdown("**🖼️ Grand titre de la page d'accueil**")
    h1, h2 = st.columns([2, 1])
    with h1:
        st.session_state.shop_hero_main = st.text_input(
            "Titre principal", st.session_state.shop_hero_main,
            help="La grande phrase affichée sur l'accueil.")
    with h2:
        st.session_state.shop_hero_accent = st.text_input(
            "Mot en valeur (couleur ambre)", st.session_state.shop_hero_accent)
    st.caption(f"Aperçu : {st.session_state.shop_hero_main} *{st.session_state.shop_hero_accent}*.")

    st.session_state.shop_description = st.text_area(
        "📝 Description de la boutique (texte affiché sur l'accueil)",
        st.session_state.shop_description, height=160,
        help="Présentez votre boutique : qui vous êtes, ce que vous vendez, vos valeurs…")

    if st.button("💾 Enregistrer l'identité de la boutique"):
        save_settings()
        st.success("✅ Identité, titre & description enregistrés !")

    st.markdown("---")
    st.markdown("### ➕ Ajouter un produit")
    with st.form("add_product", clear_on_submit=True):
        a, b = st.columns(2)
        with a:
            name = st.text_input("Nom du produit *")
            category = st.text_input("Catégorie", "Général")
            price = st.number_input("Prix (DA) *", min_value=0, step=50)
        with b:
            emoji = st.text_input("Emoji (si pas de photo)", "🌿")
            volume = st.text_input("Volume / format", "")
            img = st.file_uploader("Photo produit (optionnel)", type=["png", "jpg", "jpeg"])
        desc = st.text_area("Description")
        if st.form_submit_button("✨ Ajouter le produit"):
            if not name.strip() or price <= 0:
                st.error("⚠️ Le nom et un prix valide sont obligatoires.")
            else:
                st.session_state.products.append({
                    "id": st.session_state.next_id, "name": name.strip(),
                    "category": category.strip() or "Général", "price": int(price),
                    "emoji": emoji.strip() or "🌿", "volume": volume.strip(),
                    "description": desc.strip(), "img_b64": file_to_b64(img),
                })
                st.session_state.next_id += 1
                save_products()
                st.success(f"🌿 « {name} » ajouté et sauvegardé !")
                st.rerun()

    st.markdown(f"### 📦 Mes produits ({len(st.session_state.products)})")
    if not st.session_state.products:
        st.warning("Aucun produit pour l'instant.")
    for p in st.session_state.products:
        col1, col2, col3 = st.columns([0.5, 4, 1])
        col1.markdown(f"<div style='font-size:1.8em'>{p['emoji']}</div>", unsafe_allow_html=True)
        col2.markdown(f"**{p['name']}** — {p['price']:,} DA  \n<span style='color:#7A7A6A;font-size:.85em'>{p['category']}</span>", unsafe_allow_html=True)
        if col3.button("🗑️", key=f"del_{p['id']}"):
            st.session_state.products = [x for x in st.session_state.products if x["id"] != p["id"]]
            st.session_state.cart.pop(p["id"], None)
            save_products()
            st.rerun()

    # ── 🚚 LIVRAISON PAR WILAYA ──
    st.markdown("---")
    st.markdown("### 🚚 Frais de livraison par wilaya")
    st.session_state.free_threshold = st.number_input(
        "🎁 Livraison gratuite à partir de (DA) — mettez 0 pour désactiver",
        min_value=0, step=500, value=int(st.session_state.free_threshold))
    st.caption("Modifiez le prix de chaque wilaya dans le tableau puis cliquez sur Enregistrer.")
    rows = [{"Wilaya": w, "Prix (DA)": int(st.session_state.delivery.get(w, 500))} for w in WILAYAS]
    edited = st.data_editor(rows, hide_index=True, use_container_width=True,
                            disabled=["Wilaya"], height=380, key="delivery_editor")
    if st.button("💾 Enregistrer les frais de livraison"):
        st.session_state.delivery = {r["Wilaya"]: int(r["Prix (DA)"] or 0) for r in edited}
        save_delivery()
        st.success("✅ Frais de livraison enregistrés !")

# ═════════════════════════════════════════════
#  PAGE — COMMANDES (vendeur)
# ═════════════════════════════════════════════
elif "Commandes" in st.session_state.page:
    st.markdown("""<div class="sec-eyebrow">Suivi des ventes</div>
    <div class="sec-title">📩 Commandes reçues</div><div class="sec-rule"></div>""", unsafe_allow_html=True)
    orders = load_json(ORDERS_FILE, [])
    if not orders:
        st.info("Aucune commande pour l'instant.")
    else:
        ca = sum(o["total"] for o in orders)
        m1, m2 = st.columns(2)
        m1.metric("Nombre de commandes", len(orders))
        m2.metric("Chiffre d'affaires", f"{ca:,} DA")
        st.download_button("⬇️ Télécharger les commandes (JSON)",
                           data=json.dumps(orders, ensure_ascii=False, indent=2),
                           file_name="commandes.json", mime="application/json")
        st.markdown("---")
        for o in reversed(orders):
            articles = "<br>".join(f"• {it['emoji']} {it['name']} × {it['qty']} = {it['subtotal']:,} DA"
                                   for it in o["items"])
            liv = "Offerte 🎁" if o.get("delivery_fee", 0) == 0 else f"{o.get('delivery_fee',0):,} DA"
            st.markdown(f"""<div class="order-card">
                <div style="font-weight:700; color:#1E3A14;">🧾 {o['date']} — {o['total']:,} DA</div>
                <div style="font-size:.88em; color:#555; margin-top:6px;">
                    👤 {o['nom']} &nbsp;|&nbsp; 📞 {o['tel']}<br>
                    📍 {o['adresse']}<br>
                    🚚 Wilaya : {o.get('wilaya','—')} &nbsp;|&nbsp; Livraison : {liv}<br>
                    💳 {o['payment']}<br><br>{articles}<br>
                    <em>Sous-total : {o.get('subtotal', o['total']):,} DA</em>
                </div></div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  PAGE — ACCUEIL
# ═════════════════════════════════════════════
elif "Accueil" in st.session_state.page:
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-eyebrow">✦ {st.session_state.shop_name} ✦</div>
        <div class="hero-title">{st.session_state.shop_hero_main} <em>{st.session_state.shop_hero_accent}</em>.</div>
        <div class="hero-rule"></div>
        <div class="hero-body">{st.session_state.shop_slogan}</div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.shop_description.strip():
        st.markdown(f"""<div class="about-box">
            <div class="sec-eyebrow">À propos</div>
            <div class="about-text">{st.session_state.shop_description}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="sec-eyebrow">Sélection</div>
    <div class="sec-title">Nos produits phares</div><div class="sec-rule"></div>""", unsafe_allow_html=True)
    if not st.session_state.products:
        st.info("🛍️ La boutique n'a pas encore de produits.")
    else:
        for col, p in zip(st.columns(4), st.session_state.products[:4]):
            with col:
                st.markdown(f"""
                <div style="background:white; border:1px solid var(--border); border-radius:15px;
                            padding:20px 14px; text-align:center; margin-bottom:12px;">
                    <div style="font-size:2.8em; margin-bottom:8px;">{p['emoji']}</div>
                    <div class="amber-pill">{p['category']}</div>
                    <div style="font-family:'Playfair Display',serif; color:#1E3A14; font-size:1em;
                                font-weight:600; margin:9px 0 5px;">{p['name']}</div>
                    <div style="font-weight:700; color:#5A8A3C;">{p['price']:,} DA</div>
                </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  PAGE — CATALOGUE
# ═════════════════════════════════════════════
elif "Catalogue" in st.session_state.page:
    st.markdown("""<div class="sec-eyebrow">Notre sélection</div>
    <div class="sec-title">Catalogue</div><div class="sec-rule"></div>""", unsafe_allow_html=True)
    if not st.session_state.products:
        st.info("🛍️ Aucun produit disponible pour le moment.")
    else:
        cats = ["Tous"] + list(dict.fromkeys(p["category"] for p in st.session_state.products))
        cat = st.selectbox("Filtrer par catégorie :", cats)
        items = st.session_state.products if cat == "Tous" else [p for p in st.session_state.products if p["category"] == cat]
        for start in range(0, len(items), 3):
            for col, p in zip(st.columns(3, gap="medium"), items[start:start+3]):
                with col:
                    qty = st.session_state.cart.get(p["id"], 0)
                    st.markdown(f"""
                    <div class="prod-card">
                        <div class="prod-thumb" style="position:relative;">
                            <div class="prod-cat-pill">{p['category']}</div>{thumb_html(p)}
                        </div>
                        <div class="prod-body">
                            <div class="prod-name">{p['name']}</div>
                            <div class="prod-desc">{p['description'] or '—'}</div>
                            <div class="prod-price-da">{p['price']:,} DA</div>
                            <div style="font-size:.75em;color:var(--muted);margin-top:6px;">{p['volume']}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    if qty > 0:
                        st.success(f"✅ Panier (×{qty})")
                        x, y, z = st.columns(3)
                        if x.button("➖", key=f"d_{p['id']}"): set_qty(p["id"], qty-1); st.rerun()
                        y.markdown(f"<div style='text-align:center;font-weight:700;padding:8px'>{qty}</div>", unsafe_allow_html=True)
                        if z.button("➕", key=f"i_{p['id']}"): add_to_cart(p["id"]); st.rerun()
                    else:
                        if st.button("🛒 Ajouter", key=f"a_{p['id']}"):
                            add_to_cart(p["id"]); st.rerun()
                    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  PAGE — PANIER & COMMANDE
# ═════════════════════════════════════════════
elif "Panier" in st.session_state.page:
    if st.session_state.order_confirmed and st.session_state.order_data:
        o = st.session_state.order_data
        st.markdown(f"""<div class="success-wrap">
            <div style="font-size:3.5em;">🎉</div>
            <div style="font-family:'Playfair Display',serif; font-size:1.8em; color:#1E3A14;">Commande confirmée !</div>
            <div style="color:#7A7A6A; margin-top:8px;">Merci <strong>{o['nom']}</strong>, livraison vers
            <strong>{o['wilaya']}</strong>. Nous vous appelons au <strong>{o['tel']}</strong>.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"Sous-total : **{o['subtotal']:,} DA** · Livraison : **{o['delivery_fee']:,} DA** · "
                    f"Total : **{o['total']:,} DA** — {o['date']}")
        if st.button("🌱 Continuer mes achats"):
            st.session_state.order_confirmed = False; st.session_state.order_data = None
            st.session_state.cart = {}; st.rerun()

    elif not st.session_state.cart:
        st.markdown("""<div class="empty-cart"><div style="font-size:3.5em;">🛒</div>
        <div style="font-family:'Playfair Display',serif; font-size:1.5em; color:#5A8A3C;">Votre panier est vide</div></div>""", unsafe_allow_html=True)

    else:
        st.markdown("""<div class="sec-eyebrow">Étape 1 → 2</div>
        <div class="sec-title">Mon panier & commande</div><div class="sec-rule"></div>""", unsafe_allow_html=True)
        left, right = st.columns([1, 1.05], gap="large")
        with left:
            for pid, qty in list(st.session_state.cart.items()):
                p = get_product(pid)
                if not p: continue
                st.markdown(f"**{p['emoji']} {p['name']}** — {p['price']:,} DA × {qty} = **{p['price']*qty:,} DA**")
                a, b, c, d = st.columns(4)
                if a.button("➖", key=f"cd_{pid}"): set_qty(pid, qty-1); st.rerun()
                b.markdown(f"<div style='text-align:center;font-weight:700;padding:6px'>{qty}</div>", unsafe_allow_html=True)
                if c.button("➕", key=f"ci_{pid}"): add_to_cart(pid); st.rerun()
                if d.button("🗑️", key=f"cx_{pid}"): remove_item(pid); st.rerun()

            subtotal = cart_total()
            st.markdown("#### 🚚 Livraison")
            wilaya = st.selectbox("Wilaya de livraison", WILAYAS, key="wilaya_select")
            delivery_fee = int(st.session_state.delivery.get(wilaya, 0))
            free_applied = st.session_state.free_threshold and subtotal >= st.session_state.free_threshold
            if free_applied:
                delivery_fee = 0
            grand_total = subtotal + delivery_fee

            ship_txt = "Offerte 🎁" if free_applied else f"{delivery_fee:,} DA"
            reste = (st.session_state.free_threshold - subtotal) if st.session_state.free_threshold else 0
            hint = (f"<div class='ctl-row'><span>Plus que {reste:,} DA pour la livraison gratuite</span></div>"
                    if (st.session_state.free_threshold and not free_applied) else "")
            st.markdown(f"""<div class="cart-total-box">
                <div class="ctl-row"><span>Sous-total produits</span><span>{subtotal:,} DA</span></div>
                <div class="ctl-row"><span>Livraison ({wilaya})</span><span>{ship_txt}</span></div>
                {hint}
                <div class="ct-amount">{grand_total:,} DA</div>
            </div>""", unsafe_allow_html=True)

        with right:
            with st.form("order"):
                st.markdown("**📦 Informations de livraison**")
                nom = st.text_input("Nom & prénom *")
                tel = st.text_input("Téléphone *")
                adr = st.text_area("Adresse complète *", height=90)
                pay = st.radio("Paiement", ["💵 À la livraison", "🏦 Virement CCP/Baridimob"])
                st.caption(f"Wilaya sélectionnée : **{wilaya}** · Total à payer : **{grand_total:,} DA**")
                if st.form_submit_button("✨ Valider ma commande"):
                    if not nom.strip() or not tel.strip() or not adr.strip():
                        st.error("⚠️ Nom, téléphone et adresse sont obligatoires.")
                    else:
                        items = []
                        for pid, qty in st.session_state.cart.items():
                            p = get_product(pid)
                            if p:
                                items.append({"name": p["name"], "emoji": p["emoji"], "qty": qty,
                                              "unit_price": p["price"], "subtotal": p["price"]*qty})
                        order = {"nom": nom.strip(), "tel": tel.strip(), "adresse": adr.strip(),
                                 "wilaya": wilaya, "payment": pay, "items": items,
                                 "subtotal": subtotal, "delivery_fee": delivery_fee,
                                 "total": grand_total,
                                 "date": datetime.now().strftime("%d/%m/%Y à %H:%M")}
                        save_order(order)
                        st.session_state.order_data = order
                        st.session_state.order_confirmed = True
                        st.rerun()
