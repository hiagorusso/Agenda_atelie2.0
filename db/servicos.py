from db.connection import iniciar_supabase
import streamlit as st

def listar_servicos():
    """Obtém a lista de serviços da tabela 'servicos'."""
    supabase = iniciar_supabase()
    if supabase is None:
        raise RuntimeError("Cliente Supabase não foi inicializado.")

    try:
        # Executa a consulta no Supabase
        response = supabase.from_("servicos").select("*").execute()

        # Verifica se a resposta contém dados
        if response.data:
            return response.data
        else:
            return []  # Retorna uma lista vazia se não houver dados
    except Exception as e:
        raise RuntimeError(f"Erro ao listar serviços: {e}")

# def cadastrar_servico(nome, valor):
#     """Cadastra um novo serviço."""
#     supabase = iniciar_supabase()
#     response = supabase.from_("servicos").insert({"nome": nome, "valor": valor}).execute()
#     if response.error:
#         raise Exception(response.error.message)

def cadastrar_servico(nome, valor):
    """Cadastra um serviço no banco Supabase."""
    supabase = iniciar_supabase()

    if not supabase:
        raise RuntimeError("Cliente Supabase não foi inicializado.")

    try:
        response = supabase.from_("servicos").insert({"nome": nome, "valor": valor}).execute()

        if response.status_code == 201:
            return "Serviço cadastrado com sucesso."
        else:
            raise Exception(f"Erro ao cadastrar serviço: {response.json()}")
    except Exception as e:
        raise Exception(f"Erro ao interagir com o Supabase: {e}")


def atualizar_valor_servico(servico_id, novo_valor):
    """Atualiza o valor de um serviço existente."""
    supabase = iniciar_supabase()
    response = supabase.from_("servicos").update({"valor": novo_valor}).eq("id", servico_id).execute()
    if response.error:
        raise Exception(response.error.message)

def deletar_servico(servico_id):
    """Deleta um serviço."""
    supabase = iniciar_supabase()
    response = supabase.from_("servicos").delete().eq("id", servico_id).execute()
    if response.error:
        raise Exception(response.error.message)

def deletar_atendimento(atendimento_id):
    supabase = iniciar_supabase()
    """Exclui um atendimento do banco de dados com base no ID."""
    try:
        # Executa a exclusão no Supabase
        response = supabase.from_("atendimentos").delete().eq("id", atendimento_id).execute()

        # Verifica se a exclusão foi bem-sucedida
        if response.status_code == 200 and response.data:
            st.success(f"Atendimento com ID {atendimento_id} foi excluído com sucesso.")
        else:
            st.warning(f"Nenhum atendimento encontrado com ID {atendimento_id}.")
    except Exception as e:
        st.error(f"Erro ao excluir atendimento: {e}")