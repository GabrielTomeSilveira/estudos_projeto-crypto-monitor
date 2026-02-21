import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Crypto Monitor Dashboard", page_icon="📈", layout="wide")
st.title("📊 Monitor de Criptomoedas - Dados em Tempo Real")

@st.cache_resource
def get_engine():
    user = os.getenv("DB_USER", "dev_user")
    password = os.getenv("DB_PASSWORD", "dev_password")
    host = os.getenv("DB_HOST", "postgres")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "crypto_analytics")
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)

engine = get_engine()

@st.cache_data(ttl=60)
def load_data():
    query = """
        SELECT coin_id, price_brl, market_cap_brl, volume_brl, extracted_at
        FROM precos_crypto
        ORDER BY extracted_at DESC
        LIMIT 1000
    """
    with engine.connect() as conn:
        # Usa a conexão DBAPI bruta (raw), que tem o método cursor()
        raw_conn = conn.connection
        df = pd.read_sql(query, raw_conn)
    return df

st.sidebar.header("Configurações")
auto_refresh = st.sidebar.checkbox("Auto-refresh a cada 60s", value=True)

df = load_data()

st.sidebar.subheader("Estatísticas")
st.sidebar.write(f"Total de registros no banco: {len(df)}")
st.sidebar.write(f"Última atualização: {df['extracted_at'].max()}")

st.subheader("📋 Últimos Registros")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("📈 Evolução dos Preços")
coins = df['coin_id'].unique()
selected_coin = st.selectbox("Selecione a moeda", coins)

df_coin = df[df['coin_id'] == selected_coin].sort_values('extracted_at')

if not df_coin.empty:
    fig_price = px.line(df_coin, x='extracted_at', y='price_brl', title=f'Preço de {selected_coin} (BRL)')
    st.plotly_chart(fig_price, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_mcap = px.line(df_coin, x='extracted_at', y='market_cap_brl', title='Market Cap')
        st.plotly_chart(fig_mcap, use_container_width=True)
    with col2:
        fig_vol = px.line(df_coin, x='extracted_at', y='volume_brl', title='Volume')
        st.plotly_chart(fig_vol, use_container_width=True)
else:
    st.warning("Sem dados para a moeda selecionada.")

if st.button("Recarregar dados"):
    st.cache_data.clear()
    st.rerun()

if auto_refresh:
    st.empty()
    st.toast("Atualizando automaticamente a cada 60s...")