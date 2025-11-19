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
        alertas.append("Quarto vazio: ar-condicionado e iluminação desligados.")

    elif quarto_ocupado and not presenca:
        ar_condicionado_ligado = True
        modo_eco = True
        iluminacao_ligada = False
        alertas.append("Quarto ocupado sem presença: ar-condicionado em modo ECO, luz apagada.")

    elif quarto_ocupado and presenca:
        ar_condicionado_ligado = True
        iluminacao_ligada = True
        alertas.append("Presença detectada: conforto mantido (AC e iluminação ligados).")

    if 0 <= horario <= 5:
        iluminacao_ligada = False
        alertas.append("Horário de madrugada: iluminação reduzida/desligada por economia.")

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

print(" Simulação IoT de Consumo de Energia")
print(f"Consumo do dia (CSV): {consumo_dia} kWh")
print(f"Horário atual: {horario}h")
print(f"Quarto ocupado? {quarto_ocupado}")
print(f"Presença detectada? {presenca}")
print("--------------------------------------------------------------\n")

resultado = avaliar_sistema(presenca, quarto_ocupado, horario, consumo_dia)

estado_ac = "ligado" if resultado["ar_condicionado_ligado"] else "desligado"
estado_luz = "ligada" if resultado["iluminacao_ligada"] else "desligada"
estado_eco = "ativado" if resultado["modo_eco"] else "desativado"

print(f"Estado final do ar-condicionado: {estado_ac} (modo ECO {estado_eco})")
print(f"Estado final da iluminação: {estado_luz}")
print("\nAlertas gerados:")

if resultado["alertas"]:
    for alerta in resultado["alertas"]:
        print(f"   {alerta}")
else:
    print("   Nenhum alerta gerado. Sistema operando normalmente.")
