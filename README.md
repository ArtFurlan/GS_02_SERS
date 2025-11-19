# Manager IoT de Energia — Automação e Monitoramento IoT

## Projeto de Sustentabilidade e Eficiência Energética

---

## Integrantes
- Arthur Marangoni Furlan - RM: 564665
- Gustavo Sartori S. Grigoletto - RM: 565726
- Vinicius Macedo Carvalho - RM: 563791

---

## Objetivo do Projeto

Este projeto tem como objetivo desenvolver uma solução IoT (real ou simulada) para monitoramento e automação do consumo energético em um hotel médio. Utilizando sensores simulados, lógica de controle e programação baseada em dados, a solução busca reduzir desperdícios, automatizar rotinas operacionais e promover práticas sustentáveis dentro do ambiente de trabalho.

A solução apresentada integra automação, eficiência energética e sustentabilidade, elementos essenciais no contexto do futuro do trabalho, onde decisões inteligentes e baseadas em dados tornam as operações mais eficientes e competitivas.

---

## Futuro do Trabalho

A solução não foi só montada para esse caso mas também para o futuro do trabalho, pois transforma processos antes manuais e ineficientes em rotinas automatizadas, inteligentes e sustentáveis. O sistema IoT melhora diretamente os ambientes e as rotinas produtivas ao:

- reduzir a necessidade de verificações manuais de equipamentos (como conferir se o ar-condicionado dos quartos está desligado);
- permitir que a equipe de manutenção atue de forma proativa, baseada em dados, e não apenas reagindo a problemas;
- automatizar tarefas repetitivas, liberando os funcionários para atividades mais estratégicas e de maior valor;
- criar ambientes mais confortáveis, estáveis e energeticamente eficientes para hóspedes e colaboradores;
- diminuir desperdícios e custos operacionais, permitindo que a gestão do hotel tome decisões melhores e mais rápidas;
- integrar sustentabilidade ao dia a dia, alinhando o hotel às exigências do mercado e às práticas modernas de gestão.

Assim, a solução IoT contribui para ambientes de trabalho mais eficientes, produtivos, sustentáveis e tecnologicamente preparados para os desafios do futuro.

---

# > Dados Utilizados — Simulados

O dataset representa 30 dias de consumo energético com discriminação por setor, ou seja, o consumo é separado por áreas (quartos, cozinha, ar-condicionado, iluminação etc.).  
Esses dados alimentam a lógica IoT para simular cenários reais de automação e tomadas de decisão.

### Arquivo  
`data/consumo_hotel_mensal.csv`

### Colunas
- dia
- consumo_total_kwh
- consumo_quartos_kwh
- consumo_lavanderia_kwh
- consumo_cozinha_kwh
- consumo_ar_condicionado_kwh
- consumo_iluminacao_kwh

Esses dados servem para ajustar o comportamento do sistema IoT, como:

- ligar/desligar setores com base no consumo diário,
- detectar picos de uso,
- ativar modos econômicos automatizados,
- simular tomada de decisão inteligente.

---

# > Sistema IoT Simulado 

## Visão Geral

O Manager IoT de Energia é um sistema de automação simulada que monitora presença, ocupação, horário e consumo energético estimado para acionar automaticamente:

- ar-condicionado,  
- iluminação,  
- aquecimento de água,  
- setores operacionais (ex.: lavanderia),  
- modos energéticos inteligentes.

## Lógica do Sistema IoT

O sistema usa três entradas principais:

- ocupação do quarto (vinda do sistema de reservas -> simulado),
- presença (simulada via sensor PIR),
- consumo do setor específico do CSV.

A partir disso, são aplicadas regras como:

> Quarto vazio -> desliga AC e iluminação  
> Quarto ocupado mas sem presença -> AC em modo ECO  
> Horário noturno -> iluminação reduzida  
> Picos de consumo -> acionamento de alerta  
> Lavanderia -> operação proibida no horário de ponta  

---

# Código do Dispositivo IoT Simulado

Arquivo: `src/simulacao_iot.py`

```python
import pandas as pd

df = pd.read_csv('../data/consumo_hotel_mensal.csv')

# Simulação do sensor
presenca = False
quarto_ocupado = False
horario = 23  # 23h
ar_condicionado = True
iluminacao = True

print("Simulação IoT")

# Regra 1: Quarto desocupado -> tudo desliga
if not quarto_ocupado:
    ar_condicionado = False
    iluminacao = False
    print("Quarto vazio: AC e iluminação desligados.")

# Regra 2: Quarto ocupado mas sem presença -> Modo econômico
elif quarto_ocupado and not presenca:
    ar_condicionado = True
    print("Quarto ocupado sem presença: AC em modo ECO.")

# Regra 3: Presença detectada -> Conforto total
elif quarto_ocupado and presenca:
    ar_condicionado = True
    iluminacao = True
    print("Presença detectada: Conforto mantido.")

# Regra 4: Iluminação noturna reduzida
if horario >= 0 and horario <= 5:
    iluminacao = False
    print("Horário noturno: iluminação reduzida.")

print(f"Estado final: AC={ar_condicionado}, Luz={iluminacao}")
```
# > Resultados Esperados

A automação implementada permite:
- Reduzir desperdícios de energia automaticamente
- Evitar AC ligado em quartos vazios
- Reduzir intensidade de iluminação noturna sem intervenção humana
- Diminuir custos operacionais
- Melhorar a experiência de hóspedes e colaboradores
- Promover sustentabilidade e responsabilidade energética

Comportamentos esperados:

- até 30% de economia nos quartos, dependendo da ocupação,
- redução total da iluminação de corredores durante a madrugada,
- automação de rotinas repetitivas,
- maior eficiência operacional sem aumentar carga de trabalho da equipe.

# > Estrutura do Repositório

```
hotel-energy-optimization/
├── data/
│   └── consumo_hotel_mensal.csv
├── codigo
│   └── simulacao.py
├── README.md
└── requirements.txt
```

# > Como Executar

1. Instalar dependências:
   ```
   pip install -r requirements.txt

2. Rodar a simulação IoT:
   ```
   python codigo/simulacao.py

A saída mostrará o comportamento automático do sistema conforme presença, ocupação e horário.

