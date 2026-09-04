# Diário do projeto: metamizol neutro em etanol

## 2026-09-04 — Solicitação inicial

Foi solicitado preparar, em Linux Kubuntu, um sistema molecular para simulação contendo uma molécula de dipirona solvatada em etanol em uma caixa cúbica de 24 Å, usando Packmol.

Também foi solicitado:

- empregar as metodologias dos repositórios Superpowers e OpenSpec;
- verificar arquivos e ferramentas antes da execução;
- esclarecer apenas decisões químicas essenciais ausentes;
- calcular e justificar o número de moléculas de etanol;
- criar especificação e plano antes da implementação;
- instalar ou configurar o Packmol se necessário;
- preparar entradas moleculares sem inventar coordenadas, parâmetros ou cargas;
- gerar entrada Packmol e script CLI reproduzível;
- executar e validar dimensões, composição, sobreposições e artefatos;
- preservar arquivos existentes e organizar todos os resultados.

## 2026-09-04 — Auditoria inicial

O diretório de trabalho estava vazio, exceto por metadados internos. Não havia repositório Git válido inicializado. Foram encontradas as ferramentas `gcc`, `make`, `git`, `curl`, `wget`, Python 3.14.6 e bibliotecas NumPy/SciPy. Não estavam disponíveis `packmol`, `gfortran`, Open Babel, RDKit, ASE ou MDAnalysis.

Foram consultadas as fontes oficiais:

- Superpowers: fluxo de brainstorming, escrita de planos e verificação antes de declarar conclusão;
- OpenSpec: sequência `proposal → specs → design → tasks → implement`;
- Packmol: opções oficiais de instalação e uso;
- PubChem: registros estruturais do metamizol e do etanol;
- NIST: densidade de referência do etanol.

## 2026-09-04 — Esclarecimento químico

Foi inicialmente proposto usar metamizol sódico anidro, mas o usuário corrigiu explicitamente a decisão: usar **metamizol neutro**.

Decisões aprovadas:

- soluto: metamizol neutro, fórmula C13H17N3O4S, PubChem CID 3111;
- solvente: etanol all-atom, fórmula C2H6O, PubChem CID 702;
- densidade-alvo para a contagem inicial: 0,7893 g cm⁻³;
- caixa: 24 × 24 × 24 Å³;
- saídas: PDB, XYZ, entrada Packmol, script CLI, logs e relatório de validação;
- escopo: coordenadas de empacotamento, sem topologia de dinâmica molecular, cargas ou parâmetros de campo de força.

A contagem inicial calculada foi:

```text
V = 24³ Å³ = 13 824 Å³ = 1,3824 × 10⁻²⁰ cm³
N = ρ V NA / M
  = 0,7893 × 1,3824 × 10⁻²⁰ × 6,02214076 × 10²³ / 46,06844
  ≈ 142,6
```

Adotou-se, portanto, **143 moléculas de etanol**, por arredondamento ao inteiro mais próximo. Não será subtraído um volume parcial do soluto, pois não há dado fornecido que permita fazê-lo sem uma hipótese adicional. A densidade final da solução deverá ser ajustada posteriormente por equilíbrio NPT.

## 2026-09-04 — Aprovação

Foi apresentado o fluxo `proposal → specs → design → tasks → implementação → verificação`, incluindo os critérios de validação e a organização de diretórios. O usuário aprovou a implementação e pediu a criação deste diário com registro das decisões e do trabalho realizado.

## Registro de execução

### Planejamento criado

Foram criados:

- `openspec/changes/prepare-neutral-metamizole-ethanol/proposal.md`;
- `openspec/changes/prepare-neutral-metamizole-ethanol/specs/molecular-packing/spec.md`;
- `openspec/changes/prepare-neutral-metamizole-ethanol/design.md`;
- `openspec/changes/prepare-neutral-metamizole-ethanol/tasks.md`;
- `docs/superpowers/specs/2026-09-04-neutral-metamizole-ethanol-design.md`;
- `docs/superpowers/plans/2026-09-04-neutral-metamizole-ethanol.md`.

O CLI OpenSpec não foi instalado, porque o ambiente não possui a versão mínima de Node.js indicada pelo projeto. Os artefatos foram criados diretamente de acordo com o schema `spec-driven`, sem depender do CLI.

### Packmol

Foi criado um ambiente virtual local e instalada a distribuição oficial disponível no PyPI:

