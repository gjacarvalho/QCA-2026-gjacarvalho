# Proposta: gota de etanol com metamizol neutro

## Why

Além da caixa periódica já produzida, é necessária uma configuração molecular finita em forma de gota, com o metamizol neutro no centro e etanol ao seu redor.

## What Changes

- Gerar uma gota esférica não periódica de raio 15 Å.
- Fixar uma molécula de metamizol neutro no centro (15, 15, 15) Å.
- Calcular e inserir 146 moléculas de etanol usando a densidade-alvo já aprovada.
- Gerar PDB e XYZ sem modificar os artefatos da caixa cúbica anterior.
- Validar raio, centro, composição, geometrias rígidas e sobreposições.

## Capabilities

### New Capabilities

- `molecular-droplet-packing`: geração e validação de uma gota finita de etanol com soluto central.

### Modified Capabilities

Nenhuma.

## Impact

Serão adicionados novos arquivos com o sufixo `droplet_R15`. As entradas moleculares e o Packmol local já existentes serão reutilizados sem alteração.
