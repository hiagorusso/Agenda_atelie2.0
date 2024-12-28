from db.connection import iniciar_supabase
import streamlit as st

def listar_atendimentos():
    """Lista os atendimentos registrados no banco de dados."""
    supabase = iniciar_supabase()

    if not supabase:
        raise RuntimeError("Cliente Supabase não foi inicializado.")

    try:
        # Recupera todos os atendimentos da tabela "atendimentos"
        response = supabase.from_("atendimentos").select("*").execute()

        # Debugando a resposta completa
        print("Resposta completa:", response)

        # Verifique se há dados na resposta
        if response.data:
            return response.data
        else:
            raise Exception("Nenhum atendimento encontrado ou erro ao consultar os atendimentos.")

    except Exception as e:
        print(f"Erro ao listar atendimentos: {e}")
        return None

# def adicionar_atendimento(data, servico_nome):
#     """Adiciona um atendimento à tabela 'atendimentos'."""
#     supabase = iniciar_supabase()
#     if supabase is None:
#         raise RuntimeError("Cliente Supabase não foi inicializado.")
#
#     try:
#         # Cria o payload para a inserção
#         payload = {
#             "data": data,
#             "servico": servico_nome,
#         }
#
#         # Insere o atendimento no Supabase
#         response = supabase.from_("atendimentos").insert(payload).execute()
#
#         # Verifica se a inserção foi bem-sucedida
#         if response.data:  # Se a resposta contiver dados, a inserção foi bem-sucedida
#             return True
#         else:
#             raise RuntimeError(f"Erro ao adicionar atendimento: {response.error}")
#     except Exception as e:
#         raise RuntimeError(f"Erro ao registrar atendimento: {e}")
def adicionar_atendimento(data, servico_nome):
    """Cadastra um atendimento no banco de dados com base no nome do serviço."""
    supabase = iniciar_supabase()

    try:
        # Buscar o serviço pelo nome para obter o ID
        servico = supabase.from_("servicos").select("id, nome").eq("nome", servico_nome).execute()

        if not servico.data:
            raise Exception("Serviço não encontrado.")

        servico_id = servico.data[0]["id"]

        # Inserir o atendimento com o ID e nome do serviço
        response = supabase.from_("atendimentos").insert({
            "data": data,
            "servico_id": servico_id,
            "servico": servico_nome
        }).execute()

        # Verifica se a resposta tem dados (usa .data para acessar)
        if response.data:
            return "Atendimento cadastrado com sucesso."
        else:
            # Verifica se há mensagem de erro na resposta
            error_message = response.error.message if response.error else "Erro desconhecido"
            raise Exception(f"Erro ao cadastrar atendimento: {error_message}")

    except Exception as e:
        raise Exception(f"Erro ao interagir com o Supabase: {e}")


def deletar_atendimento(atendimento_id):
    supabase = iniciar_supabase()
    """Exclui um atendimento do banco de dados com base no ID."""
    try:
        # Executa a exclusão no Supabase
        response = supabase.from_("atendimentos").delete().eq("id", atendimento_id).execute()

        # Verifique se a exclusão foi bem-sucedida
        if response.data:  # Verifica se há dados na resposta, indicando que a exclusão foi bem-sucedida
            st.success(f"Atendimento com ID {atendimento_id} foi excluído com sucesso.")
        else:
            st.warning(f"Nenhum atendimento encontrado com ID {atendimento_id}.")
    except Exception as e:
        st.error(f"Erro ao excluir atendimento: {e}")