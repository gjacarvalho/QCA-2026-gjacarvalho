# Plano de execução: metamizol neutro em etanol

## Resultado esperado

Uma execução de `scripts/build_system.sh` deverá obter/usar entradas rastreáveis, executar Packmol e validar `outputs/metamizole_ethanol_24A.pdb` e `.xyz`.

## Task 1: Configurar Packmol local

**Files:** `tools/packmol-venv/`, `logs/tool_versions.txt`

1. Criar ambiente virtual Python local.
2. Instalar a distribuição oficial `packmol` sem alterar o Python do sistema.
3. Executar `packmol --version` e registrar o resultado.

## Task 2: Obter e preparar estruturas

**Files:** `inputs/raw/*.sdf`, `inputs/raw/SOURCES.md`, `scripts/prepare_structures.py`, `inputs/prepared/*.pdb`

1. Baixar os conformeros 3D dos CIDs 3111 e 702.
2. Calcular SHA-256 dos downloads.
3. Implementar parser SDF V2000 restrito e falhar para entradas inesperadas.
4. Validar as fórmulas C13H17N3O4S e C2H6O.
5. Escrever PDB preservando as coordenadas com a precisão permitida pelo formato.

## Task 3: Criar automação de empacotamento

**Files:** `packmol/metamizole_ethanol_24A.inp`, `scripts/build_system.sh`

1. Definir tolerância 2,0 Å e formato PDB.
2. Fixar o soluto centralizado em 12, 12, 12 Å.
3. Inserir 143 etanóis dentro da célula periódica, com margem numérica de 0,1 Å em relação a `[0,24]³`.
4. Registrar toda saída textual em `logs/packmol.log`.

## Task 4: Converter e validar o resultado

**Files:** `scripts/validate_system.py`, `outputs/*`, `validation/*`

1. Acrescentar CRYST1 ao PDB final sem alterar coordenadas.
2. Produzir XYZ a partir do PDB final.
3. Verificar 1325 átomos, 1 soluto, 143 solventes e fórmulas por bloco.
4. Verificar limites cartesianos e caixa declarada.
5. Calcular a menor distância atômica intermolecular.
6. Comparar PDB e XYZ e produzir relatório JSON/Markdown.

## Task 5: Verificação final

**Files:** `README.md`, `diario.md`, `openspec/changes/prepare-neutral-metamizole-ethanol/tasks.md`

1. Executar o pipeline completo novamente.
2. Conferir código de saída e artefatos com checksums.
3. Revisar cada requisito OpenSpec contra evidência concreta.
4. Atualizar checkboxes e documentação apenas após a verificação.

## Auto-revisão

- Todos os requisitos da especificação possuem uma tarefa de implementação e validação.
- Não há placeholders de código ou decisões químicas pendentes.
- Os nomes de arquivos são consistentes entre design, tarefas e validação.
