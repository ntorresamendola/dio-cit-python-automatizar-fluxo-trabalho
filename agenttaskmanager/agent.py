from google.adk.agents.llm_agent import Agent
from trello import TrelloClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

# Suas credenciais
API_KEY = os.getenv("TRELLO_API_KEY")
API_SECRET = os.getenv("TRELLO_API_SECRET")
TOKEN = os.getenv("TRELLO_TOKEN")

# funções auxiliares para o agente de organização de tarefas


def ajustar_data(data: str, valor: int) -> str:
    """ajusta a data adicionando ou removendo dias
    Args:
        data (str): data no formato "YYYY/MM/DD" ou ISO 8601
        valor (int): número de dias a adicionar (positivo) ou remover (negativo)

    Returns:
        str: data ajustada no formato "YYYY-MM-DD"
    """
    nova_data = data.replace("/", "-")  # Ajusta o formato para ISO 8601
    nova_data = datetime.fromisoformat(nova_data) + timedelta(days=valor)
    return datetime.strftime(nova_data, "%Y-%m-%d")


# cria o contexto de data para o agente
def get_temporal_context():
    """Gera o contexto temporal atual no formato "YYYY/MM/DD HH:MM:SS"."""

    now = datetime.now()
    return now.strftime("%Y/%m/%d %H:%M:%S")


def adicionar_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str):
    """Adiciona uma tarefa como um card no Trello. Recebe o nome da tarefa, descrição e data de vencimento.
    Args:
        nome_da_task (str): O nome da tarefa a ser adicionada.
        descricao_da_task (str): A descrição da tarefa a ser adicionada.
        due_date (str): A data de vencimento da tarefa no formato "YYYY/MM/DD".
    """

    # conectar ao Trello usando as credenciais, listar os boards, encontrar o board "Dio"
    client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)
    client.list_boards()
    # Para obter o board (você precisa do ID ou nome do board)
    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == "Dio"][0]

    # Obter a lista onde quer adicionar o card, ou seja, a fazer
    listas = meu_board.list_lists()
    minha_lista = [
        l for l in listas if l.name.upper() == "TO DO" or l.name.upper() == "A FAZER"
    ][0]

    # Criar o card (task)
    minha_lista.add_card(
        name=nome_da_task, desc=descricao_da_task, due=ajustar_data(due_date, 1)
    )


def listar_tarefas(status: str = "todas"):
    client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == "Dio"][0]
    listas = meu_board.list_lists()

    if status.lower() == "todas":
        listas_filtradas = listas
    elif status.lower() == "a fazer":
        listas_filtradas = [
            l for l in listas if l.name.upper() in ["A FAZER", "TO DO", "TODO"]
        ]
    elif status.lower() == "em andamento":
        listas_filtradas = [
            l for l in listas if l.name.upper() in ["EM ANDAMENTO", "DOING"]
        ]
    elif status.lower() == "concluido":
        listas_filtradas = [
            l for l in listas if l.name.upper() in ["CONCLUÍDO", "CONCLUIDO", "DONE"]
        ]
    else:
        listas_filtradas = []

    tarefas = []

    for lista in listas_filtradas:
        cards = lista.list_cards()
        for card in cards:
            tarefas.append(
                {
                    "nome": card.name,
                    "descricao": card.desc,
                    "vencimento": ajustar_data(card.due, -1),
                    "status": lista.name,
                    "id": card.id,
                }
            )

    return tarefas


