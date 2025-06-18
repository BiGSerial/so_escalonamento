# Simulador de Escalonamento de Processos

Este projeto é um simulador de algoritmos de escalonamento de processos, desenvolvido como parte da disciplina de Sistemas Operacionais – P1 e P2 (2025/01) do curso da FAESA. O simulador foi implementado em Python e tem como objetivo comparar visualmente o comportamento de diferentes algoritmos clássicos de escalonamento.

## Objetivo

Simular e comparar os seguintes algoritmos de escalonamento:

### Parte 1 (simulador_p1.py)
- FCFS (First-Come, First-Served)
- SJF (Shortest Job First) – Não Preemptivo
- SJF (Shortest Job First) – Preemptivo

### Parte 2 (simulador_p2.py)
- Round-Robin (com quantum fixo)
- Round-Robin com prioridade
- Multilevel Queue com quantums crescentes (potências de 2)

A partir de arquivos de entrada padronizados, o sistema executa cada algoritmo e gera gráficos de Gantt para visualizar o tempo de execução dos processos.

## Estrutura do Projeto

- `simulador_p1.py`: implementa os algoritmos da Parte 1.
- `simulador_p2.py`: implementa os algoritmos da Parte 2.
- `entradas/`: diretório contendo os arquivos `.txt` com os dados de entrada dos processos.
- `resultados/`: diretório de saída com os gráficos gerados em formato PNG.
- `README.md`: este arquivo.
- `.gitignore`: define os arquivos e diretórios ignorados pelo Git.

## Formato dos Arquivos de Entrada

Cada arquivo de entrada segue o seguinte formato:

```
<Número de processos>
<ID> <ArrivalTime> <BurstTime> <Priority>
...
Quantum=<valor>
```

### Exemplo:
```
3
A 0 6 1
B 2 3 2
C 4 1 1
Quantum=2
```

## Como Executar

Clone este repositório:

```
git clone https://github.com/BiGSerial/so_escalonamento.git
cd so_escalonamento
```

Crie um ambiente virtual e ative:

```
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

Instale as dependências:

```
pip install -r requirements.txt
```

### Para executar a Parte 1:

```
python simulador_p1.py
```

### Para executar a Parte 2:

```
python simulador_p2.py
```

Os gráficos de Gantt serão gerados automaticamente na pasta `resultados/`.

## Observações

- O projeto foi desenvolvido com foco acadêmico e segue os requisitos propostos nas atividades avaliativas da disciplina.
- Os gráficos gerados facilitam a visualização das diferenças entre os algoritmos quanto ao tempo de espera, tempo de execução e ordem de atendimento dos processos.

## Autor

Will Oliveira  
Desenvolvido como parte da disciplina de Sistemas Operacionais (FAESA, 2025/01)  
Professor orientador: Gabriel Soares Baptista
