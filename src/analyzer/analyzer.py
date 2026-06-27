import json

ARQUIVO_JSON = '../results/global_results.teste_parcial_mbpp.json'

def analisar_resultados(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        dados = json.load(f)

    total_tentativas = len(dados)
    dados_validos = [d for d in dados if d is not None]
    total_validos = len(dados_validos)

    print(f"--- Relatório de Execução ---")
    print(f"Total de instâncias lidas: {total_tentativas}")
    print(f"Instâncias processadas com sucesso (sem nulls): {total_validos} ({total_validos/total_tentativas*100:.1f}%)")
    
    if total_validos == 0:
        return

    top1_hits_por_query = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    any_hits_por_query = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    total_por_query = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for item in dados_validos:
        for iteracao in item['results']:
            q = iteracao['num_queries']
            status_array = iteracao['status']
            
            if q in total_por_query:
                total_por_query[q] += 1
                
                if len(status_array) > 0:
                    if status_array[0] == True:
                        top1_hits_por_query[q] += 1
                    
                    if True in status_array:
                        any_hits_por_query[q] += 1

    print("\n--- Resultados de Acurácia ---")
    for q in [1, 2, 3,4, 5]:
        if total_por_query[q] > 0:
            taxa_top1 = (top1_hits_por_query[q] / total_por_query[q]) * 100
            taxa_any = (any_hits_por_query[q] / total_por_query[q]) * 100
            print(f"Após {q} interação(ões):")
            print(f"  -> Acurácia Top-1: {taxa_top1:.2f}% ({top1_hits_por_query[q]}/{total_por_query[q]})")
            print(f"  -> Pelo menos um correto (Any): {taxa_any:.2f}% ({any_hits_por_query[q]}/{total_por_query[q]})")

analisar_resultados(ARQUIVO_JSON)