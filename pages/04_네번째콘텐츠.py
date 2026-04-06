import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────
# 기본 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="📊 성적처리 시스템",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSV_PATH = "score.csv"

# ──────────────────────────────────────────────
# 한국인 이름 생성용 데이터
# ──────────────────────────────────────────────
LAST_NAMES = [
    "김", "이", "박", "최", "정", "강", "조", "윤", "장", "임",
    "한", "오", "서", "신", "권", "황", "안", "송", "류", "전",
    "홍", "고", "문", "양", "손", "배", "백", "허", "유", "남",
    "심", "노", "하", "곽", "성", "차", "주", "우", "구", "민",
]

FIRST_NAME_PARTS = [
    "민", "서", "지", "예", "하", "수", "현", "윤", "은", "채",
    "준", "도", "유", "아", "린", "우", "진", "연", "혁", "승",
    "태", "영", "호", "빈", "성", "재", "석", "원", "경", "다",
    "소", "정", "희", "나", "율", "주", "건", "한", "미", "담",
]


def generate_korean_name() -> str:
    """랜덤 한국인 이름(성 1글자 + 이름 2글자) 생성"""
    last = np.random.choice(LAST_NAMES)
    first = "".join(np.random.choice(FIRST_NAME_PARTS, size=2, replace=False))
    return last + first


# ──────────────────────────────────────────────
# 등급 산출 함수
# ──────────────────────────────────────────────
def calc_grade(avg: float) -> str:
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "E"


# ──────────────────────────────────────────────
# Mock 데이터 생성
# ──────────────────────────────────────────────
def generate_mock_data(n: int = 100, seed: int | None = None) -> pd.DataFrame:
    if seed is not None:
        np.random.seed(seed)

    names: list[str] = []
    seen: set[str] = set()
    while len(names) < n:
        name = generate_korean_name()
        if name not in seen:
            seen.add(name)
            names.append(name)

    subjects = {
        "국어": np.random.randint(30, 101, size=n),
        "영어": np.random.randint(30, 101, size=n),
        "수학": np.random.randint(30, 101, size=n),
        "과학": np.random.randint(30, 101, size=n),
    }

    df = pd.DataFrame({"이름": names, **subjects})
    df["총점"] = df[["국어", "영어", "수학", "과학"]].sum(axis=1)
    df["평균"] = df[["국어", "영어", "수학", "과학"]].mean(axis=1).round(1)
    df["등급"] = df["평균"].apply(calc_grade)
    return df


# ──────────────────────────────────────────────
# CSV 로드 / 저장
# ──────────────────────────────────────────────
def load_data() -> pd.DataFrame:
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return generate_and_save()


def generate_and_save(seed: int | None = None) -> pd.DataFrame:
    df = generate_mock_data(seed=seed)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
    return df


# ──────────────────────────────────────────────
# 커스텀 CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    /* 메트릭 카드 */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border: 1px solid #667eea44;
        border-radius: 12px;
        padding: 16px;
    }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 사이드바 메뉴
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 성적처리 시스템")
    st.markdown("---")
    menu = st.radio(
        "메뉴 선택",
        ["🏠 HOME", "📋 성적 / 데이터 분석", "📈 성적 시각화"],
        index=0,
        label_visibility="collapsed",
    )
    st.markdown("---")

    # 데이터 새로 생성
    st.markdown("#### ⚙️ 데이터 관리")
    seed_input = st.number_input("랜덤 시드 (빈칸=랜덤)", min_value=0, max_value=9999, value=42, step=1)
    if st.button("🔄 데이터 새로 생성", use_container_width=True):
        df_new = generate_and_save(seed=seed_input)
        st.session_state["df"] = df_new
        st.success("100명 데이터가 새로 생성되었습니다!")
        st.rerun()

    # CSV 다운로드
    df_current = load_data()
    csv_bytes = df_current.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="⬇️ score.csv 다운로드",
        data=csv_bytes,
        file_name="score.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ──────────────────────────────────────────────
# 데이터 로드
# ──────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state["df"] = load_data()
df = st.session_state["df"]

