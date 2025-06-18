# simulador_p2.py

import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm


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


# ========== ROUND ROBIN ==========
def round_robin_scheduler(processes, quantum):
    clock = 0
    queue = []
    timeline = []
    processes = sorted(processes, key=lambda p: p["arrival"])
    waiting = processes.copy()

    while waiting or queue:
        queue += [p for p in waiting if p["arrival"] <= clock]
        waiting = [p for p in waiting if p["arrival"] > clock]

        if queue:
            p = queue.pop(0)
            slice_time = min(p["remaining"], quantum)
            timeline.append(
                {"name": p["name"], "start": clock, "end": clock + slice_time}
            )
            clock += slice_time
            p["remaining"] -= slice_time
            if p["remaining"] > 0:
                queue += [p for p in waiting if p["arrival"] <= clock]
                waiting = [p for p in waiting if p["arrival"] > clock]
                queue.append(p)
        else:
            clock += 1

    return timeline


# ========== PRIORITY ROUND ROBIN ==========
def priority_rr_scheduler(processes, quantum):
    clock = 0
    queue = []
    timeline = []
    processes = sorted(processes, key=lambda p: p["arrival"])
    waiting = processes.copy()

    while waiting or queue:
        queue += [p for p in waiting if p["arrival"] <= clock]
        waiting = [p for p in waiting if p["arrival"] > clock]

        if queue:
            queue.sort(key=lambda p: p["priority"])
            current_priority = queue[0]["priority"]
            same_priority = [p for p in queue if p["priority"] == current_priority]
            p = same_priority.pop(0)
            queue.remove(p)

            slice_time = min(p["remaining"], quantum)
            timeline.append(
                {"name": p["name"], "start": clock, "end": clock + slice_time}
            )
            clock += slice_time
            p["remaining"] -= slice_time

            queue += [proc for proc in waiting if proc["arrival"] <= clock]
            waiting = [proc for proc in waiting if proc["arrival"] > clock]

            if p["remaining"] > 0:
                queue.append(p)
        else:
            clock += 1

    return timeline


# ========== MULTILEVEL QUEUE ==========
def multilevel_queue_scheduler(processes):
    clock = 0
    queue = []
    timeline = []
    processes = sorted(processes, key=lambda p: p["arrival"])
    waiting = processes.copy()
    quantum_map = {}  # nome → quantum (1, 2, 4, 8...)

    while waiting or queue:
        queue += [p for p in waiting if p["arrival"] <= clock]
        waiting = [p for p in waiting if p["arrival"] > clock]

        if queue:
            p = queue.pop(0)
            if p["name"] not in quantum_map:
                quantum_map[p["name"]] = 1

            qt = quantum_map[p["name"]]
            slice_time = min(p["remaining"], qt)
            timeline.append(
                {"name": p["name"], "start": clock, "end": clock + slice_time}
            )
            clock += slice_time
            p["remaining"] -= slice_time

            queue += [proc for proc in waiting if proc["arrival"] <= clock]
            waiting = [proc for proc in waiting if proc["arrival"] > clock]

            if p["remaining"] > 0:
                quantum_map[p["name"]] *= 2
                queue.append(p)
        else:
            clock += 1

    return timeline


# ========== GANTT ==========
def plot_gantt_comparativo(gantts_dict, title_prefix, output_file):
    fig, axs = plt.subplots(nrows=3, figsize=(12, 6), sharex=True)
    colors = cm.get_cmap("tab20", 20)

    for i, (algoritmo, gantt) in enumerate(gantts_dict.items()):
        process_names = sorted(set(t["name"] for t in gantt))
        name_to_y = {name: j for j, name in enumerate(process_names)}
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
        axs[i].set_yticklabels(process_names)
        axs[i].set_ylabel(algoritmo)
        axs[i].grid(True, axis="x", linestyle="--", alpha=0.3)

    max_time = max(t["end"] for gantt in gantts_dict.values() for t in gantt)
    axs[-1].set_xticks(range(0, max_time + 1))
    axs[-1].set_xlabel("Tempo")
    fig.suptitle(f"{title_prefix} - Algoritmos da Parte 2", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_file)
    plt.close()


# ========== EXECUÇÃO ==========
def executar_todos(input_dir="entradas", output_dir="resultados"):
    os.makedirs(output_dir, exist_ok=True)
    arquivos = sorted(f for f in os.listdir(input_dir) if f.endswith(".txt"))

    for arquivo in arquivos:
        entrada_path = os.path.join(input_dir, arquivo)
        nome_base = os.path.splitext(arquivo)[0]
        processos, quantum = parse_input(entrada_path)

        gantts_dict = {
            "Round-Robin": round_robin_scheduler(
                [p.copy() for p in processos], quantum
            ),
            "Prioridade + RR": priority_rr_scheduler(
                [p.copy() for p in processos], quantum
            ),
            "Multilevel Queue": multilevel_queue_scheduler(
                [p.copy() for p in processos]
            ),
        }

        output_path = os.path.join(output_dir, f"{nome_base}_comparativo_p2.png")
        plot_gantt_comparativo(gantts_dict, nome_base.upper(), output_path)
        print(f"→ Gráfico gerado: {output_path}")


if __name__ == "__main__":
    executar_todos()
