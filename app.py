import pandas as pd
import streamlit as st
import plotly_express as px


st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
)

pf = pd.read_csv("C:/Users/vinis/OneDrive/Documentos/dashboard de vendas/base_vendas - Sheet2.csv")

print(pf.columns.tolist())


st.title("Dashboard de Vendas")
st.markdown("Exploe o balanço de uma loja de tecnologia focada no seu desenvolvimento pessoal, \n"
" com as melgores marcas e preço para o seu bolso")



st.sidebar.header("🔍 Filtros")

#Filtro de Produto

Produto_disponiveis = sorted( str(p) for p in  pf['Produto'].unique() if pd.notnull(p))
produto_selecionaveis = st.sidebar.multiselect("Produto", Produto_disponiveis, default= Produto_disponiveis)

#filro de Clientes

pf.columns = pf.columns.str.strip()
clientes_disponiveis = sorted(map(str, pf['clientes'].dropna().unique()))
clientes_selecionaveis = st.sidebar.multiselect("clientes", clientes_disponiveis, default=clientes_disponiveis)

pf_Filtrado = pf[
    (pf["clientes"].isin(clientes_selecionaveis))&
    (pf["Produto"].isin(produto_selecionaveis))
] 

st.markdown("-----")
# graficos 
st.subheader("Gráficos")

col_graf1, col_graf2= st.columns(2) 
#grafico de barra e linha
with col_graf1:
    if not pf_Filtrado.empty:
        top_produtos = (pf_Filtrado.groupby('Produto')['Faturamento'].mean().nlargest(10).sort_values(ascending=True).reset_index())
        graficos_Produtos = px.bar(
            top_produtos,
            y='Faturamento',
            x='Produto',
            orientation='v',
            title="Faturamento por Produto",
            labels={'Faturamento': 'Faturamento anual em Real', 'Produto': ''}
        )
        graficos_Produtos.update_layout(title='Faturamento por Produto', yaxis={'categoryorder':'total ascending'})
    else:
        st.warning("Nenhum dado para exibir no gráfico")
    st.plotly_chart(graficos_Produtos,use_container_width=True ) 

    st.markdown("-----")

with col_graf2:
    if not pf_Filtrado.empty:
        qnt_vendidos =  (pf_Filtrado.groupby('Produto')['quantidade vendida'].mean().nlargest(10).sort_values(ascending=True).reset_index())
        grafivo_vendido = px.line (
            qnt_vendidos,
            y='quantidade vendida', 
            x='Produto',
            orientation='h', 
            title='Quantidade de Produtos Vendidos',
            labels={'quantidade vendida': 'Unidade por produto','Produto':''} 
        )
        grafivo_vendido.update_layout(title='Quantidade de Produtos Vendidos', yaxis={'categoryorder': 'total ascending'})
    else:
        st.warning("Nenhum dado a ser Exibido")
    st.plotly_chart(grafivo_vendido,use_container_width=True)

#grafico de barra e area
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not pf_Filtrado.empty:
        clinete_gasto = (pf_Filtrado.groupby('clientes')['Gasto Cliente'].mean().nlargest(1000).sort_values(ascending= True).reset_index())
        grafico_clinete_gasto = px.bar(
            clinete_gasto,
            y='clientes',
            x='Gasto Cliente',
            orientation='h',
            title= 'Gasto por cliente',
            labels={'Clientes': 'Clientes', 'Gasto Cliente':''}
        )
        grafico_clinete_gasto.update_layout(title='Gasto por cliente', yaxis={'categoryorder':'total ascending'})
    else:
        st.warning('Erro ao exibir')
    st.plotly_chart( grafico_clinete_gasto,use_container_width=True)

with col_graf4:
    if not pf_Filtrado.empty:
     fatu_mes= (pf_Filtrado.groupby('Mês')['Faturamento por mês'].mean().nlargest().sort_values(ascending=True).reset_index())
     grafico_fatume=px.line(
         fatu_mes,
         y='Mês',
         x='Faturamento por mês',
         title='Faturamento mensal',
         labels={'Meses':'','Faturamento':''}
     )
     grafico_fatume.update_layout(title='Faturamento Mensal', yaxis={'categoryorder': 'total ascending'})                                       
  
     st.plotly_chart(grafico_fatume, use_container_width=True)