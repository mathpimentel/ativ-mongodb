from pymongo import MongoClient
from conexao import colecao_tarefas
from datetime import datetime 

def criar_tarefa():
    titulo = input('Digite o título da tarefa: ')
    descricao = input('Digite a descrição da tarefa: ')
    data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M")
    opcoes_status = ['pendente', 'em andamento', 'concluída']
    tags = []
    comentarios = []
    while True:
        status = input('Digite o status da tarefa (pendente, em andamento, concluída): ').lower()
        if status in opcoes_status:
            break
        else:
            print('Status inválido. Digite um status valido.')
    
    add_tag = input('Deseja adicionar uma tag? (Sim ou Não): ').lower()
    if add_tag == "sim":
        while True:
            tag = input('Digite o nome da tag: ')
            tags.append(tag)
            op = input('Digite adicionar mais uma tag? (Sim ou não): ').lower()
            if op != "sim":
                break

    colecao_tarefas.insert_one({
        'titulo': titulo,
        'descricao': descricao,
        'data_criacao': data_criacao,
        'status': status,
        'tags': tags,
        'comentarios': comentarios
    })
    print('Tarefa criada com sucesso!')

def exibir_todas_tarefas(lista_tarefas):
    for i, tarefa in enumerate(lista_tarefas, start=1):
        print(f"Tarefa {i}:")  
        print(f"-  Título: {tarefa['titulo']}")
        print('-' * 15)

def detalhes_tarefa(tarefa):
    print("-" * 20)
    print(f"-  Título: {tarefa['titulo']}")
    print(f"-  Descrição: {tarefa['descricao']}")  
    print(f"-  Data de criação: {tarefa['data_criacao']}")
    print(f"-  Status: {tarefa['status']}") 
    print(f"-  Tags: {tarefa['tags']}")
    print(f"-  Comentários: {tarefa['comentarios']}") 
    print("-" * 20)

def ler_tarefas(): 
    lista_tarefas = list(colecao_tarefas.find())
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    exibir_todas_tarefas(lista_tarefas)    
    opcao = int(input('\nEscolha o n° da tarefa que deseja visualizar: '))

    if opcao <= len(lista_tarefas):
        tarefa = lista_tarefas[opcao - 1]
        detalhes_tarefa(tarefa)
    else:
        print('Tarefa não encontrada.')

def atualizar_tarefa():
    lista_tarefas = list(colecao_tarefas.find())
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    
    exibir_todas_tarefas(lista_tarefas)
    opcao = int(input('\nEscolha o n° da tarefa que deseja atualizar: '))

    if opcao < 1 or opcao > len(lista_tarefas):
        print("Não existe essa tarefa.")
        return
    
    else:
        while True:
            print('-' * 25)
            print("\nO que deseja atualizar?")
            print("1 - Editar título")
            print("2 - Editar descrição")
            print("3 - Alterar status")
            print("4 - Adicionar tag")
            print("5 - Sair")
        
            escolha = int(input("Escolha uma opção: "))
            if escolha == 1:
                print('-' * 25)
                novo_titulo = input("Digite o novo título: ")
                colecao_tarefas.update_one({"_id": lista_tarefas[opcao - 1]["_id"]}, {"$set": {"titulo": novo_titulo}})
                print("Título atualizado com sucesso!")
                print('-' * 25)

            elif escolha == 2:
                print('-' * 25)
                nova_descricao = input("Digite a nova descrição: ")
                colecao_tarefas.update_one({"_id": lista_tarefas[opcao - 1]["_id"]}, {"$set": {"descricao": nova_descricao}})
                print("Descrição atualizada com sucesso!")
                print('-' * 25)

            elif escolha == 3:
                print('-' * 25)
                novo_status = input("Digite o novo status (pendente, em andamento, concluída): ")
                colecao_tarefas.update_one({"_id": lista_tarefas[opcao - 1]["_id"]}, {"$set": {"status": novo_status}})
                print("Status atualizado com sucesso!")
                print('-' * 25)

            elif escolha == 4:
                tarefa = lista_tarefas[opcao - 1]
                tags = tarefa.get("tags", [])
                if not tags:
                    print("Essa tarefa não possui tags")
                    add = input("Deseja adicionar uma nova tag? (sim/não): ").strip().lower()
                    if add == "sim":
                        tag_nova = input("Digite a nova tag: ")
                        colecao_tarefas.update_one({"_id": tarefa["_id"]}, {"$addToSet": {"tags":tag_nova}})
                        print("Tag adicionada com sucesso")
                    return

                print("Tags atuais: ")
                for i, tag in enumerate(tags, start=1):
                    print(f"{i} - {tag}")

                i = int(input("Digite o número da tag que deseja atualizar: ")) - 1
                if i < 0 or i >= len(tags):
                    print("Tag inválida.")
                    return
                
                tag_antiga = tags[i]
                tag_nova = input("Digite a nova tag: ")
                colecao_tarefas.update_one({"_id": tarefa["_id"]},{
                "$pull": {"tags": tag_antiga},
                "$addToSet": {"tags": tag_nova}}
                )
                print("Tag adicionada com sucesso!")
                print('-' * 25)

            elif escolha == 5:
                break
            else:
                print("Opção inválida. Tente novamente.")

