import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MedProfit Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS Styling ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main background */
.stApp {
    background: #0a0e1a;
    color: #e8eaf0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #111827 100%);
    border-right: 1px solid #1e2a3a;
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #60a5fa;
}

/* Cards */
.metric-card {
    background: linear-gradient(135deg, #111827 0%, #1a2235 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 24px;
    margin: 8px 0;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #3b82f6, #1d4ed8);
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #60a5fa;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
    margin-bottom: 4px;
}

.metric-label {
    font-size: 0.8rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

.metric-delta-pos { color: #34d399; font-size: 0.85rem; font-weight: 600; }
.metric-delta-neg { color: #f87171; font-size: 0.85rem; font-weight: 600; }

/* Section headers */
.section-header {
    background: linear-gradient(135deg, #0f1f35 0%, #162032 100%);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #3b82f6;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 24px 0 16px 0;
}
.section-header h2 {
    color: #93c5fd;
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0;
}
.section-header p {
    color: #64748b;
    font-size: 0.85rem;
    margin: 6px 0 0 0;
}

/* Report cards */
.report-card {
    background: #111827;
    border: 1px solid #1e2a3a;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
}
.report-card h4 { color: #93c5fd; margin-bottom: 8px; font-size: 1rem; }
.report-card p { color: #94a3b8; font-size: 0.88rem; line-height: 1.6; }

/* Alert boxes */
.alert-danger {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-left: 4px solid #ef4444;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 8px 0;
    color: #fca5a5;
}
.alert-warning {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 8px 0;
    color: #fcd34d;
}
.alert-success {
    background: rgba(52, 211, 153, 0.1);
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-left: 4px solid #34d399;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 8px 0;
    color: #6ee7b7;
}
.alert-info {
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-left: 4px solid #3b82f6;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 8px 0;
    color: #93c5fd;
}

/* Lock overlay */
.lock-overlay {
    background: linear-gradient(135deg, #0d1117 0%, #1a1f2e 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 48px;
    text-align: center;
    margin: 20px 0;
}
.lock-icon { font-size: 3rem; margin-bottom: 16px; }
.lock-title { font-size: 1.5rem; font-weight: 700; color: #60a5fa; margin-bottom: 8px; }
.lock-desc { color: #64748b; font-size: 0.9rem; margin-bottom: 24px; line-height: 1.6; }
.badge-premium {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-free {
    background: linear-gradient(135deg, #065f46, #047857);
    color: #6ee7b7;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Table styling */
.dataframe {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117;
    border-bottom: 1px solid #1e2a3a;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b;
    background: transparent;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
}
.stTabs [aria-selected="true"] {
    color: #60a5fa !important;
    border-bottom: 2px solid #3b82f6 !important;
    background: transparent !important;
}

/* Upload area */
.stFileUploader {
    background: #111827;
    border: 2px dashed #1e3a5f;
    border-radius: 12px;
}

/* Divider */
hr { border-color: #1e2a3a; }

/* Hero header */
.hero-header {
    background: linear-gradient(135deg, #0f172a 0%, #162032 50%, #0f172a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 32px 40px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-header::after {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #93c5fd, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.hero-sub {
    color: #64748b;
    font-size: 1rem;
    margin-top: 8px;
    font-weight: 400;
}
.hero-badges { margin-top: 16px; display: flex; gap: 8px; flex-wrap: wrap; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ──────────────────────────────────────────────────────────────
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False


# ─── Helper Functions ──────────────────────────────────────────────────────────
def format_currency(val, unit="원"):
    if abs(val) >= 1e8:
        return f"{val/1e8:,.1f}억{unit}"
    elif abs(val) >= 1e4:
        return f"{val/1e4:,.0f}만{unit}"
    else:
        return f"{val:,.0f}{unit}"

def format_pct(val):
    return f"{val:.1f}%"

def color_profit(val):
    if val > 0:
        return f'<span style="color:#34d399;font-weight:700">▲ {format_currency(val)}</span>'
    else:
        return f'<span style="color:#f87171;font-weight:700">▼ {format_currency(abs(val))}</span>'

def premium_lock(feature_name, description):
    st.markdown(f"""
    <div class="lock-overlay">
        <div class="lock-icon">🔒</div>
        <div class="lock-title">{feature_name}</div>
        <div class="lock-desc">{description}</div>
        <span class="badge-premium">💎 PREMIUM 전용</span>
        <br><br>
        <p style="color:#475569;font-size:0.8rem">좌측 사이드바에서 프리미엄 모드를 활성화하세요.</p>
    </div>
    """, unsafe_allow_html=True)


# ─── Sample Data Generator ──────────────────────────────────────────────────────
def generate_sample_data():
    """엑셀 업로드 없이 시연용 샘플 데이터 생성"""
    depts = ['내과', '외과', '정형외과', '피부과', '산부인과', '소아과', '안과', '이비인후과']
    months = ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월']
    
    # 월별 진료과 매출/비용 데이터
    records = []
    np.random.seed(42)
    base_revenue = {'내과':8500,'외과':12000,'정형외과':15000,'피부과':9800,
                    '산부인과':7200,'소아과':4500,'안과':11000,'이비인후과':5500}
    base_cost = {'내과':6200,'외과':9500,'정형외과':11000,'피부과':6500,
                 '산부인과':5800,'소아과':3800,'안과':7500,'이비인후과':4200}
    
    for m_idx, month in enumerate(months):
        seasonality = 1 + 0.15*np.sin((m_idx/12)*2*np.pi - 1)
        for dept in depts:
            rev = base_revenue[dept] * seasonality * (1 + np.random.uniform(-0.08, 0.12))
            cost = base_cost[dept] * seasonality * (1 + np.random.uniform(-0.05, 0.08))
            records.append({
                '월': month, '월번호': m_idx+1, '진료과': dept,
                '매출(만원)': round(rev, 0),
                '인건비(만원)': round(cost*0.55, 0),
                '재료비(만원)': round(cost*0.25, 0),
                '운영비(만원)': round(cost*0.20, 0),
                '환자수': int(rev/15 + np.random.randint(-30,30)),
                '의사수': np.random.choice([1,2,3], p=[0.3,0.5,0.2])
            })
    
    df_monthly = pd.DataFrame(records)
    df_monthly['총비용(만원)'] = df_monthly['인건비(만원)'] + df_monthly['재료비(만원)'] + df_monthly['운영비(만원)']
    df_monthly['순이익(만원)'] = df_monthly['매출(만원)'] - df_monthly['총비용(만원)']
    df_monthly['이익률(%)'] = (df_monthly['순이익(만원)'] / df_monthly['매출(만원)'] * 100).round(1)

    # 행위별 데이터
    acts = ['진찰료','처치비','검사비','약제비','수술비','영상비','재활치료비','상담비']
    act_records = []
    for dept in depts:
        for act in acts:
            if np.random.random() > 0.35:
                rev = np.random.uniform(200, 3000)
                margin = np.random.uniform(0.15, 0.65)
                act_records.append({
                    '진료과': dept, '행위명': act,
                    '건수': int(np.random.uniform(50, 500)),
                    '매출(만원)': round(rev, 0),
                    '직접비용(만원)': round(rev*(1-margin), 0),
                    '마진율(%)': round(margin*100, 1)
                })
    df_act = pd.DataFrame(act_records)
    df_act['공헌이익(만원)'] = df_act['매출(만원)'] - df_act['직접비용(만원)']

    return df_monthly, df_act


# ─── Excel Parser ───────────────────────────────────────────────────────────────
def parse_excel(uploaded_file):
    """업로드된 엑셀 파일 파싱 - 여러 시트 지원"""
    try:
        xl = pd.ExcelFile(uploaded_file)
        sheets = xl.sheet_names
        dfs = {}
        for sheet in sheets:
            df = pd.read_excel(uploaded_file, sheet_name=sheet)
            df.columns = [str(c).strip() for c in df.columns]
            dfs[sheet] = df
        return dfs, sheets, None
    except Exception as e:
        return None, None, str(e)


# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 12px;">
        <div style="font-size:2.5rem">🏥</div>
        <div style="font-size:1.1rem;font-weight:800;color:#60a5fa;letter-spacing:-0.02em">MedProfit</div>
        <div style="font-size:0.7rem;color:#475569;letter-spacing:0.15em;text-transform:uppercase">Analytics Platform</div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    # Premium toggle
    st.markdown("### ⚙️ 서비스 설정")
    
    premium_key = st.text_input("🔑 라이선스 키", type="password", placeholder="프리미엄 키 입력...")
    PREMIUM_KEY = "MEDPROFIT2024"
    
    if premium_key == PREMIUM_KEY:
        st.session_state.is_premium = True
        st.markdown('<div class="alert-success">✅ 프리미엄 활성화됨</div>', unsafe_allow_html=True)
    elif premium_key and premium_key != PREMIUM_KEY:
        st.markdown('<div class="alert-danger">❌ 올바르지 않은 키</div>', unsafe_allow_html=True)
    
    if not st.session_state.is_premium:
        st.markdown('<div class="alert-info">🆓 현재 무료 플랜 이용 중<br><small>데모 키: MEDPROFIT2024</small></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📂 데이터 업로드")
    
    use_sample = st.checkbox("📊 샘플 데이터 사용", value=True, help="실제 데이터 없이 샘플 데이터로 분석")
    
    uploaded_file = None
    if not use_sample:
        uploaded_file = st.file_uploader(
            "엑셀 파일 업로드",
            type=['xlsx','xls'],
            help="진료과별·월별 매출/비용 데이터가 포함된 엑셀 파일을 업로드하세요"
        )
    
    st.markdown("---")
    st.markdown("### 🎯 분석 옵션")
    
    analysis_year = st.selectbox("분석 연도", [2024, 2023, 2022], index=0)
    benchmark_mode = st.checkbox("벤치마크 비교", value=False, disabled=not st.session_state.is_premium)
    if not st.session_state.is_premium:
        st.caption("🔒 벤치마크는 프리미엄 전용")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;padding:10px 0;">
        <div style="font-size:0.7rem;color:#374151;line-height:1.8">
            <div>병원 경영 컨설팅 전문</div>
            <div style="color:#4b5563">v2.0.0 | © 2024 MedProfit</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Load Data ──────────────────────────────────────────────────────────────────
if use_sample or uploaded_file is None:
    df_monthly, df_act = generate_sample_data()
    data_source = "샘플 데이터"
    sheet_names = ['월별_진료과_데이터', '행위별_데이터']
else:
    dfs, sheet_names, err = parse_excel(uploaded_file)
    if err:
        st.error(f"파일 파싱 오류: {err}")
        st.stop()
    # 첫 번째 시트를 월별 데이터로 사용
    df_monthly = list(dfs.values())[0]
    df_act = list(dfs.values())[1] if len(dfs) > 1 else None
    data_source = uploaded_file.name
    
    # 컬럼 자동 매핑
    col_map = {}
    for col in df_monthly.columns:
        lower = col.lower()
        if '매출' in lower or 'revenue' in lower: col_map['매출(만원)'] = col
        elif '비용' in lower or 'cost' in lower: col_map['총비용(만원)'] = col
        elif '이익' in lower or 'profit' in lower: col_map['순이익(만원)'] = col
        elif '진료과' in lower or 'dept' in lower: col_map['진료과'] = col
        elif '월' in lower or 'month' in lower: col_map['월'] = col
    
    # 기본 계산 추가
    if '총비용(만원)' not in df_monthly.columns and '순이익(만원)' not in df_monthly.columns:
        if '매출(만원)' in df_monthly.columns:
            df_monthly['순이익(만원)'] = df_monthly.get('매출(만원)', 0) - df_monthly.get('총비용(만원)', 0)


# ─── MAIN CONTENT ───────────────────────────────────────────────────────────────

# Hero Header
st.markdown(f"""
<div class="hero-header">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
        <div>
            <div class="hero-title">🏥 병원 수익성 분석 리포트</div>
            <div class="hero-sub">데이터 기반 전문 경영 진단 · 전략 시뮬레이션 · 미래 방향 제시</div>
            <div class="hero-badges">
                <span class="badge-free">🆓 FREE</span>
                {'<span class="badge-premium">💎 PREMIUM 활성화</span>' if st.session_state.is_premium else '<span style="background:#1e2a3a;color:#64748b;padding:4px 12px;border-radius:20px;font-size:0.75rem;font-weight:700">🔒 PREMIUM 잠금</span>'}
                <span style="background:#162032;color:#64748b;padding:4px 12px;border-radius:20px;font-size:0.75rem">📅 {analysis_year}년 분석</span>
                <span style="background:#162032;color:#64748b;padding:4px 12px;border-radius:20px;font-size:0.75rem">📊 {data_source}</span>
            </div>
        </div>
        <div style="text-align:right;color:#374151;font-size:0.75rem;font-family:'JetBrains Mono',monospace">
            <div>생성: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── TABS ────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 핵심 요약",
    "🏢 진료과별 분석",
    "⚕️ 행위별 손익",
    "📈 트렌드 분석",
    "🔮 시뮬레이션",
    "📋 전략 보고서",
    "⚠️ 리스크 진단",
    "📥 데이터 입력 가이드"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: 핵심 요약 (FREE)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<span class="badge-free">🆓 무료 제공</span>', unsafe_allow_html=True)
    st.markdown("")
    
    # KPI Cards
    total_rev = df_monthly['매출(만원)'].sum()
    total_cost = df_monthly['총비용(만원)'].sum()
    total_profit = df_monthly['순이익(만원)'].sum()
    avg_margin = (total_profit / total_rev * 100) if total_rev > 0 else 0
    total_patients = df_monthly['환자수'].sum() if '환자수' in df_monthly.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">연간 총 매출</div>
            <div class="metric-value">{total_rev/1e4:.1f}억</div>
            <div style="color:#64748b;font-size:0.8rem;margin-top:4px">{format_currency(total_rev*10000)} 원</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:#f87171;">
            <div class="metric-label">연간 총 비용</div>
            <div class="metric-value" style="color:#f87171;">{total_cost/1e4:.1f}억</div>
            <div style="color:#64748b;font-size:0.8rem;margin-top:4px">비용률 {total_cost/total_rev*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        profit_color = "#34d399" if total_profit > 0 else "#f87171"
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:{profit_color};">
            <div class="metric-label">연간 순이익</div>
            <div class="metric-value" style="color:{profit_color};">{total_profit/1e4:.1f}억</div>
            <div style="color:#64748b;font-size:0.8rem;margin-top:4px">이익률 {avg_margin:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_rev_per_patient = (total_rev / total_patients * 10000) if total_patients > 0 else 0
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:#a78bfa;">
            <div class="metric-label">총 환자수</div>
            <div class="metric-value" style="color:#a78bfa;">{total_patients:,}</div>
            <div style="color:#64748b;font-size:0.8rem;margin-top:4px">1인당 {avg_rev_per_patient/10000:.0f}만원</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_a, col_b = st.columns([3, 2])
    
    with col_a:
        st.markdown("""
        <div class="section-header">
            <h2>📊 진료과별 연간 매출/이익 현황</h2>
            <p>진료과별 수익성 비교 개요</p>
        </div>
        """, unsafe_allow_html=True)
        
        dept_summary = df_monthly.groupby('진료과').agg(
            매출=('매출(만원)', 'sum'),
            비용=('총비용(만원)', 'sum'),
            이익=('순이익(만원)', 'sum'),
            환자수=('환자수', 'sum')
        ).reset_index()
        dept_summary['이익률'] = (dept_summary['이익'] / dept_summary['매출'] * 100).round(1)
        dept_summary = dept_summary.sort_values('매출', ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='매출', x=dept_summary['진료과'], y=dept_summary['매출'],
            marker_color='#3b82f6', opacity=0.85,
            text=[f'{v:,.0f}만' for v in dept_summary['매출']],
            textposition='outside', textfont=dict(size=10, color='#93c5fd')
        ))
        fig.add_trace(go.Bar(
            name='순이익', x=dept_summary['진료과'], y=dept_summary['이익'],
            marker_color='#34d399', opacity=0.85
        ))
        fig.update_layout(
            barmode='group', paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8',
            legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#94a3b8'),
            xaxis=dict(gridcolor='#1e2a3a'), yaxis=dict(gridcolor='#1e2a3a'),
            margin=dict(l=0,r=0,t=20,b=0), height=320
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.markdown("""
        <div class="section-header">
            <h2>🥧 매출 구성비</h2>
            <p>진료과별 매출 비중</p>
        </div>
        """, unsafe_allow_html=True)
        
        colors = ['#3b82f6','#60a5fa','#93c5fd','#34d399','#6ee7b7','#a78bfa','#c4b5fd','#f87171']
        fig2 = go.Figure(go.Pie(
            labels=dept_summary['진료과'],
            values=dept_summary['매출'],
            hole=0.55,
            marker_colors=colors,
            textinfo='label+percent',
            textfont=dict(size=11, color='white')
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            showlegend=False,
            margin=dict(l=0,r=0,t=20,b=0),
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Quick Diagnosis
    st.markdown("""
    <div class="section-header">
        <h2>🩺 빠른 경영 진단</h2>
        <p>핵심 지표 기반 자동 진단 결과 (상세 진단은 프리미엄에서 제공)</p>
    </div>
    """, unsafe_allow_html=True)
    
    best_dept = dept_summary.loc[dept_summary['이익률'].idxmax(), '진료과']
    worst_dept = dept_summary.loc[dept_summary['이익률'].idxmin(), '진료과']
    best_margin = dept_summary['이익률'].max()
    worst_margin = dept_summary['이익률'].min()
    
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        if avg_margin >= 20:
            st.markdown(f'<div class="alert-success">✅ <strong>이익률 양호</strong><br>전체 이익률 {avg_margin:.1f}%로 병원 평균(15~20%) 대비 우수합니다.</div>', unsafe_allow_html=True)
        elif avg_margin >= 10:
            st.markdown(f'<div class="alert-warning">⚠️ <strong>이익률 주의</strong><br>전체 이익률 {avg_margin:.1f}%로 개선이 필요합니다.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-danger">🚨 <strong>이익률 위험</strong><br>전체 이익률 {avg_margin:.1f}%로 즉각적인 개선이 필요합니다.</div>', unsafe_allow_html=True)
    
    with col_d2:
        st.markdown(f'<div class="alert-info">🏆 <strong>최고 수익 진료과: {best_dept}</strong><br>이익률 {best_margin:.1f}% — 핵심 성장 동력입니다.</div>', unsafe_allow_html=True)
    
    with col_d3:
        st.markdown(f'<div class="alert-warning">⚠️ <strong>개선 필요 진료과: {worst_dept}</strong><br>이익률 {worst_margin:.1f}% — 비용 구조 재검토 필요.</div>', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown('<div class="alert-info">💎 <strong>상세 분석은 프리미엄에서</strong> — 진료과별 세부 손익 분해, 트렌드 예측, AI 전략 보고서, 리스크 진단 등 전문 컨설팅 수준의 분석을 제공합니다.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: 진료과별 분석 (FREE 기본 / PREMIUM 심화)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<span class="badge-free">🆓 기본 분석 무료</span> <span class="badge-premium">💎 심화 분석 프리미엄</span>', unsafe_allow_html=True)
    st.markdown("")
    
    dept_summary2 = df_monthly.groupby('진료과').agg(
        매출=('매출(만원)', 'sum'),
        인건비=('인건비(만원)', 'sum'),
        재료비=('재료비(만원)', 'sum'),
        운영비=('운영비(만원)', 'sum'),
        총비용=('총비용(만원)', 'sum'),
        순이익=('순이익(만원)', 'sum'),
        환자수=('환자수', 'sum')
    ).reset_index()
    dept_summary2['이익률(%)'] = (dept_summary2['순이익'] / dept_summary2['매출'] * 100).round(1)
    dept_summary2['인건비율(%)'] = (dept_summary2['인건비'] / dept_summary2['매출'] * 100).round(1)
    dept_summary2['재료비율(%)'] = (dept_summary2['재료비'] / dept_summary2['매출'] * 100).round(1)
    dept_summary2['1인당매출(만원)'] = (dept_summary2['매출'] / dept_summary2['환자수']).round(0)
    
    # 선택 필터
    selected_depts = st.multiselect(
        "분석할 진료과 선택", 
        options=dept_summary2['진료과'].tolist(),
        default=dept_summary2['진료과'].tolist()
    )
    df_filtered = dept_summary2[dept_summary2['진료과'].isin(selected_depts)]
    
    # 기본 테이블 (FREE)
    st.markdown("""
    <div class="section-header">
        <h2>📋 진료과별 손익 현황표</h2>
        <p>연간 집계 기준</p>
    </div>
    """, unsafe_allow_html=True)
    
    display_df = df_filtered[['진료과','매출','총비용','순이익','이익률(%)','환자수','1인당매출(만원)']].copy()
    display_df.columns = ['진료과','매출(만원)','총비용(만원)','순이익(만원)','이익률(%)','환자수','1인당매출(만원)']
    display_df = display_df.sort_values('매출(만원)', ascending=False)
    
    st.dataframe(
        display_df.style.format({
            '매출(만원)': '{:,.0f}',
            '총비용(만원)': '{:,.0f}',
            '순이익(만원)': '{:,.0f}',
            '이익률(%)': '{:.1f}%',
            '환자수': '{:,.0f}',
            '1인당매출(만원)': '{:,.0f}'
        }).background_gradient(subset=['이익률(%)'], cmap='RdYlGn')
         .map(lambda v: 'color: #34d399' if isinstance(v, (int,float)) and v > 0 else 'color: #f87171',
                   subset=['순이익(만원)']),
        use_container_width=True, height=300
    )
    
    # 비용 구조 (FREE)
    st.markdown("""
    <div class="section-header">
        <h2>💰 비용 구조 분석</h2>
        <p>인건비·재료비·운영비 비중 비교</p>
    </div>
    """, unsafe_allow_html=True)
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name='인건비', x=df_filtered['진료과'], y=df_filtered['인건비'], marker_color='#3b82f6'))
    fig3.add_trace(go.Bar(name='재료비', x=df_filtered['진료과'], y=df_filtered['재료비'], marker_color='#f59e0b'))
    fig3.add_trace(go.Bar(name='운영비', x=df_filtered['진료과'], y=df_filtered['운영비'], marker_color='#8b5cf6'))
    fig3.update_layout(
        barmode='stack', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8',
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(gridcolor='#1e2a3a'), yaxis=dict(gridcolor='#1e2a3a'),
        margin=dict(l=0,r=0,t=20,b=0), height=300
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # PREMIUM: 심화 분석
    if st.session_state.is_premium:
        st.markdown('<span class="badge-premium">💎 PREMIUM 심화 분석</span>', unsafe_allow_html=True)
        st.markdown("")
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("""
            <div class="section-header">
                <h2>🎯 수익성 포트폴리오 매트릭스</h2>
                <p>매출규모 vs 이익률 포지셔닝 (버블: 환자수)</p>
            </div>
            """, unsafe_allow_html=True)
            
            fig_scatter = px.scatter(
                df_filtered, x='이익률(%)', y='매출',
                size='환자수', color='이익률(%)',
                text='진료과',
                color_continuous_scale='RdYlGn',
                size_max=60
            )
            fig_scatter.update_traces(textposition='top center', textfont=dict(color='white', size=11))
            fig_scatter.add_vline(x=df_filtered['이익률(%)'].mean(), line_dash='dash', line_color='#64748b')
            fig_scatter.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', margin=dict(l=0,r=0,t=20,b=0),
                height=350, showlegend=False,
                xaxis=dict(gridcolor='#1e2a3a', title='이익률(%)'),
                yaxis=dict(gridcolor='#1e2a3a', title='연간 매출(만원)')
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col_p2:
            st.markdown("""
            <div class="section-header">
                <h2>📊 진료과별 손익분기점 분석</h2>
                <p>BEP 달성률 및 안전 마진</p>
            </div>
            """, unsafe_allow_html=True)
            
            df_bep = df_filtered.copy()
            # 손익분기점 = 고정비 / (1 - 변동비율)
            # 인건비 70% 고정, 재료비 100% 변동, 운영비 50% 고정으로 가정
            df_bep['고정비'] = df_bep['인건비']*0.7 + df_bep['운영비']*0.5
            df_bep['변동비율'] = (df_bep['재료비'] + df_bep['인건비']*0.3 + df_bep['운영비']*0.5) / df_bep['매출']
            df_bep['BEP매출'] = df_bep['고정비'] / (1 - df_bep['변동비율'])
            df_bep['BEP달성률(%)'] = (df_bep['매출'] / df_bep['BEP매출'] * 100).round(1)
            df_bep['안전마진(%)'] = ((df_bep['매출'] - df_bep['BEP매출']) / df_bep['매출'] * 100).round(1)
            
            colors_bep = ['#34d399' if v >= 100 else '#f87171' for v in df_bep['BEP달성률(%)']]
            fig_bep = go.Figure(go.Bar(
                x=df_bep['진료과'], y=df_bep['BEP달성률(%)'],
                marker_color=colors_bep,
                text=[f'{v:.0f}%' for v in df_bep['BEP달성률(%)']],
                textposition='outside',
                textfont=dict(color='white', size=11)
            ))
            fig_bep.add_hline(y=100, line_dash='dash', line_color='#f59e0b',
                              annotation_text='손익분기점', annotation_font_color='#f59e0b')
            fig_bep.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', margin=dict(l=0,r=0,t=20,b=0), height=350,
                xaxis=dict(gridcolor='#1e2a3a'), yaxis=dict(gridcolor='#1e2a3a', title='BEP 달성률(%)')
            )
            st.plotly_chart(fig_bep, use_container_width=True)
        
        # 인건비 생산성 분석
        st.markdown("""
        <div class="section-header">
            <h2>👨‍⚕️ 의사 1인당 생산성 분석</h2>
            <p>인력 효율성 및 의사당 매출·이익 기여도</p>
        </div>
        """, unsafe_allow_html=True)
        
        if '의사수' in df_monthly.columns:
            dept_doctors = df_monthly.groupby('진료과').agg(
                의사수=('의사수', 'mean'),
                매출=('매출(만원)', 'sum'),
                이익=('순이익(만원)', 'sum')
            ).reset_index()
            dept_doctors['의사1인당매출(만원)'] = (dept_doctors['매출'] / dept_doctors['의사수']).round(0)
            dept_doctors['의사1인당이익(만원)'] = (dept_doctors['이익'] / dept_doctors['의사수']).round(0)
            
            st.dataframe(
                dept_doctors.style.format({
                    '의사수': '{:.1f}',
                    '의사1인당매출(만원)': '{:,.0f}',
                    '의사1인당이익(만원)': '{:,.0f}'
                }).background_gradient(subset=['의사1인당매출(만원)'], cmap='Blues'),
                use_container_width=True
            )
    else:
        premium_lock(
            "🎯 심화 진료과 분석",
            "수익성 포트폴리오 매트릭스, 손익분기점(BEP) 분석, 의사 1인당 생산성 분석,\n인건비 효율성 진단 등 전문 컨설팅 수준의 심화 분석을 제공합니다."
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: 행위별 손익 (PREMIUM)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<span class="badge-premium">💎 전체 프리미엄 전용</span>', unsafe_allow_html=True)
    st.markdown("")
    
    if st.session_state.is_premium:
        st.markdown("""
        <div class="section-header">
            <h2>⚕️ 행위별 수익성 분석</h2>
            <p>진료 행위 단위로 매출·비용·마진율을 정밀 분석합니다</p>
        </div>
        """, unsafe_allow_html=True)
        
        if df_act is not None:
            col_f1, col_f2 = st.columns([1,2])
            with col_f1:
                dept_sel = st.selectbox("진료과 선택", ['전체'] + df_act['진료과'].unique().tolist())
            with col_f2:
                sort_by = st.selectbox("정렬 기준", ['매출(만원)', '마진율(%)','공헌이익(만원)','건수'])
            
            df_act_show = df_act.copy()
            if dept_sel != '전체':
                df_act_show = df_act_show[df_act_show['진료과'] == dept_sel]
            df_act_show = df_act_show.sort_values(sort_by, ascending=False)
            
            # 행위별 매출 트리맵
            fig_tree = px.treemap(
                df_act_show, path=['진료과', '행위명'],
                values='매출(만원)', color='마진율(%)',
                color_continuous_scale='RdYlGn',
                title='행위별 매출 구성 (색상: 마진율)'
            )
            fig_tree.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8',
                margin=dict(l=0,r=0,t=40,b=0), height=380
            )
            st.plotly_chart(fig_tree, use_container_width=True)
            
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                # 공헌이익 순위
                top_acts = df_act_show.nlargest(10, '공헌이익(만원)')
                fig_contrib = go.Figure(go.Bar(
                    y=top_acts['행위명'] + ' (' + top_acts['진료과'] + ')',
                    x=top_acts['공헌이익(만원)'],
                    orientation='h',
                    marker_color='#34d399',
                    text=[f'{v:,.0f}만' for v in top_acts['공헌이익(만원)']],
                    textposition='outside'
                ))
                fig_contrib.update_layout(
                    title='공헌이익 TOP 10 행위',
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8', height=350,
                    margin=dict(l=0,r=0,t=40,b=0),
                    xaxis=dict(gridcolor='#1e2a3a'), yaxis=dict(gridcolor='#1e2a3a')
                )
                st.plotly_chart(fig_contrib, use_container_width=True)
            
            with col_a2:
                # 마진율 분포
                low_margin = df_act_show[df_act_show['마진율(%)'] < 20]
                mid_margin = df_act_show[(df_act_show['마진율(%)'] >= 20) & (df_act_show['마진율(%)'] < 40)]
                high_margin = df_act_show[df_act_show['마진율(%)'] >= 40]
                
                fig_margin = go.Figure(go.Pie(
                    labels=['저마진 (<20%)', '중마진 (20~40%)', '고마진 (>40%)'],
                    values=[len(low_margin), len(mid_margin), len(high_margin)],
                    marker_colors=['#ef4444','#f59e0b','#34d399'],
                    hole=0.5
                ))
                fig_margin.update_layout(
                    title='행위 마진율 분포',
                    paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8',
                    height=350, margin=dict(l=0,r=0,t=40,b=0)
                )
                st.plotly_chart(fig_margin, use_container_width=True)
            
            # 저마진 행위 경고
            if len(low_margin) > 0:
                st.markdown(f"""
                <div class="alert-warning">
                    ⚠️ <strong>저마진 행위 {len(low_margin)}건 발견</strong> — 
                    {', '.join(low_margin['행위명'].unique()[:5].tolist())} 등의 행위는 마진율이 20% 미만으로 
                    수가 협상, 원가절감, 또는 행위 축소를 검토하세요.
                </div>
                """, unsafe_allow_html=True)
            
            # 상세 테이블
            st.markdown("#### 📋 행위별 상세 손익표")
            st.dataframe(
                df_act_show.style.format({
                    '건수': '{:,.0f}',
                    '매출(만원)': '{:,.0f}',
                    '직접비용(만원)': '{:,.0f}',
                    '공헌이익(만원)': '{:,.0f}',
                    '마진율(%)': '{:.1f}%'
                }).background_gradient(subset=['마진율(%)'], cmap='RdYlGn'),
                use_container_width=True, height=350
            )
    else:
        premium_lock(
            "⚕️ 행위별 수익성 분석",
            "진료 행위 단위(진찰료, 처치비, 검사비, 수술비 등)별 매출·비용·마진율을 정밀 분석합니다.\n손익분기 행위 식별, 공헌이익 순위, 저마진 행위 경고 등 세밀한 수익 구조 진단을 제공합니다."
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: 트렌드 분석 (FREE 기본 / PREMIUM 고급)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<span class="badge-free">🆓 기본 트렌드 무료</span> <span class="badge-premium">💎 예측·계절성 분석 프리미엄</span>', unsafe_allow_html=True)
    st.markdown("")
    
    # 월별 집계
    monthly_agg = df_monthly.groupby('월번호').agg(
        매출=('매출(만원)', 'sum'),
        비용=('총비용(만원)', 'sum'),
        이익=('순이익(만원)', 'sum'),
        환자수=('환자수', 'sum')
    ).reset_index()
    monthly_agg['월'] = ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'][:len(monthly_agg)]
    monthly_agg['이익률'] = (monthly_agg['이익']/monthly_agg['매출']*100).round(1)
    
    st.markdown("""
    <div class="section-header">
        <h2>📈 월별 매출·이익 트렌드</h2>
        <p>계절적 패턴 및 성장 추세 파악</p>
    </div>
    """, unsafe_allow_html=True)
    
    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(go.Scatter(
        x=monthly_agg['월'], y=monthly_agg['매출'],
        name='매출', line=dict(color='#3b82f6', width=3),
        fill='tonexty', fillcolor='rgba(59,130,246,0.1)'
    ), secondary_y=False)
    fig_trend.add_trace(go.Scatter(
        x=monthly_agg['월'], y=monthly_agg['이익'],
        name='순이익', line=dict(color='#34d399', width=3),
    ), secondary_y=False)
    fig_trend.add_trace(go.Scatter(
        x=monthly_agg['월'], y=monthly_agg['이익률'],
        name='이익률(%)', line=dict(color='#f59e0b', width=2, dash='dot'),
        mode='lines+markers'
    ), secondary_y=True)
    
    fig_trend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8', legend=dict(bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(gridcolor='#1e2a3a'), 
        yaxis=dict(gridcolor='#1e2a3a', title='금액(만원)'),
        yaxis2=dict(title='이익률(%)', overlaying='y', side='right'),
        margin=dict(l=0,r=0,t=20,b=0), height=350
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # 진료과별 월별 히트맵 (FREE)
    st.markdown("""
    <div class="section-header">
        <h2>🗓️ 진료과별 월별 이익률 히트맵</h2>
        <p>계절 패턴 및 부서 성과 매트릭스</p>
    </div>
    """, unsafe_allow_html=True)
    
    pivot_margin = df_monthly.pivot_table(
        values='이익률(%)', index='진료과', columns='월번호', aggfunc='mean'
    )
    pivot_margin.columns = ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'][:len(pivot_margin.columns)]
    
    fig_heat = go.Figure(go.Heatmap(
        z=pivot_margin.values,
        x=pivot_margin.columns,
        y=pivot_margin.index,
        colorscale='RdYlGn',
        text=[[f'{v:.1f}%' for v in row] for row in pivot_margin.values],
        texttemplate='%{text}',
        textfont=dict(size=10, color='white'),
        colorbar=dict(title='이익률(%)', tickfont=dict(color='#94a3b8'))
    ))
    fig_heat.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8', margin=dict(l=0,r=0,t=10,b=0), height=320
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
    # PREMIUM: 예측 분석
    if st.session_state.is_premium:
        st.markdown('<span class="badge-premium">💎 PREMIUM 예측 분석</span>', unsafe_allow_html=True)
        st.markdown("")
        
        st.markdown("""
        <div class="section-header">
            <h2>🔮 차년도 매출 예측 (선형 추세 기반)</h2>
            <p>현재 트렌드를 기반으로 한 차년도 예측 시나리오</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 간단한 선형 회귀 예측
        from numpy.polynomial import polynomial as P
        
        x = monthly_agg['월번호'].values
        y = monthly_agg['매출'].values
        
        coeffs = np.polyfit(x, y, 1)
        trend_line = np.poly1d(coeffs)
        
        # 다음 12개월 예측
        future_months = np.arange(1, 25)
        future_pred = trend_line(future_months)
        
        growth_rate = (coeffs[0] * 12) / y.mean() * 100
        
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            x=list(range(1,13)), y=monthly_agg['매출'],
            name='실제 매출', line=dict(color='#3b82f6', width=3),
            mode='lines+markers'
        ))
        fig_forecast.add_trace(go.Scatter(
            x=list(range(1,25)), y=future_pred,
            name='추세선 (24개월)', line=dict(color='#f59e0b', width=2, dash='dash')
        ))
        fig_forecast.add_trace(go.Scatter(
            x=list(range(13,25)), y=future_pred[12:],
            name='예측 구간', line=dict(color='#a78bfa', width=3),
            fill='tonexty', fillcolor='rgba(167,139,250,0.1)',
            mode='lines+markers'
        ))
        fig_forecast.add_vrect(x0=12.5, x1=24, fillcolor='rgba(167,139,250,0.05)', line_width=0)
        fig_forecast.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8', legend=dict(bgcolor='rgba(0,0,0,0)'),
            xaxis=dict(gridcolor='#1e2a3a', title='월'),
            yaxis=dict(gridcolor='#1e2a3a', title='매출(만원)'),
            margin=dict(l=0,r=0,t=20,b=0), height=350
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            pred_annual = future_pred[12:].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">차년도 예측 연매출</div>
                <div class="metric-value">{pred_annual/1e4:.1f}억</div>
                <div class="metric-delta-pos">추세 기반 예측</div>
            </div>
            """, unsafe_allow_html=True)
        with col_f2:
            curr_annual = monthly_agg['매출'].sum()
            growth_amt = pred_annual - curr_annual
            color_g = '#34d399' if growth_amt > 0 else '#f87171'
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">예상 성장액</div>
                <div class="metric-value" style="color:{color_g};">{growth_amt/1e4:+.1f}억</div>
                <div style="color:{color_g};font-size:0.85rem">{growth_rate:+.1f}%/년</div>
            </div>
            """, unsafe_allow_html=True)
        with col_f3:
            pred_monthly_avg = future_pred[12:].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">예측 월평균 매출</div>
                <div class="metric-value">{pred_monthly_avg/1e4:.1f}억</div>
                <div style="color:#64748b;font-size:0.8rem">월 기준</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-warning">
            ⚠️ <strong>예측 주의사항</strong>: 본 예측은 현재 데이터의 선형 추세를 기반으로 하며, 
            실제 경영 환경 변화(의료 정책, 경쟁 환경, 인구 변화 등)는 반영되지 않습니다. 
            전략적 의사결정 시 다양한 시나리오와 전문가 판단을 병행하시기 바랍니다.
        </div>
        """, unsafe_allow_html=True)
    else:
        premium_lock(
            "🔮 매출 예측 및 시나리오 분석",
            "선형·계절성 트렌드 기반 차년도 매출 예측, 성장률 분석, 예측 신뢰구간 등\n데이터 기반 미래 방향 예측 분석을 제공합니다."
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: 시뮬레이션 (PREMIUM)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<span class="badge-premium">💎 전체 프리미엄 전용</span>', unsafe_allow_html=True)
    st.markdown("")
    
    if st.session_state.is_premium:
        st.markdown("""
        <div class="section-header">
            <h2>🔮 경영 시뮬레이션 센터</h2>
            <p>가정 조건을 조정하여 미래 수익성을 예측하세요</p>
        </div>
        """, unsafe_allow_html=True)
        
        sim_tab1, sim_tab2, sim_tab3 = st.tabs(["💰 수가·환자수 시뮬레이션", "💼 비용 구조 시뮬레이션", "🆕 신규 진료과 시뮬레이션"])
        
        with sim_tab1:
            st.markdown("#### 진료과별 수가 인상/환자수 변동 시나리오")
            
            dept_list = df_monthly['진료과'].unique().tolist()
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                sim_dept = st.selectbox("시뮬레이션 대상 진료과", dept_list)
                price_change = st.slider("수가 변동률 (%)", -30, 50, 0, 1)
            with col_s2:
                patient_change = st.slider("환자수 변동률 (%)", -50, 100, 0, 1)
                cost_change = st.slider("비용 변동률 (%)", -20, 30, 0, 1)
            
            dept_base = df_monthly[df_monthly['진료과'] == sim_dept]
            base_rev = dept_base['매출(만원)'].sum()
            base_cost = dept_base['총비용(만원)'].sum()
            base_profit = dept_base['순이익(만원)'].sum()
            base_patients = dept_base['환자수'].sum()
            
            sim_rev = base_rev * (1 + price_change/100) * (1 + patient_change/100)
            sim_cost = base_cost * (1 + cost_change/100) * (1 + patient_change/100 * 0.6)
            sim_profit = sim_rev - sim_cost
            sim_margin = sim_profit / sim_rev * 100 if sim_rev > 0 else 0
            sim_patients = int(base_patients * (1 + patient_change/100))
            
            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            metrics = [
                ('매출', base_rev, sim_rev, '만원'),
                ('비용', base_cost, sim_cost, '만원'),
                ('순이익', base_profit, sim_profit, '만원'),
                ('환자수', base_patients, sim_patients, '명')
            ]
            
            for col, (name, base, sim, unit) in zip([col_r1,col_r2,col_r3,col_r4], metrics):
                delta = sim - base
                delta_pct = (delta/base*100) if base != 0 else 0
                color = '#34d399' if delta >= 0 else '#f87171'
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">{name} 변화</div>
                        <div class="metric-value" style="font-size:1.4rem">{sim:,.0f}<span style="font-size:0.9rem">{unit}</span></div>
                        <div style="color:{color};font-size:0.85rem;font-weight:700">{delta_pct:+.1f}%</div>
                        <div style="color:#475569;font-size:0.75rem">기준: {base:,.0f}{unit}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # 시나리오 비교 차트
            fig_sim = go.Figure()
            categories = ['매출', '비용', '순이익']
            base_vals = [base_rev, base_cost, base_profit]
            sim_vals = [sim_rev, sim_cost, sim_profit]
            
            fig_sim.add_trace(go.Bar(name='현재', x=categories, y=base_vals,
                                      marker_color='#3b82f6', opacity=0.7))
            fig_sim.add_trace(go.Bar(name='시뮬레이션', x=categories, y=sim_vals,
                                      marker_color='#34d399', opacity=0.9))
            fig_sim.update_layout(
                barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', legend=dict(bgcolor='rgba(0,0,0,0)'),
                xaxis=dict(gridcolor='#1e2a3a'), yaxis=dict(gridcolor='#1e2a3a', title='금액(만원)'),
                margin=dict(l=0,r=0,t=20,b=0), height=300
            )
            st.plotly_chart(fig_sim, use_container_width=True)
            
            # 분석 코멘트
            if sim_profit > base_profit:
                improvement = sim_profit - base_profit
                st.markdown(f"""
                <div class="alert-success">
                    ✅ <strong>수익성 개선 효과</strong>: 해당 조건 적용 시 {sim_dept}의 순이익이 
                    연간 {improvement:,.0f}만원 ({(improvement/base_profit*100):+.1f}%) 증가합니다.
                    이익률은 {base_profit/base_rev*100:.1f}% → {sim_margin:.1f}%로 변화합니다.
                </div>
                """, unsafe_allow_html=True)
            else:
                decline = base_profit - sim_profit
                st.markdown(f"""
                <div class="alert-danger">
                    🚨 <strong>수익성 악화 예상</strong>: 해당 조건 적용 시 {sim_dept}의 순이익이 
                    연간 {decline:,.0f}만원 ({-(decline/base_profit*100):.1f}%) 감소합니다.
                    비용 구조 개선 또는 수가 조정을 검토하세요.
                </div>
                """, unsafe_allow_html=True)
        
        with sim_tab2:
            st.markdown("#### 비용 구조 최적화 시뮬레이션")
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                labor_opt = st.slider("인건비 절감률 (%)", 0, 20, 5, 1)
                material_opt = st.slider("재료비 절감률 (%)", 0, 15, 3, 1)
            with col_c2:
                ops_opt = st.slider("운영비 절감률 (%)", 0, 25, 8, 1)
                rev_growth = st.slider("매출 성장률 (%)", -10, 30, 5, 1)
            
            total_rev_base = df_monthly['매출(만원)'].sum()
            total_labor = df_monthly['인건비(만원)'].sum()
            total_material = df_monthly['재료비(만원)'].sum()
            total_ops = df_monthly['운영비(만원)'].sum()
            total_cost_base = total_labor + total_material + total_ops
            total_profit_base = df_monthly['순이익(만원)'].sum()
            
            opt_labor = total_labor * (1 - labor_opt/100)
            opt_material = total_material * (1 - material_opt/100)
            opt_ops = total_ops * (1 - ops_opt/100)
            opt_cost = opt_labor + opt_material + opt_ops
            opt_rev = total_rev_base * (1 + rev_growth/100)
            opt_profit = opt_rev - opt_cost
            
            cost_saving = total_cost_base - opt_cost
            profit_improvement = opt_profit - total_profit_base
            
            col_opt1, col_opt2, col_opt3 = st.columns(3)
            with col_opt1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">비용 절감액</div>
                    <div class="metric-value" style="color:#34d399;">{cost_saving/1e4:.1f}억</div>
                    <div class="metric-delta-pos">연간 절감 효과</div>
                </div>
                """, unsafe_allow_html=True)
            with col_opt2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">이익 개선액</div>
                    <div class="metric-value" style="color:#34d399;">{profit_improvement/1e4:.1f}억</div>
                    <div class="metric-delta-pos">{profit_improvement/total_profit_base*100:+.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            with col_opt3:
                opt_margin = opt_profit/opt_rev*100 if opt_rev > 0 else 0
                base_margin2 = total_profit_base/total_rev_base*100
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">이익률 변화</div>
                    <div class="metric-value" style="color:#a78bfa;">{opt_margin:.1f}%</div>
                    <div style="color:#a78bfa;font-size:0.85rem">기준 {base_margin2:.1f}% → {opt_margin:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            # 비용 절감 워터폴 차트
            categories_w = ['현재 비용', '인건비 절감', '재료비 절감', '운영비 절감', '최적화 비용']
            values_w = [total_cost_base, -total_labor*labor_opt/100, -total_material*material_opt/100,
                        -total_ops*ops_opt/100, opt_cost]
            colors_w = ['#3b82f6', '#34d399', '#34d399', '#34d399', '#6366f1']
            
            fig_waterfall = go.Figure(go.Waterfall(
                x=categories_w,
                y=[total_cost_base, -total_labor*labor_opt/100, -total_material*material_opt/100,
                   -total_ops*ops_opt/100, 0],
                measure=['absolute','relative','relative','relative','total'],
                connector=dict(line=dict(color='#374151')),
                increasing=dict(marker_color='#f87171'),
                decreasing=dict(marker_color='#34d399'),
                totals=dict(marker_color='#6366f1')
            ))
            fig_waterfall.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', margin=dict(l=0,r=0,t=20,b=0), height=300,
                xaxis=dict(gridcolor='#1e2a3a'), yaxis=dict(gridcolor='#1e2a3a', title='비용(만원)')
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
        
        with sim_tab3:
            st.markdown("#### 신규 진료과 개설 타당성 시뮬레이션")
            
            col_n1, col_n2, col_n3 = st.columns(3)
            with col_n1:
                new_dept_name = st.text_input("신규 진료과명", value="성형외과")
                new_monthly_patients = st.number_input("월 예상 환자수", 50, 2000, 200, 10)
            with col_n2:
                new_avg_revenue = st.number_input("환자 1인당 평균 매출(만원)", 5, 200, 35, 5)
                new_margin_rate = st.slider("예상 이익률(%)", 5, 60, 25, 1)
            with col_n3:
                initial_investment = st.number_input("초기 투자비용(만원)", 1000, 100000, 15000, 500)
                setup_months = st.slider("안정화 기간(개월)", 3, 24, 6, 1)
            
            new_monthly_rev = new_monthly_patients * new_avg_revenue
            new_monthly_profit = new_monthly_rev * new_margin_rate / 100
            new_annual_rev = new_monthly_rev * 12
            new_annual_profit = new_monthly_profit * 12
            
            # ROI 계산
            roi = (new_annual_profit / initial_investment * 100) if initial_investment > 0 else 0
            payback_months = (initial_investment / new_monthly_profit) if new_monthly_profit > 0 else 999
            
            col_nk1, col_nk2, col_nk3, col_nk4 = st.columns(4)
            with col_nk1:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">예상 연간 매출</div>
                    <div class="metric-value">{new_annual_rev/1e4:.1f}억</div></div>""", unsafe_allow_html=True)
            with col_nk2:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">예상 연간 이익</div>
                    <div class="metric-value" style="color:#34d399;">{new_annual_profit/1e4:.1f}억</div></div>""", unsafe_allow_html=True)
            with col_nk3:
                roi_color = '#34d399' if roi > 20 else '#f59e0b' if roi > 10 else '#f87171'
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">투자수익률(ROI)</div>
                    <div class="metric-value" style="color:{roi_color};">{roi:.1f}%</div></div>""", unsafe_allow_html=True)
            with col_nk4:
                pb_color = '#34d399' if payback_months < 18 else '#f59e0b' if payback_months < 36 else '#f87171'
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">투자회수 기간</div>
                    <div class="metric-value" style="color:{pb_color};">{payback_months:.0f}개월</div></div>""", unsafe_allow_html=True)
            
            # 투자회수 곡선
            months_proj = list(range(1, 37))
            cumulative_profit = []
            cumul = -initial_investment
            for m in months_proj:
                if m <= setup_months:
                    monthly = new_monthly_profit * (m/setup_months) * 0.7
                else:
                    monthly = new_monthly_profit
                cumul += monthly
                cumulative_profit.append(cumul)
            
            fig_roi = go.Figure()
            colors_roi = ['#34d399' if v >= 0 else '#f87171' for v in cumulative_profit]
            fig_roi.add_trace(go.Scatter(
                x=months_proj, y=cumulative_profit,
                name='누적 손익',
                line=dict(color='#3b82f6', width=3),
                fill='tozeroy',
                fillcolor='rgba(59,130,246,0.1)'
            ))
            fig_roi.add_hline(y=0, line_color='#f59e0b', line_dash='dash',
                              annotation_text='손익분기', annotation_font_color='#f59e0b')
            fig_roi.update_layout(
                title=f'{new_dept_name} 개설 36개월 누적 손익 시뮬레이션',
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', margin=dict(l=0,r=0,t=40,b=0), height=300,
                xaxis=dict(gridcolor='#1e2a3a', title='월'),
                yaxis=dict(gridcolor='#1e2a3a', title='누적 손익(만원)')
            )
            st.plotly_chart(fig_roi, use_container_width=True)
            
            if roi > 30:
                st.markdown(f'<div class="alert-success">✅ <strong>투자 타당성 높음</strong>: ROI {roi:.1f}%로 {payback_months:.0f}개월 내 투자 회수 예상. {new_dept_name} 개설을 적극 검토하세요.</div>', unsafe_allow_html=True)
            elif roi > 15:
                st.markdown(f'<div class="alert-warning">⚠️ <strong>투자 타당성 보통</strong>: ROI {roi:.1f}%로 시장 조사 및 운영 계획 보완 후 결정을 권장합니다.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-danger">🚨 <strong>투자 위험 높음</strong>: ROI {roi:.1f}%로 현재 가정 기준으로는 투자 타당성이 낮습니다. 환자수·수가·비용 구조를 재검토하세요.</div>', unsafe_allow_html=True)
    else:
        premium_lock(
            "🔮 경영 시뮬레이션 센터",
            "수가·환자수 변동 시뮬레이션, 비용 구조 최적화 분석, 신규 진료과 개설 ROI 타당성 분석 등\n의사결정에 직접 활용할 수 있는 인터랙티브 시뮬레이션 도구를 제공합니다."
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6: 전략 보고서 (PREMIUM)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<span class="badge-premium">💎 전체 프리미엄 전용</span>', unsafe_allow_html=True)
    st.markdown("")
    
    if st.session_state.is_premium:
        # 데이터 기반 분석값 계산
        dept_s = df_monthly.groupby('진료과').agg(
            매출=('매출(만원)', 'sum'), 비용=('총비용(만원)', 'sum'),
            이익=('순이익(만원)', 'sum'), 환자수=('환자수', 'sum')
        ).reset_index()
        dept_s['이익률'] = dept_s['이익'] / dept_s['매출'] * 100
        
        top3_dept = dept_s.nlargest(3, '이익률')['진료과'].tolist()
        bot3_dept = dept_s.nsmallest(3, '이익률')['진료과'].tolist()
        total_rev_r = dept_s['매출'].sum()
        total_prof_r = dept_s['이익'].sum()
        overall_margin = total_prof_r/total_rev_r*100
        
        st.markdown("""
        <div class="section-header">
            <h2>📋 전문 경영 전략 보고서</h2>
            <p>데이터 기반 현황 진단 및 전략적 방향 제시 — 컨설팅 수준의 분석 리포트</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Executive Summary
        st.markdown(f"""
        <div class="report-card" style="border-left: 4px solid #3b82f6;">
            <h4>📌 Executive Summary</h4>
            <p>
            분석 기간 {analysis_year}년 기준, 병원 전체 매출은 <strong style="color:#60a5fa">{format_currency(total_rev_r*10000)}</strong>이며 
            전체 이익률은 <strong style="color:{'#34d399' if overall_margin >= 20 else '#f59e0b' if overall_margin >= 10 else '#f87171'}">{overall_margin:.1f}%</strong>를 기록하였습니다.
            {'의료기관 평균(15~20%) 대비 <strong style="color:#34d399">우수한 수준</strong>으로 안정적인 수익 구조를 보이고 있습니다.' if overall_margin >= 20 else '의료기관 평균(15~20%) 수준으로 <strong style="color:#f59e0b">추가 개선이 필요</strong>합니다.' if overall_margin >= 10 else '의료기관 평균 대비 <strong style="color:#f87171">현저히 낮은 수준</strong>으로 즉각적인 경영 개선이 필요합니다.'}
            핵심 수익 진료과는 <strong style="color:#60a5fa">{', '.join(top3_dept)}</strong>이며, 
            개선이 시급한 진료과는 <strong style="color:#f87171">{', '.join(bot3_dept)}</strong>입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 현황 진단
        st.markdown("#### 🔍 현황 진단")
        
        col_str1, col_str2 = st.columns(2)
        with col_str1:
            strength_depts = dept_s[dept_s['이익률'] >= dept_s['이익률'].quantile(0.67)]
            st.markdown(f"""
            <div class="report-card" style="border-left: 4px solid #34d399;">
                <h4>💪 강점 (Strengths)</h4>
                <p>
                • <strong>고수익 진료과 보유</strong>: {', '.join(strength_depts['진료과'].tolist())}는 
                평균 이익률 {strength_depts['이익률'].mean():.1f}%를 달성하며 병원 수익의 핵심 축으로 기능 중<br><br>
                • <strong>규모의 경제 가능성</strong>: 현재 진료 규모에서 고정비 레버리지를 활용한 
                추가 이익 창출 여력이 존재<br><br>
                • <strong>다각화된 포트폴리오</strong>: {len(dept_s)}개 진료과 운영으로 
                특정 과목 리스크 분산 효과 보유
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_str2:
            weak_depts = dept_s[dept_s['이익률'] < dept_s['이익률'].quantile(0.33)]
            labor_ratio = df_monthly['인건비(만원)'].sum() / df_monthly['매출(만원)'].sum() * 100
            st.markdown(f"""
            <div class="report-card" style="border-left: 4px solid #f87171;">
                <h4>⚠️ 약점 (Weaknesses)</h4>
                <p>
                • <strong>저수익 진료과 존재</strong>: {', '.join(weak_depts['진료과'].tolist())}의 
                수익성이 저조하여 전체 이익률을 하방 압박 중<br><br>
                • <strong>높은 인건비 비율</strong>: 전체 매출 대비 인건비 비율 {labor_ratio:.1f}%로 
                {'적정 수준(50~60%)' if 50 <= labor_ratio <= 60 else '개선 여지 있음'}<br><br>
                • <strong>계절 변동성</strong>: 월별 매출 편차가 크며, 비수기 대응 전략이 필요한 상황
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        col_str3, col_str4 = st.columns(2)
        with col_str3:
            st.markdown(f"""
            <div class="report-card" style="border-left: 4px solid #f59e0b;">
                <h4>🚀 기회 (Opportunities)</h4>
                <p>
                • <strong>비급여 진료 확대</strong>: 피부과·성형외과 등 비급여 중심 
                진료 라인업 강화로 수익성 향상 가능<br><br>
                • <strong>디지털 헬스케어 도입</strong>: 원격 진료, 모바일 예약 시스템 도입으로 
                운영 효율성 제고 및 환자 접근성 향상<br><br>
                • <strong>건강검진 패키지</strong>: 종합 건강검진 상품 개발로 
                환자 1인당 매출(LTV) 극대화 가능
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_str4:
            st.markdown(f"""
            <div class="report-card" style="border-left: 4px solid #8b5cf6;">
                <h4>🌩️ 위협 (Threats)</h4>
                <p>
                • <strong>의료 수가 정책 리스크</strong>: 건강보험 수가 동결 또는 
                인하 정책으로 인한 급여 매출 압박 가능성<br><br>
                • <strong>경쟁 심화</strong>: 지역 내 대형병원 확장 및 의원급 
                경쟁 증가로 환자 유출 위험<br><br>
                • <strong>의료 인력 비용 상승</strong>: 의사·간호사 인건비 상승 추세로 
                인건비율 악화 가능성
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 전략 방향
        st.markdown("#### 🎯 전략적 방향 제시 (3개년 로드맵)")
        
        st.markdown(f"""
        <div class="report-card" style="border-left: 4px solid #3b82f6;">
            <h4>📅 단기 (1년): 비용 구조 최적화 및 핵심 수익원 강화</h4>
            <p>
            ① <strong>저수익 진료과 수익성 개선</strong>: {', '.join(bot3_dept)} 진료과의 
            인건비·재료비 절감 방안 수립 및 환자당 수익 향상 프로그램 도입<br>
            ② <strong>핵심 진료과 역량 강화</strong>: {', '.join(top3_dept)} 진료과의 환자 유치 마케팅 
            강화 및 진료 역량 투자로 매출 성장 가속화<br>
            ③ <strong>비용 효율화</strong>: 재료비 공동구매 협상, 운영 자동화, 에너지 절감 등 
            즉시 실행 가능한 비용 절감 과제 추진 (목표: 비용률 3~5%p 개선)<br>
            ④ <strong>환자 경험 개선</strong>: 대기 시간 단축, 예약 시스템 고도화로 
            환자 만족도 향상 및 재방문율 제고
            </p>
        </div>
        
        <div class="report-card" style="border-left: 4px solid #f59e0b;">
            <h4>📅 중기 (2~3년): 성장 동력 확보 및 포트폴리오 재편</h4>
            <p>
            ① <strong>고수익 비급여 영역 확장</strong>: 피부미용, 건강증진, 도수치료 등 
            비급여 비중을 현재 대비 20~30% 확대하여 수익성 구조 개선<br>
            ② <strong>신규 수익원 개발</strong>: 건강검진 센터 운영, 기업 제휴 클리닉, 
            리조트 협력 건강관리 프로그램 등 부가 수익원 발굴<br>
            ③ <strong>의료 정보화 투자</strong>: EMR 고도화, AI 진단 보조 시스템 도입으로 
            진료 생산성 향상 및 오진 리스크 감소<br>
            ④ <strong>인력 구조 최적화</strong>: PA(진료지원인력) 활용 확대, 의사 1인당 생산성 
            개선, 성과연동형 보상 체계 도입
            </p>
        </div>
        
        <div class="report-card" style="border-left: 4px solid #34d399;">
            <h4>📅 장기 (3년+): 지역 거점 의료기관으로의 도약</h4>
            <p>
            ① <strong>규모 확장</strong>: 분원 설립 또는 협력 의원 네트워크 구축으로 
            지역 내 의료 접근성 강화 및 브랜드 파워 확대<br>
            ② <strong>전문화·차별화</strong>: 특정 질환(당뇨, 심장, 관절 등) 특화 센터 운영으로 
            경쟁 병원과의 차별화 포지셔닝 확보<br>
            ③ <strong>디지털 전환</strong>: 원격 모니터링, 만성질환 관리 플랫폼 구축으로 
            환자 생애주기 전반을 커버하는 헬스케어 파트너로 포지셔닝<br>
            ④ <strong>목표 수익성</strong>: 이익률 {min(overall_margin + 8, 35):.0f}% 이상, 
            매출 {total_rev_r*1.3/1e4:.0f}억원 달성
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 핵심 KPI 목표
        st.markdown("#### 📌 권장 KPI 목표치")
        
        kpi_data = {
            'KPI 지표': ['전체 이익률', '인건비율', '재료비율', '환자 1인당 매출', '의사 1인당 연매출', '환자 재방문율'],
            '현재 수준': [
                f"{overall_margin:.1f}%",
                f"{df_monthly['인건비(만원)'].sum()/df_monthly['매출(만원)'].sum()*100:.1f}%",
                f"{df_monthly['재료비(만원)'].sum()/df_monthly['매출(만원)'].sum()*100:.1f}%",
                f"{df_monthly['매출(만원)'].sum()/df_monthly['환자수'].sum():.0f}만원",
                "산출 중",
                "측정 필요"
            ],
            '1년 목표': [
                f"{min(overall_margin+5, 35):.0f}%",
                f"{max(df_monthly['인건비(만원)'].sum()/df_monthly['매출(만원)'].sum()*100-3, 45):.0f}%",
                f"{max(df_monthly['재료비(만원)'].sum()/df_monthly['매출(만원)'].sum()*100-2, 15):.0f}%",
                f"{df_monthly['매출(만원)'].sum()/df_monthly['환자수'].sum()*1.1:.0f}만원",
                "5억+",
                "40%+"
            ],
            '3년 목표': [
                f"{min(overall_margin+12, 40):.0f}%",
                "50% 이하",
                "18% 이하",
                f"{df_monthly['매출(만원)'].sum()/df_monthly['환자수'].sum()*1.25:.0f}만원",
                "7억+",
                "55%+"
            ]
        }
        
        kpi_df = pd.DataFrame(kpi_data)
        st.dataframe(kpi_df, use_container_width=True, hide_index=True)
        
    else:
        premium_lock(
            "📋 전문 경영 전략 보고서",
            "SWOT 기반 현황 진단, 3개년 전략 로드맵, KPI 목표 수립, 진료과별 맞춤 전략 등\n컨설팅 수준의 완성형 전략 보고서를 자동 생성합니다."
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 7: 리스크 진단 (PREMIUM)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<span class="badge-premium">💎 전체 프리미엄 전용</span>', unsafe_allow_html=True)
    st.markdown("")
    
    if st.session_state.is_premium:
        st.markdown("""
        <div class="section-header">
            <h2>⚠️ 경영 리스크 진단 대시보드</h2>
            <p>잠재 리스크 조기 탐지 및 대응 방안 제시</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 리스크 지표 계산
        dept_risk = df_monthly.groupby('진료과').agg(
            매출=('매출(만원)', 'sum'), 이익=('순이익(만원)', 'sum'),
            인건비=('인건비(만원)', 'sum'), 환자수=('환자수', 'sum')
        ).reset_index()
        dept_risk['이익률'] = dept_risk['이익'] / dept_risk['매출'] * 100
        dept_risk['인건비율'] = dept_risk['인건비'] / dept_risk['매출'] * 100
        
        total_rev_risk = dept_risk['매출'].sum()
        
        # 집중도 리스크
        top1_share = dept_risk.nlargest(1, '매출')['매출'].values[0] / total_rev_risk * 100
        top2_share = dept_risk.nlargest(2, '매출')['매출'].sum() / total_rev_risk * 100
        
        # 월별 변동성
        monthly_rev_std = df_monthly.groupby('월번호')['매출(만원)'].sum().std()
        monthly_rev_mean = df_monthly.groupby('월번호')['매출(만원)'].sum().mean()
        cv = monthly_rev_std / monthly_rev_mean * 100  # 변동계수
        
        # 손실 진료과 수
        loss_depts = dept_risk[dept_risk['이익'] < 0]
        low_margin_depts = dept_risk[dept_risk['이익률'] < 10]
        high_labor_depts = dept_risk[dept_risk['인건비율'] > 65]
        
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        
        with col_r1:
            risk_level = "🔴 고위험" if top1_share > 40 else "🟡 중위험" if top1_share > 25 else "🟢 저위험"
            color_r = '#f87171' if top1_share > 40 else '#f59e0b' if top1_share > 25 else '#34d399'
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">매출 집중도 리스크</div>
                <div class="metric-value" style="color:{color_r};font-size:1.3rem">{risk_level}</div>
                <div style="color:#64748b;font-size:0.8rem">1위 진료과 비중: {top1_share:.1f}%</div>
            </div>""", unsafe_allow_html=True)
        
        with col_r2:
            risk_level2 = "🔴 고위험" if cv > 20 else "🟡 중위험" if cv > 10 else "🟢 저위험"
            color_r2 = '#f87171' if cv > 20 else '#f59e0b' if cv > 10 else '#34d399'
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">계절 변동성 리스크</div>
                <div class="metric-value" style="color:{color_r2};font-size:1.3rem">{risk_level2}</div>
                <div style="color:#64748b;font-size:0.8rem">변동계수(CV): {cv:.1f}%</div>
            </div>""", unsafe_allow_html=True)
        
        with col_r3:
            risk_level3 = "🔴 고위험" if len(loss_depts) > 2 else "🟡 중위험" if len(loss_depts) > 0 else "🟢 저위험"
            color_r3 = '#f87171' if len(loss_depts) > 2 else '#f59e0b' if len(loss_depts) > 0 else '#34d399'
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">적자 진료과 리스크</div>
                <div class="metric-value" style="color:{color_r3};font-size:1.3rem">{risk_level3}</div>
                <div style="color:#64748b;font-size:0.8rem">적자 진료과: {len(loss_depts)}개</div>
            </div>""", unsafe_allow_html=True)
        
        with col_r4:
            risk_level4 = "🔴 고위험" if len(high_labor_depts) > 3 else "🟡 중위험" if len(high_labor_depts) > 1 else "🟢 저위험"
            color_r4 = '#f87171' if len(high_labor_depts) > 3 else '#f59e0b' if len(high_labor_depts) > 1 else '#34d399'
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">인건비 부담 리스크</div>
                <div class="metric-value" style="color:{color_r4};font-size:1.3rem">{risk_level4}</div>
                <div style="color:#64748b;font-size:0.8rem">인건비율 65%↑: {len(high_labor_depts)}개과</div>
            </div>""", unsafe_allow_html=True)
        
        st.markdown("---")
        
        col_risk_a, col_risk_b = st.columns(2)
        
        with col_risk_a:
            # 리스크 레이더 차트
            st.markdown("#### 🕷️ 종합 리스크 레이더")
            
            risk_scores = {
                '매출 집중도': min(top1_share/50*10, 10),
                '계절 변동성': min(cv/25*10, 10),
                '인건비 부담': min(df_monthly['인건비(만원)'].sum()/df_monthly['매출(만원)'].sum()*100/70*10, 10),
                '저마진 진료과': min(len(low_margin_depts)/len(dept_risk)*10, 10),
                '적자 진료과': min(len(loss_depts)/len(dept_risk)*10*2, 10),
                '수익성': max(0, (20-overall_margin)/20*10)
            }
            
            categories_radar = list(risk_scores.keys())
            values_radar = list(risk_scores.values())
            values_radar.append(values_radar[0])
            categories_radar.append(categories_radar[0])
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values_radar, theta=categories_radar,
                fill='toself', fillcolor='rgba(239,68,68,0.15)',
                line=dict(color='#ef4444', width=2),
                name='현재 리스크'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[5]*len(categories_radar), theta=categories_radar,
                fill='toself', fillcolor='rgba(59,130,246,0.05)',
                line=dict(color='#3b82f6', width=1, dash='dash'),
                name='적정 수준(5점)'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0,10], tickfont=dict(color='#64748b')),
                    angularaxis=dict(tickfont=dict(color='#94a3b8')),
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8',
                legend=dict(bgcolor='rgba(0,0,0,0)'),
                margin=dict(l=30,r=30,t=30,b=30), height=380
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col_risk_b:
            st.markdown("#### 📋 리스크 상세 진단표")
            
            risk_items = []
            
            if top1_share > 40:
                risk_items.append({'리스크': '매출 집중도 과다', '수준': '🔴 고위험', '내용': f'1위 진료과 매출 비중 {top1_share:.1f}%. 해당 과 위기 시 전체 수익 급락 위험', '대응': '하위 진료과 육성, 신규 수익원 개발'})
            elif top1_share > 25:
                risk_items.append({'리스크': '매출 집중도', '수준': '🟡 중위험', '내용': f'상위 2개 진료과가 매출 {top2_share:.1f}% 점유. 다각화 필요', '대응': '포트폴리오 다각화 전략 수립'})
            
            if cv > 10:
                risk_items.append({'리스크': '계절 변동성', '수준': '🔴 고위험' if cv > 20 else '🟡 중위험', '내용': f'월별 매출 변동계수 {cv:.1f}%. 비수기 현금흐름 불안정', '대응': '비수기 프로모션, 건강검진 패키지 강화'})
            
            for _, row in dept_risk[dept_risk['이익률'] < 0].iterrows():
                risk_items.append({'리스크': f'{row["진료과"]} 적자', '수준': '🔴 고위험', '내용': f'이익률 {row["이익률"]:.1f}%로 지속 적자 중', '대응': '원가 절감, 수가 조정, 또는 폐쇄 검토'})
            
            for _, row in dept_risk[(dept_risk['이익률'] >= 0) & (dept_risk['이익률'] < 10)].iterrows():
                risk_items.append({'리스크': f'{row["진료과"]} 저수익', '수준': '🟡 중위험', '내용': f'이익률 {row["이익률"]:.1f}%로 병원 평균 하회', '대응': '비용 절감 및 환자당 수익 향상 방안 수립'})
            
            for _, row in dept_risk[dept_risk['인건비율'] > 65].iterrows():
                risk_items.append({'리스크': f'{row["진료과"]} 인건비 과다', '수준': '🟡 중위험', '내용': f'인건비율 {row["인건비율"]:.1f}%로 비정상적으로 높음', '대응': 'PA 활용, 파트타임 조정, 성과급 체계 도입'})
            
            if not risk_items:
                risk_items.append({'리스크': '전반적 양호', '수준': '🟢 저위험', '내용': '현재 주요 리스크 지표 모두 양호한 수준', '대응': '현 전략 유지 및 성장 기회 탐색'})
            
            risk_df = pd.DataFrame(risk_items)
            st.dataframe(risk_df, use_container_width=True, hide_index=True, height=400)
        
        # 현금흐름 스트레스 테스트
        st.markdown("""
        <div class="section-header">
            <h2>💉 스트레스 테스트 — 최악의 시나리오 분석</h2>
            <p>외부 충격 발생 시 병원 수익성에 미치는 영향 시뮬레이션</p>
        </div>
        """, unsafe_allow_html=True)
        
        base_profit_st = df_monthly['순이익(만원)'].sum()
        base_rev_st = df_monthly['매출(만원)'].sum()
        
        scenarios = {
            '수가 10% 인하': base_rev_st * (-0.10),
            '환자 20% 감소': base_rev_st * (-0.20),
            '인건비 15% 상승': df_monthly['인건비(만원)'].sum() * (-0.15),
            '재료비 20% 상승': df_monthly['재료비(만원)'].sum() * (-0.20),
            '복합 위기 (수가↓+환자↓)': base_rev_st * (-0.15) + base_rev_st * (-0.15)
        }
        
        stress_results = []
        for scenario, impact in scenarios.items():
            new_profit = base_profit_st + impact
            change_pct = (impact / base_profit_st * 100) if base_profit_st != 0 else 0
            new_margin = (new_profit / (base_rev_st + (impact if '수가' in scenario or '환자' in scenario else 0)) * 100)
            stress_results.append({
                '시나리오': scenario,
                '이익 충격(만원)': round(impact, 0),
                '충격 후 순이익(만원)': round(new_profit, 0),
                '이익 변화율(%)': round(change_pct, 1),
                '예상 이익률(%)': round(new_margin, 1),
                '위험도': '🔴 위험' if new_profit < 0 else '🟡 주의' if change_pct < -30 else '🟢 양호'
            })
        
        stress_df = pd.DataFrame(stress_results)
        st.dataframe(
            stress_df.style.map(
                lambda v: 'color: #f87171' if isinstance(v, (int,float)) and v < 0 else 'color: #34d399' if isinstance(v, (int,float)) and v > 0 else '',
                subset=['이익 충격(만원)', '충격 후 순이익(만원)', '이익 변화율(%)']
            ),
            use_container_width=True, hide_index=True
        )
        
    else:
        premium_lock(
            "⚠️ 경영 리스크 진단",
            "매출 집중도·계절 변동성·인건비 부담·적자 진료과 등 주요 리스크를 정량 분석하고,\n스트레스 테스트(최악 시나리오 시뮬레이션)를 통해 경영 취약성을 사전에 진단합니다."
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 8: 데이터 입력 가이드 (FREE)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<span class="badge-free">🆓 무료 제공</span>', unsafe_allow_html=True)
    st.markdown("")
    
    st.markdown("""
    <div class="section-header">
        <h2>📥 엑셀 데이터 입력 가이드</h2>
        <p>정확한 분석을 위한 데이터 형식 안내 및 다운로드</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="report-card">
        <h4>📋 Sheet 1 — 월별 진료과 데이터 (필수)</h4>
        <p>
        다음 컬럼을 포함한 엑셀 시트를 준비하세요:<br><br>
        <strong style="color:#60a5fa">필수 컬럼</strong><br>
        • <code>월</code>: 1월, 2월 ... 12월 (또는 1, 2 ... 12)<br>
        • <code>진료과</code>: 내과, 외과, 정형외과 등 진료과명<br>
        • <code>매출(만원)</code>: 해당 월 해당 진료과 총 매출<br>
        • <code>인건비(만원)</code>: 해당 월 해당 진료과 인건비 합계<br>
        • <code>재료비(만원)</code>: 해당 월 해당 진료과 재료비·약품비 합계<br>
        • <code>운영비(만원)</code>: 관리비, 임차료, 감가상각 등 기타 운영비<br>
        • <code>환자수</code>: 해당 월 해당 진료과 총 환자수(연인원)<br><br>
        <strong style="color:#f59e0b">선택 컬럼 (있으면 더 정확한 분석 가능)</strong><br>
        • <code>의사수</code>: 해당 진료과 의사 수<br>
        • <code>총비용(만원)</code>: 인건비+재료비+운영비 합계<br>
        • <code>순이익(만원)</code>: 매출-총비용<br>
        • <code>이익률(%)</code>: 순이익/매출 × 100
        </p>
    </div>
    
    <div class="report-card">
        <h4>📋 Sheet 2 — 행위별 데이터 (선택, 프리미엄 분석용)</h4>
        <p>
        • <code>진료과</code>: 진료과명<br>
        • <code>행위명</code>: 진찰료, 처치비, 검사비, 약제비, 수술비 등<br>
        • <code>건수</code>: 해당 행위 연간 시행 건수<br>
        • <code>매출(만원)</code>: 해당 행위 연간 총 매출<br>
        • <code>직접비용(만원)</code>: 해당 행위에 직접 소요되는 재료비·인건비<br>
        • <code>마진율(%)</code>: (매출-직접비용)/매출 × 100
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 샘플 엑셀 다운로드
    st.markdown("#### 📥 샘플 엑셀 템플릿 다운로드")
    
    # 샘플 데이터 생성
    sample_df1, sample_df2 = generate_sample_data()
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sample_df1.drop(columns=['월번호'], errors='ignore').to_excel(writer, sheet_name='월별_진료과_데이터', index=False)
        sample_df2.to_excel(writer, sheet_name='행위별_데이터', index=False)
    excel_bytes = output.getvalue()
    
    st.download_button(
        label="📥 샘플 엑셀 템플릿 다운로드 (.xlsx)",
        data=excel_bytes,
        file_name="병원수익성분석_샘플템플릿.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.markdown("""
    <div class="alert-info">
        💡 <strong>Tip</strong>: 샘플 템플릿을 다운로드하여 실제 병원 데이터로 교체한 뒤 업로드하시면 됩니다. 
        컬럼명을 동일하게 유지해주세요. 금액 단위는 <strong>만원</strong> 기준입니다.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="alert-warning">
        ⚠️ <strong>개인정보 주의</strong>: 업로드된 데이터는 분석 후 저장되지 않습니다. 
        환자 개인정보가 포함되지 않도록 집계 형태의 데이터만 업로드하세요.
    </div>
    """, unsafe_allow_html=True)
