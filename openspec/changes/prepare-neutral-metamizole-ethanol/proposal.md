# Proposta: preparar metamizol neutro em etanol

## Why

É necessário produzir uma configuração inicial reproduzível de uma molécula de metamizol neutro solvatada em etanol, em uma caixa cúbica de 24 Å, para servir de ponto de partida a uma etapa posterior de parametrização e simulação molecular.

## What Changes

- Registrar estruturas moleculares com proveniência verificável.
- Calcular a quantidade de etanol a partir da densidade-alvo documentada.
- Instalar o Packmol isoladamente no workspace.
- Produzir uma entrada Packmol e um script CLI reproduzível.
- Gerar coordenadas empacotadas em PDB e XYZ.
- Validar composição, dimensões, limites geométricos, distâncias intermoleculares e consistência dos arquivos.
- Documentar comandos, decisões, limitações e próximos passos.

## Capabilities

### New Capabilities

- `molecular-packing`: geração reproduzível e validação de uma caixa molecular de metamizol neutro em etanol.

### Modified Capabilities

Nenhuma.

## Impact

Serão adicionados documentos, scripts, entradas moleculares, uma instalação local do Packmol, arquivos de saída e relatórios. Nenhum arquivo previamente existente será modificado ou removido.
