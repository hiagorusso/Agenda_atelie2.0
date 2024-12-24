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

def cadastrar_servico(nome, valor):
    """Cadastra um serviço no banco Supabase."""
    supabase = iniciar_supabase()

    if not supabase:
        raise RuntimeError("Cliente Supabase não foi inicializado.")

    try:
        # Realiza a inserção
        response = supabase.from_("servicos").insert({"nome": nome, "valor": valor}).execute()

        # Verifica se a resposta contém dados ou um erro
        if response.data:
            return "Serviço cadastrado com sucesso."
        elif response.error:
            raise Exception(f"Erro ao cadastrar serviço: {response.error}")
        else:
            raise Exception("Erro desconhecido ao cadastrar serviço.")
    except Exception as e:
        raise Exception(f"Erro ao interagir com o Supabase: {e}")


def atualizar_valor_servico(servico_id, novo_valor):
    """Atualiza o valor de um serviço existente."""
    supabase = iniciar_supabase()

    if not supabase:
        raise RuntimeError("Cliente Supabase não foi inicializado.")

    try:
        # Realizando a atualização no banco de dados
        response = supabase.from_("servicos").update({"valor": novo_valor}).eq("id", servico_id).execute()

        # Verificando se a resposta contém dados (se a atualização foi bem-sucedida)
        if response.data:
            return f"Valor do serviço atualizado para R${novo_valor:.2f}."

        # Caso não tenha dados, verifica se houve erro na resposta
        if response.error:
            raise Exception(f"Erro ao atualizar o valor do serviço: {response.error.message}")

        # Caso nenhum dado ou erro seja encontrado
        raise Exception("Erro inesperado ao atualizar o valor do serviço.")

    except Exception as e:
        raise Exception(f"Erro ao interagir com o Supabase: {e}")


def deletar_servico(servico_id):
    """Deleta um serviço."""
    supabase = iniciar_supabase()

    if not supabase:
        raise RuntimeError("Cliente Supabase não foi inicializado.")

    try:
        response = supabase.from_("servicos").delete().eq("id", servico_id).execute()

        # Verifique se a resposta contém dados (se o serviço foi deletado com sucesso)
        if response.data:
            return "Serviço deletado com sucesso."

        # Caso não tenha dados, tente capturar o erro
        if response.error:
            raise Exception(f"Erro ao deletar serviço: {response.error}")

        # Caso nenhum erro ou dados sejam encontrados
        raise Exception("Erro inesperado ao deletar o serviço.")

    except Exception as e:
        raise Exception(f"Erro ao interagir com o Supabase: {e}")

