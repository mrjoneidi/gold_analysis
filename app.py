import requests
from bs4 import BeautifulSoup
import streamlit as st
import time

st.set_page_config(page_title="تحلیل بازار طلا", page_icon="💰", layout="centered")

# استایل راست‌چین
st.markdown("""
    <style>
    body { direction: rtl; text-align: right; font-family: Tahoma; }
    .stButton button { width: 100%; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

st.title("💰 تحلیل بازار طلا")

def fetch_data():
    url = "https://www.tgju.org/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    def get_price(slug):
        row = soup.find("tr", {"data-market-nameslug": slug})
        if row:
            tds = row.find_all("td")
            price = tds[0].text.strip().replace(",", "")
            return float(price)
        return 0

    mesghal_price = get_price("mesghal")
    ons_price = get_price("ons")
    dollar_price = get_price("price_dollar_rl")

    mozane_dakhel = mesghal_price
    mozane_jahani = (ons_price * dollar_price) / 9.5742
    tafazol = mozane_dakhel - mozane_jahani

    if abs(tafazol) < 100000:
        action = ("✅ پیشنهاد: خرید", "green")
    elif 100000 <= abs(tafazol) <= 500000:
        action = ("🔵 پیشنهاد: صبر", "blue")
    else:
        action = ("❌ پیشنهاد: فروش", "red")

    return mozane_dakhel, mozane_jahani, tafazol, action

auto_refresh = st.checkbox("آپدیت خودکار هر ۳۰ ثانیه", value=False)

def display_data():
    try:
        mozane_dakhel, mozane_jahani, tafazol, action = fetch_data()

        st.subheader("📊 قیمت‌ها")
        st.write(f"**مظنه داخل:** {mozane_dakhel:,.0f} تومان")
        st.write(f"**مظنه جهانی:** {mozane_jahani:,.0f} تومان")
        st.write(f"**تفاضل:** {tafazol:,.0f} تومان")

        st.markdown(f"<h3 style='color:{action[1]}'>{action[0]}</h3>", unsafe_allow_html=True)
        st.caption(f"آخرین بروزرسانی: {time.strftime('%H:%M:%S')}")
    except Exception as e:
        st.error(f"خطا در دریافت اطلاعات: {e}")

if auto_refresh:
    # این باعث میشه صفحه هر ۳۰ ثانیه رفرش بشه
    st.experimental_rerun()
    time.sleep(30)

display_data()

if not auto_refresh:
    if st.button("🔄 بروزرسانی", key="refresh_btn"):
        display_data()
