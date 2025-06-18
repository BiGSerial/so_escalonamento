# Simulador de Escalonamento de Processos

Este projeto é um simulador de algoritmos de escalonamento de processos, desenvolvido como parte da disciplina de Sistemas Operacionais – P1 (2025/01) do curso da FAESA. O simulador foi implementado em Python e tem como objetivo comparar visualmente o comportamento de diferentes algoritmos clássicos de escalonamento.

## Objetivo

Simular e comparar os seguintes algoritmos de escalonamento:

- FCFS (First-Come, First-Served)
- SJF (Shortest Job First) – Não Preemptivo
- SJF (Shortest Job First) – Preemptivo

A partir de arquivos de entrada padronizados, o sistema executa cada algoritmo e gera gráficos de Gantt para visualizar o tempo de execução dos processos.

## Estrutura do Projeto

- `simulador.py`: script principal que executa os três algoritmos e gera os gráficos.
- `entradas/`: diretório contendo os arquivos `.txt` com os dados de entrada dos processos.
- `resultados/`: diretório de saída com os gráficos gerados em formato PNG.
- `README.md`: este arquivo.
- `.gitignore`: define os arquivos e diretórios ignorados pelo Git.

## Formato dos Arquivos de Entrada

Cada arquivo de entrada segue o seguinte formato:


<Número de processos>
<ID> <ArrivalTime> <BurstTime> <Priority>

Quantum=<valor>


### Exemplo:
```
3
A 0 6 1
B 2 3 2
C 4 1 1
Quantum=2
```

## Como Executar

1. Clone este repositório:
   ```
   git clone https://github.com/BiGSerial/so_escalonamento.git
   cd so_escalonamento
   ```

2. Certifique-se de ter o Python 3 instalado com as bibliotecas necessárias:
   ```
   pip install matplotlib
   ```

3. Execute o simulador:
   ```
   python simulador.py
   ```

4. Os gráficos de Gantt serão salvos automaticamente na pasta `resultados/`.

## Observações

- O projeto foi desenvolvido com foco acadêmico e segue os requisitos propostos na atividade avaliativa da disciplina.
- Os gráficos gerados facilitam a visualização das diferenças entre os algoritmos quanto ao tempo de espera, o tempo de execução e a ordem de atendimento dos processos.

## Autor

Will Oliveira  
Desenvolvido como parte da disciplina de Sistemas Operacionais (FAESA, 2025/01).  
Professor orientador: Gabriel Soares Baptista

