# Especificação: gota molecular

## ADDED Requirements

### Requirement: Geometria da gota

O sistema SHALL representar uma gota esférica não periódica de etanol, com centro em (15, 15, 15) Å e raio máximo de 15 Å.

#### Scenario: Limite radial

- **WHEN** as coordenadas finais forem analisadas
- **THEN** nenhum átomo SHALL estar a mais de 15 Å do centro da gota, considerada tolerância de escrita de 0,002 Å
- **AND** o PDB não SHALL declarar condições periódicas por meio de CRYST1

### Requirement: Soluto central

O sistema SHALL conter uma molécula de metamizol neutro C13H17N3O4S com baricentro em (15, 15, 15) Å.

#### Scenario: Centro do soluto

- **WHEN** os átomos MTZ forem analisados
- **THEN** SHALL formar exatamente uma molécula
- **AND** seu baricentro SHALL coincidir com o centro dentro de 0,002 Å por eixo

### Requirement: Solvente

O sistema SHALL conter 146 moléculas de etanol C2H6O ao redor do soluto.

#### Scenario: Composição final

- **WHEN** o PDB final for analisado
- **THEN** SHALL conter 147 moléculas e 1352 átomos
- **AND** SHALL conter 1 MTZ e 146 ETL

### Requirement: Separação intermolecular

O Packmol SHALL usar tolerância de 2,0 Å sem condições periódicas.

#### Scenario: Contatos diretos

- **WHEN** átomos de moléculas distintas forem comparados
- **THEN** a menor distância cartesiana SHALL ser pelo menos 1,99 Å

### Requirement: Proveniência e rigidez

As mesmas entradas PubChem aprovadas para o sistema cúbico SHALL ser reutilizadas, e as geometrias internas SHALL permanecer rígidas dentro de 0,005 Å de desvio devido à precisão PDB.

#### Scenario: Comparação de geometria

- **WHEN** as assinaturas de distâncias internas forem comparadas às entradas
- **THEN** os desvios máximos do metamizol e do etanol SHALL ser menores ou iguais a 0,005 Å
