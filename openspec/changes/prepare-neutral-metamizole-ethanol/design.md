# Design: metamizol neutro em etanol

## Context

O workspace não possuía ferramentas químicas especializadas nem compilador Fortran. O Packmol fornece distribuição pré-compilada via PyPI; por isso será instalado em ambiente virtual local, evitando mudanças no sistema Kubuntu.

## Goals / Non-Goals

### Goals

- Reutilizar literalmente coordenadas 3D provenientes do PubChem.
- Gerar uma configuração Packmol determinística na medida suportada pela ferramenta.
- Manter rastreabilidade de entradas, comandos, versões e resultados.
- Validar o produto independentemente das mensagens de sucesso do Packmol.

### Non-Goals

- Escolher motor de dinâmica molecular.
- Atribuir campo de força, cargas, topologia ou condições de produção.
- Garantir a densidade termodinâmica final antes de minimização/equilíbrio NPT.

## Decisions

### Estruturas e conversão

Os registros 3D SDF dos CIDs 3111 e 702 serão preservados em `inputs/raw/`. Um conversor local lerá os átomos e coordenadas do bloco SDF e emitirá PDBs compatíveis com Packmol. A fórmula será validada pela contagem de elementos antes da conversão.

### Geometria do sistema

O metamizol será centralizado em (12, 12, 12) Å e mantido em orientação inicial. Os 143 etanóis serão distribuídos dentro da caixa periódica `[0,24]³`. A tolerância Packmol será 2,0 Å. O recurso `pbc` nativo será usado para evitar contatos também entre faces opostas da caixa. Uma margem de 0,1 Å nas restrições do solvente absorverá a tolerância numérica das restrições e manterá os átomos na célula primária.

### Saídas e validação

O Packmol produzirá um PDB intermediário. O script acrescentará metadados CRYST1 e produzirá XYZ das mesmas coordenadas. O validador verificará:

- fórmulas das entradas;
- número total de átomos e moléculas;
- caixa declarada e limites cartesianos;
- menor distância periódica (imagem mínima) entre átomos de moléculas diferentes;
- equivalência das coordenadas PDB/XYZ dentro da precisão de escrita;
- presença e checksums dos artefatos.

## Diretórios

```text
inputs/raw/       downloads originais
inputs/prepared/  PDBs moleculares usados pelo Packmol
packmol/          arquivo de entrada
scripts/          automação e validação
outputs/          PDB e XYZ finais
logs/             saída do Packmol
validation/       relatórios JSON e Markdown
tools/            ambiente local da ferramenta
```

## Risks / Trade-offs

- A contagem de 143 etanóis usa o volume total da caixa e não desconta o volume parcial do soluto.
- A tolerância geométrica do Packmol não substitui minimização de energia.
- O formato PDB limita coordenadas a três casas decimais; os SDFs originais são mantidos para preservar a fonte.
- Protonação, tautomeria e parametrização deverão ser revistas à luz do campo de força e do pH pretendidos antes da dinâmica molecular.

## Open Questions

Nenhuma questão bloqueante após a aprovação explícita do metamizol neutro e das demais decisões apresentadas.
