# Especificação: empacotamento molecular

## ADDED Requirements

### Requirement: Proveniência molecular

O sistema SHALL usar coordenadas moleculares obtidas de registros públicos identificados, sem criar coordenadas, cargas ou parâmetros de campo de força.

#### Scenario: Estrutura do soluto

- **WHEN** a entrada do metamizol for preparada
- **THEN** sua fonte SHALL ser o conformero 3D PubChem CID 3111
- **AND** sua fórmula SHALL ser C13H17N3O4S
- **AND** não SHALL conter sódio ou água de hidratação

#### Scenario: Estrutura do solvente

- **WHEN** a entrada do etanol for preparada
- **THEN** sua fonte SHALL ser o conformero 3D PubChem CID 702
- **AND** sua fórmula SHALL ser C2H6O

### Requirement: Composição

O sistema SHALL conter exatamente uma molécula de metamizol neutro e 143 moléculas de etanol.

#### Scenario: Contagem final

- **WHEN** o PDB empacotado for analisado
- **THEN** SHALL conter 1 unidade de metamizol
- **AND** SHALL conter 143 unidades de etanol
- **AND** SHALL conter 1325 átomos no total

### Requirement: Caixa molecular

O sistema SHALL representar uma caixa cúbica de 24 Å de lado.

#### Scenario: Limites cartesianos

- **WHEN** as coordenadas finais forem verificadas
- **THEN** todos os átomos SHALL estar no intervalo de 0 a 24 Å em x, y e z, dentro da precisão do formato PDB
- **AND** o PDB SHALL conter um registro CRYST1 de 24 × 24 × 24 Å e ângulos de 90 graus

### Requirement: Separação intermolecular

O Packmol SHALL ser executado com tolerância explícita de 2,0 Å.

#### Scenario: Validação de contatos

- **WHEN** pares de átomos pertencentes a moléculas diferentes forem examinados
- **THEN** a menor distância sob convenção de imagem mínima periódica SHALL ser informada
- **AND** qualquer distância menor que 1,99 Å SHALL ser registrada como falha
- **AND** distâncias entre 1,99 e 2,00 Å SHALL ser registradas como tolerância numérica do otimizador

### Requirement: Reprodutibilidade

O sistema SHALL fornecer uma interface CLI única que prepare, empacote, converta e valide o sistema.

#### Scenario: Execução limpa

- **WHEN** o script for executado com as entradas e o Packmol disponíveis
- **THEN** SHALL produzir PDB, XYZ, log de execução, relatório JSON e resumo legível
- **AND** SHALL retornar código diferente de zero se uma validação obrigatória falhar

### Requirement: Limite de escopo

Os artefatos SHALL ser descritos como coordenadas iniciais e não como um sistema já parametrizado para dinâmica molecular.

#### Scenario: Ausência de parâmetros

- **WHEN** a entrega for revisada
- **THEN** não SHALL alegar que cargas, tipos atômicos, ligações parametrizadas ou campo de força foram atribuídos
