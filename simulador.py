import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pprint import pprint


# ========== PARSE DE ENTRADA ==========
def parse_input(input_path):
    with open(input_path, "r") as input_file:
        lines = input_file.read().strip().split("\n")

    n = int(lines[0])
    processes = []

    for line in lines[1 : n + 1]:
        name, arrival, duration, priority = line.split()
        processes.append(
            {
                "name": name,
                "arrival": int(arrival),
                "duration": int(duration),
                "priority": int(priority),
                "remaining": int(duration),
            }
        )

    quantum = int(lines[-1].split("=")[-1])
    return processes, quantum


# ========== FCFS ==========
def fcfs_scheduler(processes):
    processes.sort(key=lambda x: x["arrival"])
    process_new = []
    start = 0
    for p in processes:
        if p["arrival"] > start:
            start = p["arrival"]
        process_new.append(
            {
                "name": p["name"],
                "start": start,
                "end": start + p["duration"],
            }
        )
        start += p["duration"]
    return process_new


# ========== SJF NÃO PREEMPTIVO ==========
def sjf_non_preemptive_scheduler(processes):
    clock = 0
    ready_queue = []
    completed = []
    processes = sorted(processes, key=lambda x: x["arrival"])
    waiting = processes.copy()

    while waiting or ready_queue:
        ready_queue += [p for p in waiting if p["arrival"] <= clock]
        waiting = [p for p in waiting if p["arrival"] > clock]
        if ready_queue:
            ready_queue.sort(key=lambda x: x["duration"])  # menor duração
            p = ready_queue.pop(0)
            start = max(clock, p["arrival"])
            end = start + p["duration"]
            completed.append({"name": p["name"], "start": start, "end": end})
            clock = end
        else:
            clock += 1
    return completed


# ========== SJF PREEMPTIVO ==========
def sjf_preemptive_scheduler(processes):
    clock = 0
    completed = []
    processes = sorted(processes, key=lambda x: x["arrival"])
    n = len(processes)
    remaining = {p["name"]: p["duration"] for p in processes}
    last_proc = None
    timeline = []

    while any(remaining.values()):
        ready = [
            p for p in processes if p["arrival"] <= clock and remaining[p["name"]] > 0
        ]
        if ready:
            proc = min(ready, key=lambda x: remaining[x["name"]])
            if last_proc != proc["name"]:
                if last_proc is not None:
                    timeline[-1]["end"] = clock
                timeline.append({"name": proc["name"], "start": clock})
                last_proc = proc["name"]
            remaining[proc["name"]] -= 1
        else:
            if last_proc is not None:
                timeline[-1]["end"] = clock
                last_proc = None
            timeline.append({"name": "Idle", "start": clock, "end": clock + 1})
        clock += 1

    if timeline and "end" not in timeline[-1]:
        timeline[-1]["end"] = clock

    return [t for t in timeline if t["name"] != "Idle"]


def plot_gantt_comparativo(gantts_dict, title_prefix, output_file):
    fig, axs = plt.subplots(nrows=3, figsize=(12, 6), sharex=True)
    colors = cm.get_cmap("tab20", 20)

    for i, (algoritmo, gantt) in enumerate(gantts_dict.items()):
        process_names = list({task["name"] for task in gantt})
        process_names.sort()
        name_to_y = {name: i for i, name in enumerate(process_names)}
        name_to_color = {name: colors(j) for j, name in enumerate(process_names)}

        for task in gantt:
            y_pos = name_to_y[task["name"]]
            axs[i].barh(
                y_pos,
                task["end"] - task["start"],
                left=task["start"],
                height=0.5,
                color=name_to_color[task["name"]],
            )
        axs[i].set_yticks(list(name_to_y.values()))
        axs[i].set_yticklabels(list(name_to_y.keys()))
        axs[i].set_ylabel(algoritmo)
        axs[i].grid(True, axis="x", linestyle="--", alpha=0.3)

    max_time = max(task["end"] for gantt in gantts_dict.values() for task in gantt)
    axs[-1].set_xticks(range(0, max_time + 1))
    axs[-1].set_xlabel("Tempo")
    fig.suptitle(f"{title_prefix} - Comparativo de Algoritmos", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_file)
    plt.close()


# ========== EXECUÇÃO ==========
def executar_todos(input_dir="entradas", output_dir="resultados"):
    os.makedirs(output_dir, exist_ok=True)
    arquivos = sorted([f for f in os.listdir(input_dir) if f.endswith(".txt")])

    for arquivo in arquivos:
        entrada_path = os.path.join(input_dir, arquivo)
        nome_base = os.path.splitext(arquivo)[0]
        processos, quantum = parse_input(entrada_path)
        print(f"\nArquivo: {arquivo} | Quantum: {quantum}")

        gantts_dict = {
            "FCFS": fcfs_scheduler([p.copy() for p in processos]),
            "SJF Não Preemptivo": sjf_non_preemptive_scheduler(
                [p.copy() for p in processos]
            ),
            "SJF Preemptivo": sjf_preemptive_scheduler([p.copy() for p in processos]),
        }

        saida = os.path.join(output_dir, f"{nome_base}_comparativo.png")
        plot_gantt_comparativo(gantts_dict, nome_base.upper(), saida)
        print(f"  → Gráfico comparativo salvo em: {saida}")


if __name__ == "__main__":
    executar_todos()