# ══════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════
if menu == "🏠 HOME":
    st.title("🏠 성적처리 시스템 대시보드")
    st.markdown("> 100명의 학생 성적 데이터를 생성·분석·시각화하는 웹 애플리케이션입니다.")
    st.markdown("")

    # 요약 메트릭
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("👨‍🎓 총 학생 수", f"{len(df)}명")
    col2.metric("📚 평균 점수", f"{df['평균'].mean():.1f}점")
    col3.metric("🏆 최고 평균", f"{df['평균'].max():.1f}점")
    col4.metric("📉 최저 평균", f"{df['평균'].min():.1f}점")
    col5.metric("🅰️ A등급 비율", f"{(df['등급'] == 'A').mean() * 100:.1f}%")

    st.markdown("---")

    # 등급 분포 요약
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("#### 📊 등급 분포")
        grade_counts = df["등급"].value_counts().reindex(["A", "B", "C", "D", "E"], fill_value=0)
        fig_pie = px.pie(
            values=grade_counts.values,
            names=grade_counts.index,
            color=grade_counts.index,
            color_discrete_map={"A": "#2ecc71", "B": "#3498db", "C": "#f39c12", "D": "#e67e22", "E": "#e74c3c"},
            hole=0.4,
        )
        fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=320)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.markdown("#### 🏅 상위 10명")
        top10 = df.nlargest(10, "평균")[["이름", "국어", "영어", "수학", "과학", "평균", "등급"]].reset_index(drop=True)
        top10.index = top10.index + 1
        st.dataframe(top10, use_container_width=True, height=360)

    # 전체 데이터 미리보기
    st.markdown("#### 📄 전체 데이터 미리보기")
    st.dataframe(df, use_container_width=True, height=300)


# ══════════════════════════════════════════════
# PAGE: 성적 / 데이터 분석
# ══════════════════════════════════════════════
elif menu == "📋 성적 / 데이터 분석":
    st.title("📋 성적 / 데이터 분석")

    tab1, tab2, tab3 = st.tabs(["📊 기술통계", "🔍 학생 검색", "📑 등급별 분석"])

    # ── 기술통계 ──
    with tab1:
        st.markdown("#### 과목별 기술통계량")
        subjects = ["국어", "영어", "수학", "과학", "총점", "평균"]
        desc = df[subjects].describe().T
        desc.columns = ["개수", "평균", "표준편차", "최솟값", "25%", "50%", "75%", "최댓값"]
        st.dataframe(desc.style.format("{:.1f}"), use_container_width=True)

        st.markdown("---")
        st.markdown("#### 과목별 평균 비교")
        subj_means = df[["국어", "영어", "수학", "과학"]].mean().reset_index()
        subj_means.columns = ["과목", "평균"]
        fig_bar = px.bar(
            subj_means, x="과목", y="평균", color="과목",
            color_discrete_sequence=["#3498db", "#e74c3c", "#2ecc71", "#f39c12"],
            text_auto=".1f",
        )
        fig_bar.update_layout(showlegend=False, margin=dict(t=30, b=30), height=350)
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── 학생 검색 ──
    with tab2:
        st.markdown("#### 학생 이름으로 검색")
        search_name = st.text_input("학생 이름 입력", placeholder="예: 김민서")
        if search_name:
            results = df[df["이름"].str.contains(search_name)]
            if len(results) == 0:
                st.warning("검색 결과가 없습니다.")
            else:
                st.success(f"{len(results)}명의 학생을 찾았습니다.")
                st.dataframe(results, use_container_width=True)

                if len(results) == 1:
                    student = results.iloc[0]
                    st.markdown(f"##### 🎯 {student['이름']} 학생 상세 성적")
                    cols = st.columns(4)
                    for i, subj in enumerate(["국어", "영어", "수학", "과학"]):
                        cols[i].metric(subj, f"{int(student[subj])}점")

                    # 레이더 차트
                    fig_radar = go.Figure()
                    categories = ["국어", "영어", "수학", "과학"]
                    values = [student[s] for s in categories] + [student["국어"]]
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories + ["국어"],
                        fill="toself",
                        fillcolor="rgba(102, 126, 234, 0.25)",
                        line=dict(color="#667eea", width=2),
                        name=student["이름"],
                    ))
                    fig_radar.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=False, height=350, margin=dict(t=40, b=40),
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)

    # ── 등급별 분석 ──
    with tab3:
        st.markdown("#### 등급별 학생 수 및 통계")
        grade_selected = st.selectbox("등급 선택", ["전체", "A", "B", "C", "D", "E"])
        if grade_selected == "전체":
            filtered = df
        else:
            filtered = df[df["등급"] == grade_selected]

        st.metric("학생 수", f"{len(filtered)}명")
        st.dataframe(filtered.sort_values("평균", ascending=False).reset_index(drop=True), use_container_width=True, height=400)