def mudar_status_tarefa(nome_da_task: str, novo_status: str) -> str:
    try:
        client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)

        boards = client.list_boards()
        meu_board = [b for b in boards if b.name == "Dio"][0]
        listas = meu_board.list_lists()

        # Mapear status para listas
        status_map = {
            "a fazer": "A FAZER",
            "em andamento": "EM ANDAMENTO",
            "concluido": "CONCLUÍDO",
        }

        nome_lista_destino = status_map.get(novo_status.lower())

        if not nome_lista_destino:
            return f"❌ Status inválido. Use: 'a fazer', 'em andamento' ou 'concluido'"

        # Encontrar lista de destino
        lista_destino = next(
            (l for l in listas if l.name.upper() == nome_lista_destino.upper()), None
        )

        if not lista_destino:
            return f"❌ Lista '{nome_lista_destino}' não encontrada no board"

        # Buscar card em todas as listas
        card_encontrado = None
        lista_origem = None

        for lista in listas:
            cards = lista.list_cards()
            card_encontrado = next(
                (c for c in cards if c.name.lower() == nome_da_task.lower()), None
            )
            if card_encontrado:
                lista_origem = lista
                break

        if not card_encontrado:
            return f"❌ Card '{nome_da_task}' não encontrado"

        # Mover
        card_encontrado.change_list(lista_destino.id)
        return f"✅ '{nome_da_task}': {lista_origem.name} → {lista_destino.name}"  # type: ignore
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def arquivar_tarefa(nome_da_task: str) -> str:
    try:
        client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)

        boards = client.list_boards()
        meu_board = [b for b in boards if b.name == "Dio"][0]
        listas = meu_board.list_lists()

        # Buscar card em todas as listas
        card_encontrado = None
        for card in meu_board.all_cards():
            if card.name.lower() == nome_da_task.lower():
                card_encontrado = card
                break
        if card_encontrado:
            card_encontrado.set_closed(True)
            return f"✅ Card '{nome_da_task}' arquivado com sucesso"
        else:
            return f"❌ Card '{nome_da_task}' não encontrado"
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def desarquivar_tarefa(nome_da_task: str) -> str:
    try:
        client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)

        boards = client.list_boards()
        meu_board = [b for b in boards if b.name == "Dio"][0]

        # Buscar card arquivado em todas as listas
        card_encontrado = None
        for card in meu_board.all_cards():
            if card.name.lower() == nome_da_task.lower() and card.closed:
                card_encontrado = card
                break
        if card_encontrado:
            card_encontrado.set_closed(False)
            return f"✅ Card '{nome_da_task}' desarquivado com sucesso"
        else:
            return f"❌ Card '{nome_da_task}' arquivado não encontrado"
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def listar_tarefas_arquivadas():
    client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == "Dio"][0]
    archived_cards = meu_board.get_cards(card_filter="closed")

    tarefas = []
    for card in archived_cards:
        tarefas.append(
            {
                "nome": card.name,
                "descricao": card.desc,
                "vencimento": ajustar_data(card.due, -1),
                "status": "ARQUIVADO",
                "id": card.id,
            }
        )
    return tarefas


def remover_todas_as_tarefas_arquivadas():
    client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == "Dio"][0]
    archived_cards = meu_board.get_cards(card_filter="closed")

    for card in archived_cards:
        card.delete()  # Excluir o card arquivado


def remover_tarefa(nome_da_task: str) -> str:
    try:
        client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)

        boards = client.list_boards()
        meu_board = [b for b in boards if b.name == "Dio"][0]

        # Buscar card em todas as listas
        card_encontrado = None
        for card in meu_board.all_cards():
            if card.name.lower() == nome_da_task.lower():
                card_encontrado = card
                break
        if card_encontrado:
            card_encontrado.delete()
            return f"✅ Card '{nome_da_task}' removido com sucesso"
        else:
            return f"❌ Card '{nome_da_task}' não encontrado"
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def remover_todas_as_tarefas():
    client = TrelloClient(api_key=API_KEY, api_secret=API_SECRET, token=TOKEN)

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == "Dio"][0]
    all_cards = meu_board.all_cards()

    for card in all_cards:
        card.delete()  # Excluir o card


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Agente de organização de tarefas.",
    instruction="""
        Você é um agente de organização de tarefas.     
        Sua função é receber uma tarefa e criar um card no Trello com o nome e descrição da tarefa.
        Você deve me perguntar as atividas que tenho no dia e criar um card para cada uma delas.
        Você inicia a conversa assim que for ativado, perguntando quais são as tarefas do dia.
        Sempre inicie a conversa perguntando quais são as tarefas do dia informando a data pela tool get_temporal_context, 
        e depois vá perguntando se tem mais alguma tarefa, até que o usuário diga que não tem mais tarefas.
        Suas funções:
         1. Adicionar novas tarefas com nome e descrição
          2. Listar todas as tarefas ou filtrar por status
          3. Marcar tarefas como concluídas
          4. Remover tarefas da lista
          5. Mudar o status da tarefa (ex: de "A Fazer" para "Em Andamento" e de "Em Andamento" para "Concluído")
          6. Gerar contexto temporal (data e hora atual) para organizar as tarefas do dia  
          7. Arquivar e desarquivar tarefas
          8. Listar tarefas arquivadas
          9. Excluir tarefas
    """,
    tools=[
        get_temporal_context,
        adicionar_tarefa,
        listar_tarefas,
        mudar_status_tarefa,
        arquivar_tarefa,
        desarquivar_tarefa,
        remover_tarefa,
        listar_tarefas_arquivadas,
        remover_todas_as_tarefas_arquivadas,
        remover_todas_as_tarefas,
    ],
)
