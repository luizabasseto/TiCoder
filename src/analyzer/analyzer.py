import json

def analisar_metricas(caminho_arquivo, ks=(1, 5), max_m=5):
    with open(caminho_arquivo, "r") as f:
        data = [d for d in json.load(f) if d is not None]

    resultados = {
        k: {
            m: {"total": 0, "hits": 0}
            for m in range(1, max_m + 1)
        }
        for k in ks
    }

    for item in data:
        for iteracao in item["results"]:
            m = iteracao["num_queries"]

            if m > max_m:
                continue

            status = iteracao["status"]

            for k in ks:
                resultados[k][m]["total"] += 1

                if any(status[:k]):
                    resultados[k][m]["hits"] += 1

    print("| Métrica | m | Valor |")
    print("|:-------|:-:|------:|")

    for k in ks:
        for m in range(1, max_m + 1):
            total = resultados[k][m]["total"]

            if total == 0:
                continue

            valor = resultados[k][m]["hits"] / total * 100

            print(f"| pass@{k}@{m} | {m} | {valor:.2f}% |")


analisar_metricas("../results/global_results.teste_parcial_humanEval.json")