import streamlit as st

st.set_page_config(page_title="توقعات كأس العالم 2026", layout="wide")
st.title("⚽ لعبة توقعات كأس العالم 2026")

# 1. المجموعات المحدثة بناءً على 664767981_1307360061509712_3936504344452919803_n.jpg
groups = {
    "المجموعة A": ["المكسيك", "جنوب إفريقيا", "كوريا الجنوبية", "التشيك"],
    "المجموعة B": ["كندا", "البوسنة", "قطر", "سويسرا"],
    "المجموعة C": ["البرازيل", "المغرب", "إسكتلندا", "هايتي"],
    "المجموعة D": ["الولايات المتحدة", "الباراغواي", "أستراليا", "تركيا"],
    "المجموعة E": ["ألمانيا", "الإكوادور", "ساحل العاج", "كوراساو"],
    "المجموعة F": ["هولندا", "اليابان", "السويد", "تونس"],
    "المجموعة G": ["بلجيكا", "مصر", "إيران", "نيوزيلندا"],
    "المجموعة H": ["إسبانيا", "الرأس الأخضر", "السعودية", "أوروغواي"],
    "المجموعة I": ["فرنسا", "السنغال", "العراق", "النرويج"],
    "المجموعة J": ["الأرجنتين", "الجزائر", "النمسا", "الأردن"],
    "المجموعة K": ["البرتغال", "جمهورية الكونغو الديمقراطية", "أوزبكستان", "كولومبيا"],
    "المجموعة L": ["إنجلترا", "كرواتيا", "غانا", "بنما"]
}

# دالة ذكية للمباريات
def play_bracket(teams, title):
    st.subheader(title)
    winners = []
    for i in range(0, len(teams), 2):
        col1, col2 = st.columns(2)
        winner = col1.radio(f"المباراة {i//2 + 1}: {teams[i]} vs {teams[i+1]}", [teams[i], teams[i+1]], key=f"{title}_{i}")
        winners.append(winner)
    return winners

# إدارة مراحل اللعبة
if 'stage' not in st.session_state: st.session_state.stage = 'groups'

# --- المجموعات ---
if st.session_state.stage == 'groups':
    st.info("اختاري المتصدر والوصيف لكل مجموعة، وحددي أفضل 8 ثوالث")
    winners, runners, thirds = {}, {}, []
    for g, t in groups.items():
        c1, c2, c3 = st.columns(3)
        winners[g] = c1.selectbox(f"{g} - المتصدر", t, key=f"{g}_1")
        runners[g] = c2.selectbox(f"{g} - الوصيف", t, key=f"{g}_2")
        thirds.append(c3.selectbox(f"{g} - الثالث", t, key=f"{g}_3"))
    
    selected_thirds = st.multiselect("اختاري أفضل 8 ثوالث:", thirds, max_selections=8)
    if st.button("تأكيد التأهل (دور الـ 32)"):
        if len(selected_thirds) == 8:
            st.session_state.round_32 = list(winners.values()) + list(runners.values()) + selected_thirds
            st.session_state.stage = 'round_32'
            st.rerun()

# --- الأدوار الإقصائية (الديناميكية) ---
elif st.session_state.stage == 'round_32':
    st.session_state.r16 = play_bracket(st.session_state.round_32, "دور الـ 32")
    if st.button("للـ 16"): st.session_state.stage = 'r16'; st.rerun()

elif st.session_state.stage == 'r16':
    st.session_state.qf = play_bracket(st.session_state.r16, "دور الـ 16")
    if st.button("للربع"): st.session_state.stage = 'qf'; st.rerun()

elif st.session_state.stage == 'qf':
    st.session_state.sf = play_bracket(st.session_state.qf, "ربع النهائي")
    if st.button("للنصف"): st.session_state.stage = 'sf'; st.rerun()

elif st.session_state.stage == 'sf':
    # نصف النهائي + الخاسرين للمركز الثالث
    sf_winners = play_bracket(st.session_state.sf, "نصف النهائي")
    losers = [t for t in st.session_state.sf if t not in sf_winners]
    st.session_state.finalists, st.session_state.third_place_match = sf_winners, losers
    if st.button("للمباريات النهائية"): st.session_state.stage = 'final'; st.rerun()

elif st.session_state.stage == 'final':
    third = play_bracket(st.session_state.third_place_match, "مباراة المركز الثالث")[0]
    champ = play_bracket(st.session_state.finalists, "النهائي الكبير")[0]
    if st.button("تتويج البطل"):
        st.balloons()
        st.success(f"🏆 البطل: {champ} | 🥉 المركز الثالث: {third}")