```bash
python3 -m venv tools/packmol-venv
tools/packmol-venv/bin/python -m pip install packmol
```

Versão instalada: Packmol 21.2.3. A primeira tentativa de instalação, dentro do sandbox sem rede, falhou por resolução DNS. Após autorização explícita de acesso externo, a instalação foi concluída. Nenhum pacote de sistema foi alterado.

### Estruturas de entrada

Foram executados os downloads:

```bash
curl -fL --retry 3 -o inputs/raw/metamizole_cid3111_3d.sdf \
  'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/3111/record/SDF?record_type=3d'
curl -fL --retry 3 -o inputs/raw/ethanol_cid702_3d.sdf \
  'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/702/record/SDF?record_type=3d'
```

Checksums e resultados da inspeção:

```text
7fcf65696c3798dd4dec4258ba6de8849a3ce108229447b914f909c5abc707b8  metamizole_cid3111_3d.sdf
302540b4e75e32468e7fed274a1104edc33bc30e06127f6c43918462ece3060b  ethanol_cid702_3d.sdf
metamizol: 38 átomos, 39 ligações no SDF, fórmula C13H17N3O4S, carga formal total 0
etanol: 9 átomos, 8 ligações no SDF, fórmula C2H6O, carga formal total 0
```

O script `scripts/prepare_structures.py` copia mecanicamente elementos e coordenadas do SDF para PDB. Propriedades de cargas parciais presentes nos metadados PubChem não são utilizadas. As ligações também não são transferidas, pois a topologia está fora do escopo.

### Entrada e execução do Packmol

O arquivo `packmol/metamizole_ethanol_24A.inp` usa:

- tolerância atômica de 2,0 Å;
- semente fixa `20260904`;
- caixa periódica de 24 × 24 × 24 Å;
- metamizol com baricentro fixo em (12, 12, 12) Å;
- 143 etanóis;
- numeração sequencial de resíduos;
- ausência de conectividade/topologia adicionada.

O pipeline é executado por:

```bash
scripts/build_system.sh
```

Na primeira execução, o Packmol concluiu o empacotamento, mas o validador encontrou coordenadas até 0,094 Å além da célula primária, consequência de moléculas próximas às faces e da tolerância numérica da restrição. Não foi aplicada uma correção posterior de coordenadas. A entrada foi refinada com `precision 0.001` e uma margem interna explícita de 0,1 Å para o solvente, mantendo simultaneamente o cálculo periódico das distâncias.

Na execução seguinte, o Packmol informou sucesso, 1325 átomos, 144 moléculas, violação máxima de distância igual a zero e violação máxima de restrições de 0,00095006 Å.

### Resultado de validação

O relatório `validation/report.md` registrou PASS para:

- 1325 átomos;
- 144 moléculas: 1 metamizol e 143 etanóis;
- fórmulas moleculares esperadas;
- caixa CRYST1 de 24 × 24 × 24 Å;
- coordenadas entre 0,099 e 23,931 Å em x, 0,100 e 23,919 Å em y e 0,100 e 23,905 Å em z;
- menor distância intermolecular periódica de 2,198706 Å;
- identidade entre as coordenadas PDB e XYZ.

A contagem inteira de 143 etanóis representa 0,791325 g cm⁻³ no volume total, diferença decorrente do arredondamento de 142,634 para 143.

Foi acrescentada uma validação geométrica independente para confirmar que o Packmol somente aplicou transformações rígidas às moléculas. Os desvios máximos das assinaturas de distâncias internas, limitados pela precisão de três casas decimais do PDB, foram 0,000990 Å para o metamizol e 0,001432 Å para o etanol. O baricentro observado do metamizol foi (12,000000; 11,999895; 12,000132) Å.

Durante a primeira tentativa da verificação final, a compilação Python identificou um erro de sintaxe recém-introduzido na expressão que calcula o desvio geométrico. Como o pipeline parou antes de regenerar o relatório, nenhum resultado antigo foi tratado como evidência nova. A expressão foi corrigida e todo o pipeline foi executado novamente com código de saída zero e status PASS.

Checksums finais das coordenadas reproduzidas:

```text
e2cc0d3d2c3c85c30664b32f76b36ece61fadb370951b823cec780aac07c50c3  outputs/metamizole_ethanol_24A.pdb
c3991adad8a238ed5b59ff5a88d74ec1cc889b6fb03b46cee7923f7db61fe5c9  outputs/metamizole_ethanol_24A.xyz
```

