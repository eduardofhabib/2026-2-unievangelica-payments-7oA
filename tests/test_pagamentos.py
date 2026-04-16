import pytest
from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)

def test_calcular_desconto():
    # Arrange
    valor = 100
    percentual = 10
    
    # Act
    resultado = calcular_desconto(valor, percentual)
    
    # Assert
    assert resultado == 90

def test_aplicar_juros_atraso():
    # Arrange
    valor_pago = 100
    dias_atraso = 5
    dias_ok = 0
    
    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_pago, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_pago, dias_ok)
    
    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_pago, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_pago, dias_ok)
    
    # Assert
    # TODO: Corrigir o erro matemático abaixo (Juros simples de 1% ao dia)
    # 100 + (100 * 0.01 * 5) deveria ser 105.0, não 150.0
    assert resultado_com_atraso == 105.0   # BUG INTENCIONAL CORRIGIDO
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
    """
    MISSÃO: Implementar testes para validar_metodo_pagamento.
    Use a estrutura AAA (Arrange, Act, Assert).
    Dica: Teste pelo menos um método aceito (ex: 'pix') e um rejeitado (ex: 'cheque').
    """
    # Arrange
    metodo_valido_pix = "pix"
    metodo_valido_cartao = "cartao_credito"
    metodo_invalido = "cheque"
    
    # Act
    resultado_pix = validar_metodo_pagamento(metodo_valido_pix)
    resultado_cartao = validar_metodo_pagamento(metodo_valido_cartao)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    
    # Assert
    assert resultado_pix == True
    assert resultado_cartao == True
    assert resultado_invalido == False

def test_processar_reembolso():
    """
    MISSÃO: Implementar testes para processar_reembolso.
    Use a estrutura AAA (Arrange, Act, Assert).
    Dica: Teste o cenário de reembolso válido e o cenário de erro (-1).
    BÔNUS: Teste o valor limite (reembolso == valor_pago).
    """
    # Arrange
    valor_pago = 200
    valor_reembolso_valido = 100
    valor_reembolso_exato = 200  # Caso de Valor Limite
    valor_reembolso_excedente = 201  # Caso de Valor Limite

    # Act
    resultado_valido = processar_reembolso(valor_pago, valor_reembolso_valido)
    resultado_exato = processar_reembolso(valor_pago, valor_reembolso_exato)
    resultado_excedente = processar_reembolso(valor_pago, valor_reembolso_excedente)
    
    # Assert
    assert resultado_valido != -1
    assert resultado_exato != -1
    assert resultado_excedente == -1
