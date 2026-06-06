<div align="center">
  <p align="center">
    <img 
      alt="DIO Education" 
      src="https://raw.githubusercontent.com/digitalinnovationone/template-github-trilha/main/.github/assets/logo.webp" 
      width="100px" 
    />
    <h1>CI&T - Do Prompt ao Agente</h1>
    <h2>Criando um Agente para Automatizar um Fluxo de Trabalho em Python</h2>
  </p>
</div>

<p align="center">
  <img src="https://img.shields.io/static/v1?label=DIO&message=Education&color=E94D5F&labelColor=202024" alt="DIO Project" />
  <a href="NIVEL"><img  src="https://img.shields.io/static/v1?label=Nivel&message=Intermediario&color=E94D5F&labelColor=202024" alt="Nivel"></a>



## 💻 Sobre o Projeto

Construímos um agente planejador de tarefas em Python usando a biblioteca TrelloClient e o google-adk, usando o modelo gemini-2.5-flash. O agente cria tarefas, move as tarefas de lista (a fazer, em andamento, concluído), arquiva e desarquiva tarefas, exclui todo tipo de tarefa (arquivada ou não) e lista as tarefas, tanto as que estão no quadro quanto as que estão arquivadas.

Versão final do agente:

````python
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

````



## ⚙️Pré-requisitos de Ambiente

- Conta ativa no Trello. Tutorial de como criar e configurar a conta [aqui](\agenttaskmanager\readme.md).

- Python 3.7 ou superior instalado.

- pip (gerenciador de pacotes Python).

- Navegador web (ou o VsCode), para testar o agente.

- É esperado que o quadro do Trello tenha este formato, ajuste o código de acordo se não for o caso:

  ![Board esperada no Trello](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\09-boardtrello.png)

## 📚 Pré-requisitos de Habilidades e Níveis de Conhecimento

Antes de ingressar neste conteúdo, é desejável possuir conhecimento prévio nas seguintes áreas:

- Python.

- Comandos básicos de linha de comando (mudar de diretório etc.).

- Uso de arquivos de ambiente (.env).

- Uso de APIs e bibliotecas em Python.

- Engenharia de prompt.

- Conhecimento sobre agentes de inteligência artificial.

- Configuração de ambiente virtual em Python.

- Foi usado o VsCode neste projeto, mas não é obrigatório.


## 🛠️Como foi configurado o ambiente virtual

Depois do ambiente virtual criado na pasta raiz do repositório, instalei as dependências automaticamente na criação do ambiente virtual do VsCode. O comando para instalar as dependências sem depender do instalador automático é:

````bash
pip install -r requirements.txt
````

Depois configurei o adk com o comando:

````bash
adk create agenttaskmanager
````

Foram escolhidas as opções Gemni Flash, Google AI e foi necessário criar uma chave de API gratuita em:

https://aistudio.google.com/api-keys

Foi criado um agente na pasta agenttaskmanager com o arquivo __init__.py, e um arquivo .env com a chave GOOGLE_API_KEY ) que deve estar no arquivo .gitignore) e agent.py

Para testar o agente (selecione a pasta onde o agente está, ou seja, agenttaskmanager) mande um oi:

````
adk web
````

##  🤖Configuração do agente

* Primeiro modifiquei o agent.py para configuração inicial do agente:

![Agente configurado](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\01-agente.png)

* Após as chaves do arquivo .env serem criadas e carregadas no arquivo, foi criada a função *get_temporal_context* para dar o contexto de tempo para o agente e foi criada a função *adicionar_tarefa*, que recebe o nome da tarefa, sua descrição e sua data de término. Ambas as funções foram adicionadas ao parâmetro tools do agente root, que é uma lista. 
* Foi necessário criar a função auxiliar *ajustar_data* para ajustar datas enviadas, devido ao modo como a API do Trello funciona. 
* Depois de testar as funções já implementadas, foi criada a função de listar tarefas, que por padrão lista todas. A função recebe as tarefas do Trello, as grava em uma lista, filtra essa lista por nome (todas, a fazer, em andamento, concluído - se o nome não for válido, a lista fica vazia) e depois converte cada tarefa (card recebido) em uma lista de dicionários que representam as informações da tarefa.

* Por fim, depois de testada essa nova função, foi criada a funcionalidade de mover os cards entre as tarefas (a fazer, em andamento, concluído), *mudar_status_tarefa*. 
* Depois foram implementadas as funções para arquivar e desarquivar uma tarefa: *arquivar_tarefa* e *desarquivar_tarefa*. Uma tarefa é definida como arquivada se o atributo status do card for *True*. Bastou requerer todos os cards, filtrar pela opção desejado (*True* ou *False*, arquivado ou desarquivado) e "inverter" o atributo status do card.
* Por fim, foram criadas funções para remover tarefas (uma específica, todas as arquivadas, ou **todas** elas, arquivadas ou não). São elas: *remover_todas_as_tarefas*, *remover_tarefa* e *remover_todas_as_tarefas_arquivadas*. Para isso foram filtrados os cards de interesse para cada função e usado o método *card.delete()* para os cards a serem apagados.
* Por fim, foram feitos os testes finais do agente, alguns dos quais listados na próxima sessão.



## 🔬Testes

* Teste 1: Perguntar quais minhas tarefas quando o quadro está sem cards. ✅

  ![Teste 1](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\02-teste1.png)

* Teste 2: adicionar algumas tarefas (quadro inicialmente vazio). ✅

![Teste 2](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\03-teste2.png)

![image-20260605190337251](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\03-teste22.png)

* Teste 3: listar tarefas. ✅

![image-20260605190942416](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\04-teste3.png)

* Teste 4: mover alguns cards. ✅

![Teste 4](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\05-teste41.png)

![Teste 4](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\05-teste42.png)

* Teste 5: arquivar tarefas e exibir tarefas arquivadas. ✅

  ![](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\06-teste6.png)

* Teste 6: remover tarefas e desarquivar tarefa. ✅

![Teste 6](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\07-teste61.png)

![Teste 6](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\07-teste62.png)

* Teste 7: arquivar todas as tarefas e remover todas as tarefas arquivadas. ✅

![Teste 8](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\08-teste71.png)

![Teste 7](C:\Users\natan\Desktop\dio\cit\agente-automacao-python\images\08-teste72.png)

## 🎯 Objetivos e Resultados

Após a conclusão do projeto, é demonstrada habilidade em:

- Usar a linguagem Python junto com bibliotecas externas e integrando chaves e parâmetros de configuração via arquivo .env.
- Integrar o Google ADK para criação de agentes de inteligência artificial em conjunto com o consumo de uma API REST via wrapper em Python (biblioteca py-trello).
- Usar, configurar e testar um agente de inteligência artificial.







<p align="center">
  <a href="https://www.dio.me/" target="_blank">
    <img align="center" src="https://raw.githubusercontent.com/digitalinnovationone/template-github-trilha/main/.github/assets/footer.png" alt="banner"/>
  </a>
</p>