### Limitações e próximos passos

- O volume parcial do metamizol não foi descontado da contagem de solvente.
- A configuração não possui campo de força, cargas nem topologia.
- O estado de protonação/tautomeria deve ser confirmado para o pH e modelo físico pretendidos.
- Deve-se escolher um motor e campo de força compatíveis, parametrizar o soluto e o etanol, minimizar energia e realizar equilíbrio NVT/NPT antes de produção.
- A densidade final deve ser medida após equilíbrio NPT; o empacotamento não é uma previsão termodinâmica da solução.

## 2026-09-04 — Gota esférica de etanol, raio 15 Å

O usuário solicitou uma nova geometria: gota com raio de 15 Å, metamizol no centro e solvente ao redor. Pelo contexto aprovado, “dipirona” foi mantida como metamizol neutro C13H17N3O4S e “solvente” como etanol C2H6O. A caixa cúbica anterior foi preservada.

A gota foi definida como sistema finito e não periódico, centrado em (15, 15, 15) Å. A contagem foi recalculada para o volume esférico:

```text
V = 4π(15 Å)³/3 = 14 137,166941 Å³
N = 0,7893 × 14 137,166941 × 10⁻²⁴ × NA / 46,06844
N = 145,865265 ≈ 146 etanóis
```

A densidade de solvente representada pela contagem inteira é 0,790029 g cm⁻³. Novamente, não foi estimado nem subtraído o volume parcial do soluto.

Foram adicionados uma nova mudança OpenSpec, plano Superpowers, entrada Packmol, script CLI e validador próprios. A restrição do solvente usa uma esfera de 14,99 Å, deixando margem numérica de 0,01 Å dentro do raio solicitado de 15 Å. Não há PBC nem registro CRYST1.

Comando de execução:

```bash
scripts/build_droplet.sh
```

Na primeira execução, o Packmol 21.2.3 informou sucesso para 1352 átomos e 147 moléculas, com violação máxima da distância-alvo igual a zero e violação máxima das restrições de 0,00099403 Å. O relatório `validation/droplet_R15_report.md` apresentou PASS em 13 verificações:

- 1 metamizol e 146 etanóis;
- fórmulas corretas;
- ausência de periodicidade/CRYST1;
- baricentro do metamizol em (15,000000; 14,999921; 15,000132) Å;
- raio máximo observado de 15,000363 Å, dentro da tolerância de escrita PDB;
- menor distância intermolecular direta de 2,171610 Å;
- desvios máximos de geometria rígida de 0,000990 Å para metamizol e 0,001267 Å para etanol;
- coordenadas idênticas entre PDB e XYZ.

A gota é uma configuração inicial finita com superfície livre. A simulação posterior precisará definir como tratar evaporação/confinamento, além de parametrização, minimização e equilíbrio.

A execução foi repetida com a mesma semente. Todos os valores de validação e os checksums permaneceram idênticos:

```text
0a87d4a5a9a60e85b760858e9a57b5acc70fc065699aed45e7b1ec4896dcd73a  outputs/metamizole_ethanol_droplet_R15.pdb
6c4a83777f6b8660194d0e002e8a530665bbdcde837e402b348ce69a168895fd  outputs/metamizole_ethanol_droplet_R15.xyz
```

## 2026-09-04 — Preparação para publicação no GitHub

O usuário solicitou publicar todo o projeto em `https://github.com/gjacarvalho/QCA-2026-gjacarvalho`, ampliar o README com o estado atual e preservar os prompts utilizados.

O repositório remoto foi inspecionado antes de qualquer escrita. A branch padrão era `main`, com apenas um commit inicial e um README contendo o título do repositório. O novo `README.md` documenta os dois sistemas, cálculos, validações, reprodução, estrutura de diretórios, limitações e próximos passos. O arquivo `PROMPTS.md` preserva textualmente os cinco prompts do usuário até esta etapa.

O ambiente virtual local, caches Python e diretórios internos da ferramenta foram adicionados ao `.gitignore`; entradas moleculares, scripts, especificações, planos, saídas, logs e relatórios permanecem incluídos na publicação. Antes do commit foram executados `git diff --check`, compilação dos scripts Python, validação sintática dos scripts shell e leitura dos dois relatórios JSON, ambos com 13/13 checks PASS.
