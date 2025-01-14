import streamlit as st
from streamlit import sidebar
from login import tela_login
from db.servicos import cadastrar_servico, listar_servicos, deletar_servico
from db.atendimentos import adicionar_atendimento, listar_atendimentos, deletar_atendimento
from db.servicos import atualizar_valor_servico
from services.resumo import consultar_resumo
from datetime import datetime
from db.connection import iniciar_supabase
from services.export import gerar_resumo_pdf, gerar_resumo_excel

# Definir o ícone e o título da página
st.set_page_config(page_title="Gerenciamento de Atendimentos", page_icon="src/favicon1.png")

supabase = iniciar_supabase()

if supabase is None:
    raise RuntimeError("Cliente Supabase não foi inicializado. Verifique suas credenciais e o arquivo secrets.toml.")

# Operações com o cliente
try:
    response = supabase.from_("servicos").select("*").execute()
    print(response)
except Exception as e:
    print(f"Erro ao acessar a tabela 'servicos': {e}")



# Função principal
def tela_principal():
    # Adicionar imagem de perfil redonda na barra lateral
    profile_image_path = "src/perfil.jpg"  # Substitua pelo caminho da sua imagem

    # Adicionar CSS para tornar a imagem redonda
    st.sidebar.markdown("""
        <style>
            .profile-pic {
                border-radius: 50%;
                width: 60px;
                height: 60px;
                margin: 10px auto;
            }
        </style>
    """, unsafe_allow_html=True)

    # Exibir a imagem redonda na barra lateral usando HTML
    st.sidebar.image(profile_image_path, use_container_width=False)

    st.title("Gerenciamento de Atendimentos do Ateliê")

    menu = st.sidebar.selectbox("Escolha uma das opções", [
        "Registrar Atendimento",
        "Excluir Atendimento",
        "Cadastrar Serviço",
        "Listar Serviços",
        "Deletar Serviço",
        "Alterar Valor do Serviço",
        "Consultar Resumo",
    ])

    if menu == "Cadastrar Serviço":
        st.header("Cadastrar Serviço")
        nome = st.text_input("Nome do Serviço")
        valor = st.number_input("Valor do Serviço", min_value=0.0, step=0.01)
        if st.button("Cadastrar"):
            try:
                cadastrar_servico(nome, valor)
                st.success(f"Serviço '{nome}' cadastrado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")


    elif menu == "Listar Serviços":
        st.header("Serviços Disponíveis")
        try:
            servicos = listar_servicos()
            if servicos:
                # Ordenar a lista de serviços pelo nome
                servicos_ordenados = sorted(servicos, key=lambda s: s["nome"])
                st.table([{"Nome": s["nome"], "Valor (R$)": f"{s['valor']:.2f}"} for s in servicos_ordenados])
            else:
                st.info("Nenhum serviço cadastrado.")
        except Exception as e:
            st.error(f"Erro ao listar serviços: {e}")


    elif menu == "Registrar Atendimento":

        st.header("Registrar Atendimento")

        try:

            servicos = listar_servicos()

            if servicos:

                # Ordena os serviços em ordem alfabética pelo nome

                servicos_ordenados = sorted(servicos, key=lambda s: s["nome"])

                servico_selecionado = st.selectbox(

                    "Selecione o Serviço",

                    options=[s["nome"] for s in servicos_ordenados]

                )

                # Exibe o valor do serviço selecionado

                valor_servico = next(s["valor"] for s in servicos_ordenados if s["nome"] == servico_selecionado)

                st.write(f"**Valor do Serviço:** R${valor_servico:.2f}")

                data = st.date_input("Data do Atendimento", datetime.now().date())

                if st.button("Registrar"):

                    try:

                        adicionar_atendimento(data.strftime("%Y-%m-%d"), servico_selecionado)

                        st.success("Atendimento registrado com sucesso!")

                    except Exception as e:

                        st.error(f"Erro ao registrar atendimento: {e}")

            else:

                st.warning("Nenhum serviço disponível para registro.")

        except Exception as e:

            st.error(f"Erro ao carregar serviços: {e}")



    elif menu == "Consultar Resumo":

        st.header("Consultar Resumo Mensal")

        # Seleção do mês e ano

        mes = st.selectbox("Mês", options=list(range(1, 13)), format_func=lambda x: f"{x:02}")

        ano = st.number_input("Ano", min_value=2000, max_value=2100, value=datetime.now().year)

        # Inicializa o estado persistente

        if "atendimentos" not in st.session_state:
            st.session_state.atendimentos = []

            st.session_state.total = 0.0

            st.session_state.total_liquido = 0.0

        if st.button("Consultar"):

            try:

                # Consulta os dados e armazena no estado

                atendimentos, total = consultar_resumo(mes, ano)

                st.session_state.atendimentos = atendimentos

                st.session_state.total = total

                st.session_state.total_liquido = total * 0.7

            except Exception as e:

                st.error(f"Erro ao consultar resumo: {e}")

        # Exibe os resultados armazenados no estado

        if st.session_state.atendimentos:

            st.write(f"Resumo Mensal de Atendimentos para {mes:02}/{ano}:")

            # Configurar paginação

            itens_por_pagina = 5

            total_paginas = (len(st.session_state.atendimentos) - 1) // itens_por_pagina + 1

            pagina_atual = st.number_input(

                "Página", min_value=1, max_value=total_paginas, step=1, value=1

            )

            inicio = (pagina_atual - 1) * itens_por_pagina

            fim = inicio + itens_por_pagina

            # Exibir itens da página atual

            for item in st.session_state.atendimentos[inicio:fim]:
                st.write(

                    f"Serviço: {item['nome']} | Quantidade: {item['quantidade']} | Total: R${item['total']:.2f}"

                )

            # Exibir totalizações fora da página

            st.write(f"**Valor total do mês:** R${st.session_state.total:.2f}")

            st.write(f"**Valor líquido (após 30%):** R${st.session_state.total_liquido:.2f}")

            # Exportar PDF

            with st.spinner("Gerando PDF..."):

                pdf_path = gerar_resumo_pdf(

                    st.session_state.atendimentos,

                    st.session_state.total,

                    st.session_state.total_liquido,

                )

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(

                        label="📄 Baixar Resumo em PDF",

                        data=pdf_file,

                        file_name="resumo_mensal.pdf",

                        mime="application/pdf",

                    )

            # Exportar Excel

            with st.spinner("Gerando Excel..."):

                excel_path = gerar_resumo_excel(

                    st.session_state.atendimentos,

                    st.session_state.total,

                    st.session_state.total_liquido,

                )

                with open(excel_path, "rb") as excel_file:
                    st.download_button(

                        label="📊 Baixar Resumo em Excel",

                        data=excel_file,

                        file_name="resumo_mensal.xlsx",

                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                    )

        else:

            st.info(f"Nenhum atendimento encontrado para {mes:02}/{ano}.")



    elif menu == "Deletar Serviço":

        st.header("Deletar Serviço")

        # Listar serviços do Firestore

        servicos = listar_servicos()

        if servicos:

            # Ordenar os serviços em ordem alfabética pelo nome

            servicos_ordenados = sorted(servicos, key=lambda s: s["nome"])

            # Exibir os nomes dos serviços no selectbox

            servico_selecionado = st.selectbox(

                "Selecione o Serviço",

                options=[s["nome"] for s in servicos_ordenados]

            )

            if st.button("Deletar"):

                try:

                    # Encontrar o serviço selecionado na lista de serviços

                    servico_para_deletar = next(

                        s for s in servicos_ordenados if s["nome"] == servico_selecionado

                    )

                    # Passar o ID do serviço para a função de exclusão

                    deletar_servico(servico_para_deletar["id"])

                    st.success(f"Serviço '{servico_selecionado}' deletado com sucesso!")
                    st.rerun()

                except Exception as e:

                    st.error(f"Erro ao deletar serviço: {e}")

        else:

            st.info("Nenhum serviço disponível para deletar.")



    elif menu == "Alterar Valor do Serviço":
        st.header("Alterar Valor do Serviço")

        # Listar serviços do Firestore
        servicos = listar_servicos()

        if servicos:
            # Criar um dicionário com os nomes e IDs dos serviços
            servico_opcoes = {s['nome']: (s['id'], s['valor']) for s in servicos}
            servico_selecionado = st.selectbox("Selecione o Serviço", list(servico_opcoes.keys()))

            # Valor atual do serviço
            valor_atual = servico_opcoes[servico_selecionado][1]
            novo_valor = st.number_input(
                "Novo Valor do Serviço",
                min_value=0.0,
                step=0.01,
                value=valor_atual
            )

            if st.button("Atualizar Valor"):
                try:
                    servico_id = servico_opcoes[servico_selecionado][0]
                    atualizar_valor_servico(servico_id, novo_valor)  # Passar o ID do serviço e o novo valor
                    st.success(f"Valor do serviço '{servico_selecionado}' atualizado para R${novo_valor:.2f}.")
                except Exception as e:
                    st.error(f"Erro ao atualizar o valor: {e}")
        else:
            st.info("Nenhum serviço cadastrado.")






    elif menu == "Excluir Atendimento":

        st.header("Excluir Atendimento")

        # Filtros de data
        data_selecionada = st.date_input("Selecione a Data", value=datetime.now().date())

        # col1, col2, col3 = st.columns(3)
        #
        # with col1:
        #
        #     dia = st.number_input("Dia", min_value=1, max_value=31, step=1, format="%d", value=1)
        #
        # with col2:
        #
        #     mes = st.selectbox("Mês", options=list(range(1, 13)), format_func=lambda x: f"{x:02}")
        #
        # with col3:
        #
        #     ano = st.number_input("Ano", min_value=2000, max_value=2100, step=1, value=datetime.now().year)

        # Consultar atendimentos

        if st.button("Consultar"):
            atendimentos = listar_atendimentos() or []  # Garante que seja uma lista

            atendimentos_filtrados = [

                atendimento for atendimento in atendimentos

                if datetime.strptime(atendimento["data"], "%Y-%m-%d").date() == data_selecionada

            ]

            st.session_state["atendimentos_filtrados"] = atendimentos_filtrados

        # Recuperar atendimentos filtrados do session_state

        atendimentos_filtrados = st.session_state.get("atendimentos_filtrados", [])

        if atendimentos_filtrados:

            atendimento_selecionado = st.selectbox(

                "Selecione o Atendimento para excluir",

                options=atendimentos_filtrados,

                format_func=lambda x: f"Serviço: {x['servico']} | Data: {x['data']}",

                key="atendimento_selecionado"  # Use a chave para rastrear o estado

            )

            if st.button("Excluir Atendimento"):

                try:

                    deletar_atendimento(atendimento_selecionado["id"])  # Exclui o atendimento

                    st.success("Atendimento excluído com sucesso!")

                    # Atualiza a lista de atendimentos

                    atendimentos_filtrados = [

                        atendimento for atendimento in atendimentos_filtrados

                        if atendimento["id"] != atendimento_selecionado["id"]

                    ]

                    st.session_state["atendimentos_filtrados"] = atendimentos_filtrados

                    st.rerun()  # Recarrega a página para refletir a exclusão

                except Exception as e:

                    st.error(f"Erro ao excluir atendimento: {e}")


        else:

            st.info("Nenhum atendimento encontrado para a data especificada.")




    # elif menu == "Excluir Atendimento":
    #     st.header("Excluir Atendimento")
    #     atendimentos = listar_atendimentos()  # Chama a função para listar os atendimentos
    #     if atendimentos:
    #         atendimento_selecionado = st.selectbox(
    #             "Selecione o Atendimento para excluir",
    #             options=atendimentos,
    #             format_func=lambda x: f"Serviço: {x['servico']} | Data: {x['data']}"
    #         )
    #         if st.button("Excluir Atendimento"):
    #             deletar_atendimento(atendimento_selecionado['id'])  # Exclui o atendimento
    #             st.success("Atendimento excluído com sucesso!")
    #     else:
    #         st.info("Nenhum atendimento registrado para excluir.")

  # Adiciona o botão de logout na parte inferior da sidebar
    st.sidebar.markdown("""
        <style>
            .logout-button {
                position: absolute;
                bottom: 10px;
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    # Botão de logout na parte inferior
    if st.sidebar.button("Logout", key="logout", help="Sair da aplicação", use_container_width=True):
        # Limpa a sessão e redireciona para a tela de login
        st.session_state.clear()  # Limpa a sessão
        st.session_state["pagina_atual"] = "login"  # Define a página para "login"
        st.rerun()  # Força o rerun da aplicação após limpar a sessão

# Verifica se o usuário já está autenticado e redireciona para a tela correspondente
if "pagina_atual" in st.session_state and st.session_state["pagina_atual"] == "home":
    # Exibe a página principal após o login
    tela_principal()
else:
    # Exibe a tela de login
    tela_login()


