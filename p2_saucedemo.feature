Funcionalidade: Fluxo de compras na Swag Labs (SauceDemo)
  Como um cliente da loja virtual Swag Labs
  Eu quero autenticar, escolher produtos e finalizar uma compra com segurança
  Para que eu possa adquirir itens de forma prática e sem obstáculos

  # O contexto inicial garante que sempre partimos da tela de login.
  Contexto:
    Dado que acesso a página de login de Swag Labs em "https://www.saucedemo.com/"

  Cenário: Login com credenciais válidas
    Dado que estou na página de login
    Quando informo o nome de usuário "standard_user" e a senha "secret_sauce"
    Então devo ser autenticado com sucesso
    E devo ser redirecionado para a lista de produtos
    E devo ver o título da página "Products"

  Cenário: Login com senha inválida
    Dado que estou na página de login
    Quando informo o nome de usuário "standard_user" e a senha "senha_incorreta"
    Então devo visualizar a mensagem de erro "Epic sadface: Username and password do not match any user in this service"
    E não devo ser autenticado

  Cenário: Login com usuário bloqueado
    Dado que estou na página de login
    Quando informo o nome de usuário "locked_out_user" e a senha "secret_sauce"
    Então devo visualizar a mensagem de erro "Epic sadface: Sorry, this user has been locked out."
    E não devo ser autenticado

  Cenário: Adicionar produto ao carrinho e visualizar carrinho
    Dado que fiz login com o usuário "standard_user" e a senha "secret_sauce"
    E que estou na lista de produtos
    Quando ordeno os produtos por "Price (low to high)"
    E adiciono o produto mais barato ao carrinho
    Então o ícone de carrinho deve exibir a quantidade "1"
    E o botão do produto deve mudar para "Remove"
    Quando eu acessar o carrinho
    Então devo ver o item "Sauce Labs Onesie" com preço "$7.99"

  Cenário: Remover produto do carrinho
    Dado que já adicionei o item "Sauce Labs Onesie" ao carrinho
    E estou visualizando o carrinho
    Quando removo o item do carrinho
    Então o carrinho deve ficar vazio
    E o ícone de carrinho não deve exibir contador

  Cenário: Finalizar compra com sucesso
    Dado que fiz login como "standard_user" e adicionei um item ao carrinho
    Quando inicio o processo de checkout
    E preencho meus dados pessoais com "John" como primeiro nome, "Doe" como sobrenome e "12345" como CEP
    E concluo o pedido
    Então devo visualizar a mensagem "Thank you for your order!"
    E o carrinho deve ser esvaziado

  Esquema do Cenário: Tentativas de login com diferentes perfis
    Dado que estou na página de login
    Quando informo o nome de usuário "<usuario>" e a senha "<senha>"
    Então devo visualizar a mensagem "<mensagem>"
    E o resultado da autenticação deve ser "<resultado>"

    Exemplos:
      | usuario         | senha         | mensagem                                                                     | resultado |
      | standard_user   | secret_sauce  | Login realizado com sucesso                                                 | sucesso  |
      | locked_out_user | secret_sauce  | Epic sadface: Sorry, this user has been locked out.                        | falha    |
      | user_invalido   | secret_sauce  | Epic sadface: Username and password do not match any user in this service  | falha    |
      | problem_user    | secret_sauce  | Login realizado com sucesso                                                 | sucesso  |