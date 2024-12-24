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

def adicionar_atendimento(data, servico_nome):
    """Adiciona um atendimento à tabela 'atendimentos'."""
    supabase = iniciar_supabase()
    if supabase is None:
        raise RuntimeError("Cliente Supabase não foi inicializado.")

    try:
        # Cria o payload para a inserção
        payload = {
            "data": data,
            "servico": servico_nome,
        }

        # Insere o atendimento no Supabase
        response = supabase.from_("atendimentos").insert(payload).execute()

        # Verifica se a inserção foi bem-sucedida
        if response.data:  # Se a resposta contiver dados, a inserção foi bem-sucedida
            return True
        else:
            raise RuntimeError(f"Erro ao adicionar atendimento: {response.error}")
    except Exception as e:
        raise RuntimeError(f"Erro ao registrar atendimento: {e}")


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