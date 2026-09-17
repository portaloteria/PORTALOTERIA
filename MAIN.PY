# pip install pandas openpyxl
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portal do Bolão", layout="centered")

SENHA_ACESSO = "bolao123"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 Acesso Privado ao Bolão")
    senha = st.text_input("Digite a senha do grupo:", type="password")
    if st.button("Entrar"):
        if senha == SENHA_ACESSO:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
else:
    st.title("🏆 Portal Web do Bolão")
    st.write("Acompanhamento transparente e conferência independente.")
    
    aba1, aba2, aba3 = st.tabs(["🔍 Conferência", "📑 Jogos & Recibo", "⚙️ Área do Administrador"])
    
    if "jogos_df" not in st.session_state:
        st.session_state.jogos_df = None
    if "recibo_foto" not in st.session_state:
        st.session_state.recibo_foto = None

    with aba3:
        st.subheader("📤 Envio de Dados")
        arquivo_excel = st.file_uploader("Suba o arquivo Excel (.xlsx) com os 1.000 jogos:", type=["xlsx"])
        foto_recibo = st.file_uploader("Suba a foto do Recibo Geral da Lotérica:", type=["png", "jpg", "jpeg"])
        
        if arquivo_excel:
            try:
                df = pd.read_excel(arquivo_excel, header=None)
                st.session_state.jogos_df = df
                st.success(f"Sucesso! {len(df)} jogos carregados do Excel.")
            except Exception as e:
                st.error(f"Erro ao ler o Excel: {e}")
            
        if foto_recibo:
            st.session_state.recibo_foto = foto_recibo.read()
            st.success("Foto do recibo updated.")

    with aba2:
        st.subheader("📸 Prova Real e Auditoria")
        if st.session_state.recibo_foto:
            st.image(st.session_state.recibo_foto, caption="Comprovante Geral de Pagamento da Lotérica", use_container_width=True)
        else:
            st.info("Nenhum recibo foi publicado para este concurso ainda.")
            
        st.subheader("📋 Lista Completa de Apostas")
        if st.session_state.jogos_df is not None:
            st.write(st.session_state.jogos_df)
        else:
            st.info("Aguardando o upload dos jogos em Excel.")

    with aba1:
        st.subheader("🧮 Painel de Conferência")
        st.write("Digite as 15 dezenas sorteadas para cruzar com os jogos:")
        
        cols = [st.columns(5) for _ in range(3)]
        sorteio = []
        contador = 1
        
        for i in range(3):
            for j in range(5):
                num = cols[i][j].number_input(f"N{contador}", min_value=1, max_value=25, value=contador)
                sorteio.append(num)
                contador += 1
        
        if st.button("Conferir Jogos", type="primary"):
            if st.session_state.jogos_df is None:
                st.error("Erro: O administrador ainda não fez o upload do arquivo Excel.")
            elif len(set(sorteio)) != 15:
                st.error("Erro: Existem números repetidos nos campos do sorteio.")
            else:
                set_sorteio = set(sorteio)
                faixas_acertos = {11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
                
                for _, linha in st.session_state.jogos_df.iterrows():
                    jogo_numeros = set(linha.dropna().values)
                    total_acertos = len(jogo_numeros.intersection(set_sorteio))
                    if total_acertos in faixas_acertos:
                        faixas_acertos[total_acertos] += 1
                
                st.success("📊 Relatório de Desempenho do Bolão:")
                res_df = pd.DataFrame(list(faixas_acertos.items()), columns=["Acertos", "Total de Cartões"])
                st.table(res_df)
