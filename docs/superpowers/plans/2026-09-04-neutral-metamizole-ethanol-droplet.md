# Plano de execução: gota de metamizol neutro em etanol

## Resultado esperado

Uma gota molecular finita com raio máximo de 15 Å, uma molécula de metamizol neutro central e 146 moléculas de etanol, gerada sem alterar a caixa cúbica anterior.

## Task 1: Entrada esférica

**File:** `packmol/metamizole_ethanol_droplet_R15.inp`

1. Definir tolerância 2,0 Å, precisão 0,001 e semente fixa.
2. Fixar MTZ em (15,15,15) Å.
3. Restringir 146 ETL à esfera com margem numérica de 0,01 Å.
4. Não habilitar PBC nem CRYST1.

## Task 2: Validação

**File:** `scripts/validate_droplet.py`

1. Verificar 1352 átomos, 147 resíduos, fórmulas e contagens.
2. Verificar baricentro do MTZ.
3. Verificar raio máximo de todos os átomos.
4. Verificar ausência de CRYST1.
5. Verificar menor distância cartesiana intermolecular.
6. Verificar rigidez contra as entradas e consistência PDB/XYZ.

## Task 3: Automação e execução

**File:** `scripts/build_droplet.sh`

1. Verificar ferramenta e entradas.
2. Preparar estruturas a partir dos SDFs preservados.
3. Executar Packmol e capturar log.
4. Executar o validador e propagar falhas.

## Task 4: Verificação final

1. Compilar os scripts Python e validar o shell.
2. Executar o pipeline duas vezes com semente fixa.
3. Confirmar relatório PASS e checksums estáveis.
4. Atualizar tarefas e diário somente após evidência fresca.
