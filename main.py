import streamlit as st
from db.servicos import cadastrar_servico, listar_servicos, deletar_servico
from db.atendimentos import adicionar_atendimento, listar_atendimentos, deletar_atendimento
from db.servicos import atualizar_valor_servico
#from services.resumo import consultar_resumo
from datetime import datetime
from db.connection import iniciar_supabase
#from services.export import gerar_resumo_pdf, gerar_resumo_excel

supabase = iniciar_supabase()

if supabase is None:
    raise RuntimeError("Cliente Supabase não foi inicializado. Verifique suas credenciais e o arquivo secrets.toml.")

# Operações com o cliente
try:
    response = supabase.from_("servicos").select("*").execute()
    print(response)
except Exception as e:
    print(f"Erro ao acessar a tabela 'servicos': {e}")



st.title("Gerenciamento de Atendimentos do Ateliê")


menu = st.sidebar.selectbox("Escolha uma das opção", [
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
        except Exception as e:
            st.error(f"Erro: {e}")



elif menu == "Listar Serviços":
    st.header("Serviços Disponíveis")

    # Obter a lista de serviços
    try:
        servicos = listar_servicos()
    except Exception as e:
        st.error(f"Erro ao listar serviços: {e}")
        servicos = []

    # Verificar e exibir os serviços
    if servicos:
        st.table([{"Nome": s["nome"], "Valor (R$)": f"{s['valor']:.2f}"} for s in servicos])
    else:
        st.info("Nenhum serviço cadastrado.")

elif menu == "Registrar Atendimento":
    st.header("Registrar Atendimento")
    try:
        servicos = listar_servicos()
        if servicos:
            servico_selecionado = st.selectbox(
                "Selecione o Serviço",
                options=[s["nome"] for s in servicos]
            )
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

# elif menu == "Consultar Resumo":
#     st.header("Consultar Resumo Mensal")
#
#     # Seleção do mês e ano
#     mes = st.selectbox("Mês", options=list(range(1, 13)), format_func=lambda x: f"{x:02}")
#     ano = st.number_input("Ano", min_value=2000, max_value=2100, value=datetime.now().year)
#
#     if st.button("Consultar"):
#         try:
#             # Chama a função para obter os atendimentos
#             atendimentos, total = consultar_resumo(mes, ano)
#             total_liquido = total * 0.7  # Valor líquido após 30% de desconto
#
#             # Verifica se há atendimentos no período
#             if atendimentos:
#                 st.write(f"Resumo Mensal de Atendimentos para {mes:02}/{ano}:")
#                 for item in atendimentos:
#                     st.write(
#                         f"Serviço: {item['nome']} | Quantidade: {item['quantidade']} | Total: R${item['total']:.2f}"
#                     )
#                 st.write(f"**Valor total do mês:** R${total:.2f}")
#                 st.write(f"**Valor líquido (após 30%):** R${total_liquido:.2f}")
#
#                 # Exportar PDF
#                 with st.spinner("Gerando PDF..."):
#                     pdf_path = gerar_resumo_pdf(atendimentos, total, total_liquido)
#                     with open(pdf_path, "rb") as pdf_file:
#                         st.download_button(
#                             label="📄 Baixar Resumo em PDF",
#                             data=pdf_file,
#                             file_name="resumo_mensal.pdf",
#                             mime="application/pdf"
#                         )
#
#                 # Exportar Excel
#                 with st.spinner("Gerando Excel..."):
#                     excel_path = gerar_resumo_excel(atendimentos, total, total_liquido)
#                     with open(excel_path, "rb") as excel_file:
#                         st.download_button(
#                             label="📊 Baixar Resumo em Excel",
#                             data=excel_file,
#                             file_name="resumo_mensal.xlsx",
#                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                         )
#             else:
#                 st.info(f"Nenhum atendimento encontrado para {mes:02}/{ano}.")
#         except Exception as e:
#             st.error(f"Erro ao consultar resumo: {e}")


elif menu == "Deletar Serviço":
    st.header("Deletar Serviço")

    # Listar serviços do Firestore
    servicos = listar_servicos()

    if servicos:
        # Criar um dicionário com os nomes e IDs dos serviços
        servico_opcoes = {s['nome']: s['id'] for s in servicos}
        servico_selecionado = st.selectbox("Selecione o Serviço para Deletar", list(servico_opcoes.keys()))

        if st.button("Deletar"):
            try:
                deletar_servico(servico_opcoes[servico_selecionado])  # Passar o ID do serviço
                st.success(f"Serviço '{servico_selecionado}' deletado com sucesso!")
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
    atendimentos = listar_atendimentos()  # Chama a função para listar os atendimentos
    if atendimentos:
        atendimento_selecionado = st.selectbox(
            "Selecione o Atendimento para excluir",
            options=atendimentos,
            format_func=lambda x: f"Serviço: {x['servico']} | Data: {x['data']}"
        )
        if st.button("Excluir Atendimento"):
            deletar_atendimento(atendimento_selecionado['id'])  # Exclui o atendimento
            st.success("Atendimento excluído com sucesso!")
    else:
        st.info("Nenhum atendimento registrado para excluir.")