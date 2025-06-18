import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def parse_input(input_path):
    with open(input_path) as f:
        lines = f.read().strip().splitlines()
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


def round_robin_scheduler(processes, quantum):
    clock = 0
    queue = []
    timeline = []
    processes = sorted(processes, key=lambda p: p["arrival"])
    waiting = [p.copy() for p in processes]
    while waiting or queue:
        queue += [p for p in waiting if p["arrival"] <= clock]
        waiting = [p for p in waiting if p["arrival"] > clock]
        if queue:
            p = queue.pop(0)
            t = min(p["remaining"], quantum)
            timeline.append({"name": p["name"], "start": clock, "end": clock + t})
            clock += t
            p["remaining"] -= t
            queue += [p for p in waiting if p["arrival"] <= clock]
            waiting = [p for p in waiting if p["arrival"] > clock]
            if p["remaining"] > 0:
                queue.append(p)
        else:
            clock += 1
    return timeline


def priority_rr_scheduler(processes, quantum):
    clock = 0
    waiting = sorted([p.copy() for p in processes], key=lambda p: p["arrival"])
    queue = []
    timeline = []
    while waiting or queue:
        while waiting and waiting[0]["arrival"] <= clock:
            queue.append(waiting.pop(0))
        if queue:
            ready = sorted(queue, key=lambda p: p["priority"], reverse=True)
            p = ready[0]
            queue.remove(p)
            future = [q["arrival"] for q in waiting if q["priority"] > p["priority"]]
            t_int = min(future) if future else None
            is_unique = all(q["priority"] < p["priority"] for q in queue)
            if t_int is not None and t_int > clock and t_int - clock < quantum:
                t = t_int - clock
            else:
                if t_int is None and is_unique:
                    t = p["remaining"]
                else:
                    t = min(quantum, p["remaining"])
            timeline.append({"name": p["name"], "start": clock, "end": clock + t})
            clock += t
            p["remaining"] -= t
            while waiting and waiting[0]["arrival"] <= clock:
                queue.append(waiting.pop(0))
            if p["remaining"] > 0:
                queue.append(p)
        else:
            clock += 1
    return timeline


def multilevel_queue_scheduler(processes):
    clock = 0
    waiting = sorted([p.copy() for p in processes], key=lambda p: p["arrival"])
    queue = []
    timeline = []
    quantum_map = {}
    level_map = {}
    base_q = 1

    while waiting or queue:
        while waiting and waiting[0]["arrival"] <= clock:
            p = waiting.pop(0)
            quantum_map[p["name"]] = base_q
            level_map[p["name"]] = 0
            queue.append(p)

        if queue:
            queue.sort(key=lambda p: level_map[p["name"]])
            p = queue.pop(0)
            q = quantum_map[p["name"]]
            t = min(p["remaining"], q)
            timeline.append({"name": p["name"], "start": clock, "end": clock + t})
            clock += t
            p["remaining"] -= t

            while waiting and waiting[0]["arrival"] <= clock:
                np = waiting.pop(0)
                quantum_map[np["name"]] = base_q
                level_map[np["name"]] = 0
                queue.append(np)

            if p["remaining"] > 0:
                level_map[p["name"]] += 1
                quantum_map[p["name"]] = base_q * (2 ** level_map[p["name"]])
                queue.append(p)
        else:
            clock += 1

    return timeline


def plot_gantt_comparativo(gantts, output_file):
    fig, axs = plt.subplots(nrows=3, figsize=(12, 9))
    colors = cm.get_cmap("tab20", 20)
    for ax, (name, gantt) in zip(axs, gantts.items()):
        procs = sorted({t["name"] for t in gantt})
        y_map = {n: i for i, n in enumerate(procs)}
        c_map = {n: colors(i) for i, n in enumerate(procs)}
        for t in gantt:
            ax.barh(
                y_map[t["name"]],
                t["end"] - t["start"],
                left=t["start"],
                height=0.5,
                color=c_map[t["name"]],
            )
        ax.set_yticks(list(y_map.values()))
        ax.set_yticklabels(procs)
        ax.set_xlabel("Tempo")
        ax.set_title(name)
        ax.grid(True, axis="x", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def executar_todos(input_dir="entradas", output_dir="resultados"):
    os.makedirs(output_dir, exist_ok=True)
    for f in sorted(os.listdir(input_dir)):
        if not f.endswith(".txt"):
            continue
        path = os.path.join(input_dir, f)
        processos, quantum = parse_input(path)
        gantts = {
            "Round Robin Scheduling": round_robin_scheduler(
                [p.copy() for p in processos], quantum
            ),
            "Priority Scheduling": priority_rr_scheduler(
                [p.copy() for p in processos], quantum
            ),
            "Multilevel Queue Scheduling": multilevel_queue_scheduler(
                [p.copy() for p in processos]
            ),
        }
        out = os.path.join(output_dir, f"{os.path.splitext(f)[0]}_comparativo_p2.png")
        plot_gantt_comparativo(gantts, out)
        print(f"Gráfico gerado: {out}")


if __name__ == "__main__":
    executar_todos()
