import streamlit as st
from db.connection import iniciar_supabase

# Configuração do Supabase
supabase = iniciar_supabase()


def autenticar_usuario(email, senha):
    """
    Realiza a autenticação do usuário no Supabase.
    """
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": senha})
        if response.user:  # Verifica se o usuário foi autenticado
            return response
        else:
            return None
    except Exception as e:
        st.error(f"Erro ao autenticar: {e}")
        return None


def tela_login():
    """
    Renderiza o login na sidebar e autentica o usuário.
    """
    st.sidebar.title("Login")

    # Verifica se o usuário já está autenticado
    if "login_ok" in st.session_state and st.session_state["login_ok"]:
        # Se já estiver logado, renderiza a tela principal
        return True  # Usuário logado, retorna True

    # Caso contrário, exibe os campos de login
    email = st.sidebar.text_input("Email")
    senha = st.sidebar.text_input("Senha", type="password")

    # Adiciona o botão de logout na parte inferior da sidebar
    st.sidebar.markdown("""
          <style>
              .entrar-button {
                  position: absolute;
                  bottom: 10px;
                  width: 100%;
              }
          </style>
      """, unsafe_allow_html=True)

    if st.sidebar.button("Entrar", key = "entrar", help = "Entrar na aplicação", use_container_width = True):
        usuario = autenticar_usuario(email, senha)
        if usuario:
            # Salva o usuário autenticado na sessão
            st.session_state["usuario"] = usuario

            # Marca o login como bem-sucedido
            st.session_state["login_ok"] = True

            # Define a página atual como "home"
            st.session_state["pagina_atual"] = "home"
            st.rerun()

        else:
            st.sidebar.error("Credenciais inválidas! Verifique seu email e senha.")
            return False  # Login falhou, retorna False