def deletar_tarefa():
    lista_tarefas = list(colecao_tarefas.find())
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    exibir_todas_tarefas(lista_tarefas)
    opcao = int(input('Escolha o n° da tarefa que deseja deletar: ')) 

    if opcao < 0 or opcao >= len(lista_tarefas):
        print("Não existe essa tarefa.")        
        return  
    else:
        colecao_tarefas.delete_one({"_id": lista_tarefas[opcao - 1]["_id"]})
        print("Tarefa deletada com sucesso!")

def busca_especifica():
    tipo = int(input('\nEscolha uma opção:\n1 - Buscar tarefa por status\n2 - Buscar tarefa por data de criação (AAAA-MM-DD)\n3 - Buscar tarefa por tag\n4 - Sair\n'))
    filtro = None

    if tipo == 4:
        return

    if tipo == 1:
        campo = "status"
        valor = input('Digite o status que deseja buscar (pendente, em andamento, concluída): ')
        filtro = {campo: valor}

    elif tipo == 2:
        campo = "data_criacao"
        valor = input('Digite a data (AAAA-MM-DD): ')
        try:
            data_inicio = datetime.strptime(valor, "%Y-%m-%d")
            data_fim = data_inicio.replace(hour=23, minute=59, second=59)
            filtro = {campo: {"$gte": data_inicio, "$lte": data_fim}}
        except ValueError:
            print("Formato de data inválido. Use AAAA-MM-DD.")
            return

    elif tipo == 3:
        campo = "tags"
        valor = input('Digite a tag que deseja buscar: ')
        filtro = {campo: {"$in": [valor]}}

    else:
        print("Opção inválida.")
        return

    tarefas_encontradas = list(colecao_tarefas.find(filtro))
    
    if tarefas_encontradas:
        for tarefa in tarefas_encontradas:
            detalhes_tarefa(tarefa)
    else:
        print("Nenhuma tarefa encontrada.")

def adicionar_comentario():
    lista_tarefas = list(colecao_tarefas.find())
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    exibir_todas_tarefas(lista_tarefas)
    opcao = int(input('Escolha o n° da tarefa que deseja adicionar um comentário: '))

    if opcao < 1 or opcao > len(lista_tarefas):
        print("Não existe essa tarefa.")        
        return  
    else:
        autor = input('Digite o seu nome: ')
        while True:
            comentario = input('Digite o comentário: ')
            data = datetime.now().strftime("%Y-%m-%d %H:%M")
            c = {
                "autor" : autor,
                "comentario": comentario,
                "data":data
                }
            colecao_tarefas.update_one({"_id": lista_tarefas[opcao - 1]["_id"]}, {"$push": {"comentarios": c}})
            
            print("Comentário adicionado com sucesso!")
            op = input('Deseja adicionar um novo comentário? (Sim ou Não): ').strip().lower()
            if op != "sim":
                break
