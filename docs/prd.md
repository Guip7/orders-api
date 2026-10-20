# Orders API: PRD

## Problema
Lojas online vendem produtos com estoque limitado. Sem um controle adequado, o mesmo item é vendido para dois clientes ao mesmo tempo, o cliente é cobrado em duplicidade quando clica duas vezes em "pagar" ou repete a requisição por falha de rede, e o pedido fica em estado inconsistente quando a confirmação do pagamento demora ou chega fora de ordem. A Orders API é o backend que gerencia catálogo, estoque, pedidos e pagamento de forma consistente e confiável, mesmo sob concorrência e falhas.

## Desafios técnicos

Concorrência: dois clientes comprando o último item ao mesmo tempo (locks, transações)
Idempotência: retries e cliques duplicados não podem gerar pedidos ou cobranças duplicadas
Assincronismo: pagamento confirmado depois, via webhook (filas e workers)
Performance: listagens pesadas (índices, cache, paginação por cursor)

## Usuários
Customer: cadastra-se, autentica-se, navega e busca produtos, cria pedidos, paga, acompanha o status e cancela pedidos.
Admin: cadastra e edita produtos, ajusta estoque, consulta todos os pedidos e gerencia usuários.

## Requisitos funcionais (MVP)
RF01: Usuário pode se cadastrar com e-mail e senha.
RF02: Usuário pode se autenticar e receber access token e refresh token.
RF03: Usuário pode renovar o access token com o refresh token e fazer logout (revogação).
RF04: Rotas são protegidas por papel (customer ou admin).
RF05: Admin pode criar, editar, desativar e listar produtos.
RF06: Admin pode ajustar o estoque de um produto.
RF07: Customer pode listar produtos com filtro, busca por nome e paginação por cursor.
RF08: Customer pode criar um pedido com um ou mais itens, desde que haja estoque.
RF09: Ao criar o pedido, o estoque é reservado de forma atômica (sem overselling).
RF10: Criar pedido com a mesma Idempotency-Key retorna o pedido original, sem duplicar.
RF11: Pedido segue a máquina de estados pending → paid → shipped → delivered, com cancelled possível a partir de pending e paid.
RF12: Customer pode cancelar um pedido pending; o estoque reservado é devolvido.
RF13: Pedido pending é enviado a um gateway de pagamento fake de forma assíncrona.
RF14: A API recebe o webhook do gateway e atualiza o pedido (processamento idempotente e com validação de assinatura).
RF15: Pedido pending sem pagamento após um tempo limite é cancelado automaticamente e o estoque é devolvido.
RF16: A cada mudança de status do pedido, um worker dispara uma notificação (e-mail simulado via log).
RF17: Customer consulta seus pedidos e o status de cada um; admin consulta todos.

## Requisitos não funcionais
RNF01: Listagem de produtos responde em < 200ms (p95) com 10 mil produtos cadastrados.
RNF02: Nenhum pedido pode ser criado duas vezes por retry do cliente.
RNF03: Nenhum item é vendido acima do estoque disponível, mesmo com 100 requisições simultâneas.
RNF04: Toda a stack sobe com docker compose up.
RNF05: Cobertura de testes >= 80%.
RNF06: Senhas armazenadas com hash seguro (argon2 ou bcrypt); nenhum segredo no repositório.
RNF07: Logs estruturados (JSON) com correlation id por requisição.
RNF08: Métricas expostas em formato Prometheus (latência, taxa de erro, requisições por rota).
RNF09: Pipeline de CI roda lint, tipagem e testes em todo Pull Request.

## Fora de escopo
Frontend, pagamento real, frete, cupons, multi-tenant, deploy em nuvem.