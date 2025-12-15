"""
test_saucedemo.py

Este módulo contém testes automatizados utilizando Selenium para o site Swag Labs (SauceDemo).
Cada função de teste reproduz um cenário descrito na feature em Gherkin, validando login,
manipulação do carrinho e fluxo completo de checkout.

Requisitos:
 - Selenium instalado (pip install selenium)
 - Um driver de navegador compatível (por exemplo, chromedriver) disponível no PATH
 - Python 3.7+

Para executar os testes utilize:
    pytest -s test_saucedemo.py

Se preferir rodar em modo não headless, remova a opção '--headless' das opções do Chrome.
"""

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="function")
def driver():
    """Inicializa e finaliza o WebDriver para cada teste."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # roda sem interface gráfica
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Cria a instância do navegador. Assuma que o chromedriver está no PATH.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def login(driver, username: str, password: str):
    """Realiza login no Swag Labs e retorna se houve erro e a mensagem."""
    driver.get("https://www.saucedemo.com/")
    user_field = driver.find_element(By.ID, "user-name")
    pass_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    user_field.clear()
    user_field.send_keys(username)
    pass_field.clear()
    pass_field.send_keys(password)
    login_button.click()
    # Verifica se aparece mensagem de erro
    try:
        error = driver.find_element(By.CSS_SELECTOR, "div.error-message-container h3")
        return False, error.text
    except Exception:
        return True, ""


def add_first_item_sorted_by_price(driver):
    """Ordena os produtos pelo menor preço e adiciona o primeiro item ao carrinho."""
    # Seleciona ordenação por preço baixo para alto
    sort_select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_select.select_by_visible_text("Price (low to high)")
    # Adiciona primeiro item (deve ser Sauce Labs Onesie) ao carrinho
    add_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")
    add_buttons[0].click()


def go_to_cart(driver):
    """Navega até o carrinho clicando no ícone do carrinho."""
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()


def test_login_valid(driver):
    """Teste: login com credenciais válidas."""
    success, message = login(driver, "standard_user", "secret_sauce")
    assert success, f"Esperava login com sucesso, mas ocorreu erro: {message}"
    # Verifica se está na lista de produtos
    assert "/inventory.html" in driver.current_url
    assert "Products" in driver.page_source


def test_login_invalid_password(driver):
    """Teste: login com senha incorreta."""
    success, message = login(driver, "standard_user", "senha_incorreta")
    assert not success
    assert "Username and password do not match any user" in message


def test_login_locked_out_user(driver):
    """Teste: login com usuário bloqueado."""
    success, message = login(driver, "locked_out_user", "secret_sauce")
    assert not success
    assert "Sorry, this user has been locked out" in message


def test_add_product_to_cart(driver):
    """Teste: adicionar produto mais barato ao carrinho e validar."""
    success, message = login(driver, "standard_user", "secret_sauce")
    assert success, message
    add_first_item_sorted_by_price(driver)
    # Verifica badge com número 1
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1"
    # Verifica que botão virou Remove
    remove_button = driver.find_element(By.CSS_SELECTOR, "button.btn_secondary.cart_button")
    assert remove_button.text.lower() == "remove"
    # Vai para o carrinho e verifica item
    go_to_cart(driver)
    item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    item_price = driver.find_element(By.CLASS_NAME, "inventory_item_price")
    assert item_name.text == "Sauce Labs Onesie"
    assert item_price.text == "$7.99"


def test_remove_product_from_cart(driver):
    """Teste: remover item do carrinho."""
    success, message = login(driver, "standard_user", "secret_sauce")
    assert success, message
    add_first_item_sorted_by_price(driver)
    go_to_cart(driver)
    # Remove item
    remove_button = driver.find_element(By.CSS_SELECTOR, "button.cart_button")
    remove_button.click()
    # Verifica carrinho vazio: badge inexistente e mensagem de carrinho vazio
    assert len(driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")) == 0
    # Página do carrinho quando vazio tem botão Continue Shopping
    assert driver.find_element(By.ID, "continue-shopping").is_displayed()


def test_complete_checkout(driver):
    """Teste: finalizar compra com sucesso."""
    success, message = login(driver, "standard_user", "secret_sauce")
    assert success, message
    add_first_item_sorted_by_price(driver)
    go_to_cart(driver)
    # Inicia checkout
    checkout_btn = driver.find_element(By.ID, "checkout")
    checkout_btn.click()
    # Preenche informações de usuário
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()
    # Na página de resumo verifica total
    total_label = driver.find_element(By.CLASS_NAME, "summary_total_label")
    assert "Total" in total_label.text
    # Finaliza
    driver.find_element(By.ID, "finish").click()
    # Mensagem de sucesso
    success_msg = driver.find_element(By.CLASS_NAME, "complete-header")
    assert success_msg.text == "Thank you for your order!"
    # Carrinho deve estar vazio ao retornar
    driver.find_element(By.ID, "back-to-products").click()
    assert len(driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")) == 0