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

Arquivo: `codigo/simulacao.py`

```python
import pandas as pd

df = pd.read_csv('consumo_hotel_mensal.csv')

consumo_dia = df.loc[0, 'consumo_total_kwh']
limite_consumo = 4300

def avaliar_sistema(presenca: bool, quarto_ocupado: bool, horario: int, consumo_dia: float):
    """
    Avalia o estado do ar-condicionado e da iluminação com base em:
    - presença
    - ocupação do quarto
    - horário
    - consumo do dia
    Retorna: dicionário com estados e lista de alertas.
    """

    ar_condicionado_ligado = False
    iluminacao_ligada = False
    modo_eco = False
    alertas = []

    if not quarto_ocupado:
        ar_condicionado_ligado = False
        iluminacao_ligada = False
        alertas.append("Quarto vazio → ar-condicionado e iluminação desligados.")

    elif quarto_ocupado and not presenca:
        ar_condicionado_ligado = True
        modo_eco = True
        iluminacao_ligada = False
        alertas.append("Quarto ocupado sem presença → ar-condicionado em modo ECO, luz apagada.")

    elif quarto_ocupado and presenca:
        ar_condicionado_ligado = True
        iluminacao_ligada = True
        alertas.append("Presença detectada → conforto mantido (AC e iluminação ligados).")

    if 0 <= horario <= 5:
        iluminacao_ligada = False
        alertas.append("Horário de madrugada → iluminação reduzida/desligada por economia.")

    if consumo_dia > limite_consumo:
        alertas.append(
            f"Alerta de consumo: o dia está com {consumo_dia} kWh, acima do limite de {limite_consumo} kWh."
        )

    estado = {
        "ar_condicionado_ligado": ar_condicionado_ligado,
        "iluminacao_ligada": iluminacao_ligada,
        "modo_eco": modo_eco,
        "alertas": alertas,
    }

    return estado

presenca = False
quarto_ocupado = True
horario = 23

print("=== Simulação IoT de Consumo de Energia ===")
print(f"Consumo do dia (CSV): {consumo_dia} kWh")
print(f"Horário atual: {horario}h")
print(f"Quarto ocupado? {quarto_ocupado}")
print(f"Presença detectada? {presenca}")
print("-" * 60)

resultado = avaliar_sistema(presenca, quarto_ocupado, horario, consumo_dia)

estado_ac = "ligado" if resultado["ar_condicionado_ligado"] else "desligado"
estado_luz = "ligada" if resultado["iluminacao_ligada"] else "desligada"
estado_eco = "ativado" if resultado["modo_eco"] else "desativado"

print(f"Estado final do ar-condicionado: {estado_ac} (modo ECO {estado_eco})")
print(f"Estado final da iluminação: {estado_luz}")
print("\nAlertas gerados:")

if resultado["alertas"]:
    for alerta in resultado["alertas"]:
        print(f"- {alerta}")
else:
    print("- Nenhum alerta gerado. Sistema operando normalmente.")
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
├── codigo/
│   └── simulacao.py
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