# ══════════════════════════════════════════════
# PAGE: 성적 시각화
# ══════════════════════════════════════════════
elif menu == "📈 성적 시각화":
    st.title("📈 성적 시각화")

    tab1, tab2, tab3 = st.tabs(["📊 점수 분포", "📈 과목 상관관계", "🏅 등급 분석"])

    # ── 점수 분포 ──
    with tab1:
        st.markdown("#### 과목별 점수 분포 (히스토그램)")
        subject_choice = st.selectbox("과목 선택", ["국어", "영어", "수학", "과학", "평균"])
        fig_hist = px.histogram(
            df, x=subject_choice, nbins=20,
            color_discrete_sequence=["#667eea"],
            marginal="box",
        )
        fig_hist.update_layout(
            xaxis_title=f"{subject_choice} 점수",
            yaxis_title="학생 수",
            height=420, margin=dict(t=30, b=30),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 전 과목 박스플롯")
        melted = df.melt(
            id_vars=["이름"], value_vars=["국어", "영어", "수학", "과학"],
            var_name="과목", value_name="점수",
        )
        fig_box = px.box(
            melted, x="과목", y="점수", color="과목",
            color_discrete_sequence=["#3498db", "#e74c3c", "#2ecc71", "#f39c12"],
        )
        fig_box.update_layout(showlegend=False, height=400, margin=dict(t=30, b=30))
        st.plotly_chart(fig_box, use_container_width=True)

    # ── 과목 상관관계 ──
    with tab2:
        st.markdown("#### 과목 간 상관관계 히트맵")
        corr = df[["국어", "영어", "수학", "과학"]].corr().round(3)
        fig_heat = px.imshow(
            corr, text_auto=True,
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            labels=dict(color="상관계수"),
        )
        fig_heat.update_layout(height=420, margin=dict(t=30, b=30))
        st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 과목 간 산점도")
        col1, col2 = st.columns(2)
        x_subj = col1.selectbox("X축 과목", ["국어", "영어", "수학", "과학"], index=0)
        y_subj = col2.selectbox("Y축 과목", ["국어", "영어", "수학", "과학"], index=2)
        fig_scatter = px.scatter(
            df, x=x_subj, y=y_subj, color="등급",
            color_discrete_map={"A": "#2ecc71", "B": "#3498db", "C": "#f39c12", "D": "#e67e22", "E": "#e74c3c"},
            hover_data=["이름", "평균"],
            opacity=0.7,
        )
        fig_scatter.update_layout(height=420, margin=dict(t=30, b=30))
        st.plotly_chart(fig_scatter, use_container_width=True)

    # ── 등급 분석 ──
    with tab3:
        st.markdown("#### 등급별 학생 수")
        grade_counts = df["등급"].value_counts().reindex(["A", "B", "C", "D", "E"], fill_value=0).reset_index()
        grade_counts.columns = ["등급", "학생 수"]
        fig_grade = px.bar(
            grade_counts, x="등급", y="학생 수", color="등급",
            color_discrete_map={"A": "#2ecc71", "B": "#3498db", "C": "#f39c12", "D": "#e67e22", "E": "#e74c3c"},
            text_auto=True,
        )
        fig_grade.update_layout(showlegend=False, height=380, margin=dict(t=30, b=30))
        st.plotly_chart(fig_grade, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 등급별 과목 평균")
        grade_subj = df.groupby("등급")[["국어", "영어", "수학", "과학"]].mean().round(1)
        grade_subj = grade_subj.reindex(["A", "B", "C", "D", "E"])
        melted_gs = grade_subj.reset_index().melt(id_vars="등급", var_name="과목", value_name="평균")
        fig_gs = px.bar(
            melted_gs, x="등급", y="평균", color="과목", barmode="group",
            color_discrete_sequence=["#3498db", "#e74c3c", "#2ecc71", "#f39c12"],
            text_auto=".1f",
        )
        fig_gs.update_layout(height=420, margin=dict(t=30, b=30))
        fig_gs.update_traces(textposition="outside")
        st.plotly_chart(fig_gs, use_container_width=True)
