# BDD — EducaMais (Login e Recuperação de Senha)

## Visão geral
Este trabalho transforma requisitos informais do módulo de autenticação da plataforma EducaMais em comportamentos testáveis usando BDD com Gherkin (Given/When/Then).

## O que foi coberto nos cenários
### Login
1. **Login com credenciais válidas** (caminho feliz).
2. **Senha incorreta na 1ª tentativa** (mensagem correta + incremento de falhas).
3. **Senha incorreta na 2ª tentativa** (continua incrementando e não bloqueia ainda).
4. **Bloqueio após 3 tentativas inválidas consecutivas** (mensagem “Conta bloqueada.” + bloqueia + não autentica).
5. **Login com conta já bloqueada** (mesmo com senha correta, acesso negado).

### Recuperação de senha
6. **Recuperação com e-mail cadastrado** (sistema envia e-mail).
7. **Recuperação com e-mail inexistente** (não envia e-mail, mas mantém resposta genérica).
8. **Fluxo completo** (solicita recuperação → acessa link → redefine senha → consegue logar com a nova senha).

Além disso, foi incluído um **Scenario Outline** para representar variações das tentativas inválidas de login.

## Justificativa dos exemplos escolhidos
- Foram incluídos casos de **sucesso e falha** para evitar focar apenas no caminho feliz.
- O **bloqueio após 3 tentativas** foi modelado com contador de falhas para permitir verificação do comportamento incremental.
- Na recuperação de senha, foi usado retorno **genérico** (“Se o e-mail estiver cadastrado...”) para evitar vazamento de informação (segurança).

## Pontos de atenção identificados
- **Consecutividade das tentativas**: o requisito diz “3 vezes seguidas”. Em uma implementação real, deve ficar claro se:
  - o contador reseta ao acertar a senha, ou
  - reseta após um tempo, ou
  - reseta após recuperar senha/desbloqueio.
- **Mensagem e comportamento com conta bloqueada**: deve ser consistente (sempre negar login).
- **Recuperação de senha**:
  - link deve ter validade e token único;
  - deve existir política mínima de senha (ex.: tamanho, complexidade);
  - respostas devem evitar confirmar se o e-mail existe (anti-enumeração).
- **Logs e auditoria**: recomendável registrar tentativas para segurança e suporte.

## Observação
Este trabalho não implementa Cucumber/Steps nem automação com Selenium/Cypress — apenas especifica comportamentos em BDD conforme solicitado.
