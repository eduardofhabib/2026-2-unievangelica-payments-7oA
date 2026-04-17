import sqlite3
import pytest
from app.carrinho_db import (
    criar_tabela,
    adicionar_item,
    listar_itens,
    calcular_total,
    limpar_carrinho
)

# =========================
# Fixture do banco em memória
# =========================
@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    criar_tabela(conn)
    yield conn
    conn.close()


# =========================
# Missão 1 — Persistência
# =========================

def test_item_persiste_no_banco(db):
    # Arrange
    adicionar_item(db, "Produto A", 100.0, 2)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Produto A"
    assert itens[0]["preco"] == 100.0
    assert itens[0]["quantidade"] == 2


def test_multiplos_itens_persistem(db):
    # Arrange
    adicionar_item(db, "A", 10.0, 1)
    adicionar_item(db, "B", 20.0, 2)
    adicionar_item(db, "C", 30.0, 3)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 3


def test_preco_negativo_lanca_value_error(db):
    # Assert
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto inválido", -10.0, 1)


# =========================
# Missão 2 — Cálculo de total
# =========================

def test_carrinho_vazio_retorna_zero(db):
    # Act
    total = calcular_total(db)

    # Assert
    assert total == 0.0


def test_total_considera_quantidade(db):
    # Arrange
    adicionar_item(db, "Produto", 50.0, 3)

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 150.0


def test_total_multiplos_itens(db):
    # Arrange
    adicionar_item(db, "A", 10.0, 2)  # 20
    adicionar_item(db, "B", 5.0, 4)   # 20
    adicionar_item(db, "C", 3.0, 1)   # 3

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 43.0


# =========================
# Missão 3 — Limpeza
# =========================

def test_limpar_remove_todos_os_itens(db):
    # Arrange
    adicionar_item(db, "A", 10.0, 1)
    adicionar_item(db, "B", 20.0, 1)

    # Act
    limpar_carrinho(db)
    itens = listar_itens(db)
    total = calcular_total(db)

    # Assert
    assert itens == []
    assert total == 0.0


def test_pode_adicionar_apos_limpar(db):
    # Arrange
    adicionar_item(db, "A", 10.0, 1)
    limpar_carrinho(db)

    # Act
    adicionar_item(db, "B", 20.0, 2)
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "B"
    assert itens[0]["preco"] == 20.0
    assert itens[0]["quantidade"] == 2
