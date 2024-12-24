from db.connection import iniciar_supabase

def listar_atendimentos():
    """Lista todos os atendimentos registrados."""
    supabase = iniciar_supabase()
    response = supabase.from_("atendimentos").select("*").execute()
    if response.error:
        raise Exception(response.error.message)
    return response.data

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
    """Deleta um atendimento pelo ID."""
    supabase = iniciar_supabase()
    response = supabase.from_("atendimentos").delete().eq("id", atendimento_id).execute()
    if response.error:
        raise Exception(response.error.message)