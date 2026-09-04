# Prompts utilizados

Registro textual dos prompts enviados pelo usuário durante a criação deste projeto, em ordem cronológica.

## Prompt 1 — preparação inicial

```text
Use as metodologias dos repositórios Superpowers (https://github.com/obra/superpowers/) para analisar e planejar o trabalho, e OpenSpec (https://github.com/Fission-AI/openspec) para documentar requisitos e implementação.

No Linux Kubuntu, prepare um sistema molecular para simulação contendo uma molécula de dipirona solvatada em etanol dentro de uma caixa cúbica de 24 Å de lado, utilizando o Packmol (https://github.com/m3g/packmol).

Antes de executar, verifique os arquivos e ferramentas disponíveis e esclareça apenas informações essenciais ausentes, como a estrutura correta da dipirona, o modelo do etanol, a densidade-alvo e os formatos de saída. Calcule e justifique o número de moléculas de etanol. Depois:

1. Crie a especificação e o plano de execução.
2. Instale ou configure o Packmol, se necessário.
3. Prepare os arquivos moleculares de entrada.
4. Gere o arquivo de entrada do Packmol e um script CLI reproduzível.
5. Execute o empacotamento e valide dimensões, composição, sobreposições e arquivos gerados.
6. Documente os comandos, decisões, limitações e próximos passos.

Preserve arquivos existentes e não invente coordenadas, parâmetros ou cargas. Organize todos os artefatos em diretórios claros e entregue um resumo final com os caminhos dos arquivos e instruções para reproduzir o processo.
```

## Prompt 2 — identidade química e fluxo

```text
utilize a formula metamizol neutro; me apresnete  fluxo será proposal → specs → design → tasks → implementação → verificação, e se tiver duvidas me pergunte
```

## Prompt 3 — diário e implementação

```text
construa um diario.md e registre tudo o que foi conversado e implemente esse plano
```

## Prompt 4 — gota esférica

```text
agora faca uma gota de com raio 15Angstrom com a dipirona no meio e o solvente envolta dela
```

## Prompt 5 — publicação no GitHub

```text
suba no github nesse repositorio https://github.com/gjacarvalho/QCA-2026-gjacarvalho  e faça um README.md sobre tudo o que foi feito salvando os prompts utilizados e o estado atual e faça a mesma coisa no README do github
```

## Observação

O conteúdo técnico produzido em resposta aos prompts está registrado no `README.md`, em `diario.md`, nos artefatos OpenSpec, nos planos Superpowers, nos scripts e nos relatórios de validação.
