import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pprint import pprint

def parse_input(input_path):
    with open(input_path, 'r') as input_file:
        lines = input_file.read().strip().split('\n')

    n = int(lines[0])
    processes = []
    
    for line in lines[1:n+1]:
        name, arrival, duration, priority = line.split()
        processes.append({
            'name': name,
            'arrival': int(arrival),
            'duration': int(duration),
            'priority': int(priority)
        })

    return processes, int(lines[-1].split("=")[-1])


def fcfs_scheduler(processes):
    processes.sort(key=lambda x: x['arrival'])
    process_new = []
    start = 0

    for p in processes:
        process_new.append({
            'name': p['name'],
            'start': start,
            'end': start + p['duration'],
        })
        start += p['duration']

    return process_new


def plot_gantt_chart(gantt, ax):
    """
    Recebe uma lista de dicionários. Cada dicionário é composto por:
        name: Nome do Processo (string)
        start: Tempo que o processo inicia no gráfico (int)
        end: Tempo que o processo finaliza no gráfico (int)
    """
    process_names = list({task['name'] for task in gantt})
    process_names.sort()
    name_to_y = {name: i for i, name in enumerate(process_names)}

    colors = cm.get_cmap('Pastel1', len(process_names))
    name_to_color = {name: colors(i) for i, name in enumerate(process_names)}

    for task in gantt:
        y_pos = name_to_y[task['name']]
        ax.barh(y_pos, task['end'] - task['start'], left=task['start'], height=0.5,
                align='center', color=name_to_color[task['name']])

    max_time = max(task['end'] for task in gantt)
    ax.set_xlim(0, max_time + 1)
    ax.set_xticks(range(0, max_time + 1))
    ax.set_yticks(list(name_to_y.values()))
    ax.set_yticklabels(list(name_to_y.keys()))
    ax.set_xlabel('Time')
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)


fig, axs = plt.subplots(figsize=(10, 3))
process_list, quantum = parse_input('C:\\Users\\aluno.laboratorio\\Downloads\\laboratorio\\entradas\\entrada_1.txt')
gantt_data = fcfs_scheduler(process_list)
gantt_data.append({'name': 'A', 'start': 10, 'end': 12})
plot_gantt_chart(gantt_data, axs)
axs.set_title('Gantt Chart - FCFS Scheduling')
plt.show()
