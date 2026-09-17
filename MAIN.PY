import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Portal do Bolão", layout="centered")

# DEFINA A SENHA DO GRUPO AQUI
SENHA_ACESSO = "bolao123"

# Controle de login
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
    
    # Abas do sistema conforme o escopo original
    aba1, aba2, aba3 = st.tabs(["🔍 Conferência", "📑 Jogos & Recibo", "⚙️ Área do Administrador"])
    
    # Variáveis de memória do sistema
    if "jogos_df" not in st.session_state:
        st.session_state.jogos_df = None
    if "recibo_foto" not in st.session_state:
        st.session_state.recibo_foto = None

    # 1. ÁREA DO ADMINISTRADOR (UPLOAD)
    with aba3:
        st.subheader("📤 Envio de Dados")
        arquivo_excel = st.file_uploader("Suba o arquivo Excel (.xlsx) com os 1.000 jogos:", type=["xlsx"])
        foto_recibo = st.file_uploader("Suba a foto do Recibo Geral da Lotérica:", type=["png", "jpg", "jpeg"])
        
        if arquivo_excel:
            # Lê o Excel desconsiderando cabeçalhos para pegar apenas os números
            df = pd.read_excel(arquivo_excel, header=None)
            st.session_state.jogos_df = df
            st.success(f"Sucesso! {len(df)} jogos carregados do Excel.")
            
        if foto_recibo:
            st.session_state.recibo_foto = foto_recibo.read()
            st.success("Foto do recibo atualizada com sucesso.")

    # 2. TRANSPARÊNCIA (JOGOS E COMPROVANTE)
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

    # 3. CONFERÊNCIA INDEPENDENTE
    with aba1:
        st.subheader("🧮 Painel de Conferência")
        st.write("Digite as 15 dezenas sorteadas para cruzar com os jogos:")
        
        # Criação dos 15 campos numéricos organizados na tela
        c1, c2, c3, c4, c5 = st.columns(5)
        c6, c7, c8, c9, c10 = st.columns(5)
        c11, c12, c13, c14, c15 = st.columns(5)
        
        sorteio = []
        sorteio.append(c1.number_input("N1", min_value=1, max_value=25, value=1))
        sorteio.append(c2.number_input("N2", min_value=1, max_value=25, value=2))
        sorteio.append(c3.number_input("N3", min_value=1, max_value=25, value=3))
        sorteio.append(c4.number_input("N4", min_value=1, max_value=25, value=4))
        sorteio.append(c5.number_input("N5", min_value=1, max_value=25, value=5))
        
        sorteio.append(c6.number_input("N6", min_value=1, max_value=25, value=6))
        sorteio.append(c7.number_input("N7", min_value=1, max_value=25, value=7))
        sorteio.append(c8.number_input("N8", min_value=1, max_value=25, value=8))
        sorteio.append(c9.number_input("N9", min_value=1, max_value=25, value=9))
        sorteio.append(c10.number_input("N10", min_value=1, max_value=25, value=10))
        
        sorteio.append(c11.number_input("N11", min_value=1, max_value=25, value=11))
        sorteio.append(c12.number_input("N12", min_value=1, max_value=25, value=12))
        sorteio.append(c13.number_input("N13", min_value=1, max_value=25, value=13))
        sorteio.append(c14.number_input("N14", min_value=1, max_value=25, value=14))
        sorteio.append(c15.number_input("N15", min_value=1, max_value=25, value=15))
        
        if st.button("Conferir Jogos", type="primary"):
            if st.session_state.jogos_df is None:
                st.error("Erro: O administrador ainda não fez o upload do arquivo Excel.")
            elif len(set(sorteio)) != 15:
                st.error("Erro: Existem números repetidos nos campos do sorteio.")
            else:
                # Motor de busca matemática ultra rápido
                set_sorteio = set(sorteio)
                faixas_acertos = {11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
                
                for _, linha in st.session_state.jogos_df.iterrows():
                    jogo_numeros = set(linha.values)
                    total_acertos = len(jogo_numeros.intersection(set_sorteio))
                    if total_acertos in faixas_acertos:
                        faixas_acertos[total_acertos] += 1
                
                # Exibe o relatório final na tela
                st.success("📊 Relatório de Desempenho do Bolão:")
                res_df = pd.DataFrame(list(faixas_acertos.items()), columns=["Acertos", "Total de Cartões"])
                st.table(res_df)
