# QCA 2026 — metamizol neutro solvatado em etanol com Packmol

Este repositório registra a preparação reproduzível de duas configurações moleculares contendo uma molécula de metamizol neutro em etanol:

1. uma caixa periódica cúbica de 24 Å de lado;
2. uma gota esférica não periódica de raio 15 Å.

O trabalho foi planejado com o fluxo `proposal → specs → design → tasks → implementação → verificação`, seguindo as metodologias [OpenSpec](https://github.com/Fission-AI/openspec) e [Superpowers](https://github.com/obra/superpowers). O empacotamento foi realizado com [Packmol](https://github.com/m3g/packmol) 21.2.3.

## Estado atual

| Sistema | Geometria | Composição | Átomos | Distância intermolecular mínima | Validação |
|---|---:|---:|---:|---:|---:|
| Caixa periódica | 24 × 24 × 24 Å³ | 1 metamizol + 143 etanóis | 1325 | 2,198706 Å, imagem mínima | 13/13 PASS |
| Gota não periódica | raio 15 Å | 1 metamizol + 146 etanóis | 1352 | 2,171610 Å, direta | 13/13 PASS |

As duas execuções são determinísticas nas condições registradas e foram repetidas com checksums estáveis. A caixa original permaneceu inalterada após a criação da gota.

## Decisões químicas

- Soluto: metamizol neutro, C13H17N3O4S, [PubChem CID 3111](https://pubchem.ncbi.nlm.nih.gov/compound/Metamizole).
- Solvente: etanol all-atom, C2H6O, [PubChem CID 702](https://pubchem.ncbi.nlm.nih.gov/compound/702).
- Densidade-alvo usada para contagem: 0,7893 g cm⁻³.
- Não foram atribuídos campo de força, cargas, tipos atômicos ou topologia.
- Coordenadas moleculares: conformeros 3D SDF obtidos diretamente do PubChem.
- Tolerância Packmol: 2,0 Å.

Os SDFs originais e seus checksums estão documentados em [`inputs/raw/SOURCES.md`](inputs/raw/SOURCES.md). Metadados de cargas parciais eventualmente presentes nos registros PubChem não são transferidos para as entradas PDB.

## Cálculo das moléculas de etanol

### Caixa cúbica

```text
V = 24³ Å³ = 13 824 Å³ = 1,3824 × 10⁻²⁰ cm³
N = ρ V NA / M
N = 0,7893 × 1,3824 × 10⁻²⁰ × 6,02214076 × 10²³ / 46,06844
N = 142,634 ≈ 143 etanóis
```

A contagem inteira representa 0,791325 g cm⁻³ no volume total da caixa.

### Gota esférica

```text
V = 4π(15 Å)³/3 = 14 137,166941 Å³
N = 0,7893 × 14 137,166941 × 10⁻²⁴ × NA / 46,06844
N = 145,865 ≈ 146 etanóis
```

A contagem inteira representa 0,790029 g cm⁻³ no volume integral da esfera. Em ambos os cálculos, o volume parcial do soluto não foi subtraído porque isso exigiria um dado físico adicional não fornecido.

## Instalação

O Packmol é instalado em ambiente virtual local, sem alterar os pacotes do sistema Kubuntu:

```bash
python3 -m venv tools/packmol-venv
tools/packmol-venv/bin/python -m pip install packmol==21.2.3
chmod +x scripts/build_system.sh scripts/build_droplet.sh
```

O ambiente `tools/packmol-venv/` não é versionado. As entradas, scripts, especificações, resultados e relatórios necessários são versionados.

## Reprodução

### Caixa periódica de 24 Å

```bash
scripts/build_system.sh
```

Principais resultados:

- [`outputs/metamizole_ethanol_24A.pdb`](outputs/metamizole_ethanol_24A.pdb)
- [`outputs/metamizole_ethanol_24A.xyz`](outputs/metamizole_ethanol_24A.xyz)
- [`validation/report.md`](validation/report.md)
- [`validation/report.json`](validation/report.json)
- [`logs/packmol.log`](logs/packmol.log)

### Gota não periódica de raio 15 Å

```bash
scripts/build_droplet.sh
```

Principais resultados:

- [`outputs/metamizole_ethanol_droplet_R15.pdb`](outputs/metamizole_ethanol_droplet_R15.pdb)
- [`outputs/metamizole_ethanol_droplet_R15.xyz`](outputs/metamizole_ethanol_droplet_R15.xyz)
- [`validation/droplet_R15_report.md`](validation/droplet_R15_report.md)
- [`validation/droplet_R15_report.json`](validation/droplet_R15_report.json)
- [`logs/packmol_droplet_R15.log`](logs/packmol_droplet_R15.log)

## Evidências de validação

### Caixa

- 1 metamizol C13H17N3O4S e 143 etanóis C2H6O.
- Registro CRYST1 de 24 × 24 × 24 Å e ângulos de 90°.
- Coordenadas dentro da célula primária.
- Baricentro do metamizol em aproximadamente (12,12,12) Å.
- Menor distância intermolecular periódica: 2,198706 Å.
- Geometrias internas preservadas dentro de 0,005 Å.
- Coordenadas PDB e XYZ consistentes.

### Gota

- 1 metamizol C13H17N3O4S e 146 etanóis C2H6O.
- Sem PBC e sem registro CRYST1.
- Baricentro do metamizol em aproximadamente (15,15,15) Å.
- Raio máximo observado: 15,000363 Å, dentro da precisão de escrita PDB.
- Menor distância intermolecular direta: 2,171610 Å.
- Geometrias internas preservadas dentro de 0,005 Å.
- Coordenadas PDB e XYZ consistentes.

Checksums das coordenadas finais:

```text
e2cc0d3d2c3c85c30664b32f76b36ece61fadb370951b823cec780aac07c50c3  outputs/metamizole_ethanol_24A.pdb
c3991adad8a238ed5b59ff5a88d74ec1cc889b6fb03b46cee7923f7db61fe5c9  outputs/metamizole_ethanol_24A.xyz
0a87d4a5a9a60e85b760858e9a57b5acc70fc065699aed45e7b1ec4896dcd73a  outputs/metamizole_ethanol_droplet_R15.pdb
6c4a83777f6b8660194d0e002e8a530665bbdcde837e402b348ce69a168895fd  outputs/metamizole_ethanol_droplet_R15.xyz
```

## Organização do repositório

```text
docs/superpowers/   designs e planos de execução
inputs/raw/         SDFs originais e proveniência
inputs/prepared/    PDBs moleculares usados pelo Packmol
logs/               saídas integrais das execuções
openspec/           proposals, specs, designs e tasks
outputs/            PDBs e XYZ finais
packmol/            arquivos de entrada do Packmol
scripts/            preparação, execução e validação
validation/         relatórios Markdown e JSON
diario.md           histórico detalhado de decisões e resultados
PROMPTS.md          prompts do usuário preservados textualmente
```

## Prompts utilizados

Os prompts completos, em ordem cronológica e sem paráfrases, estão em [`PROMPTS.md`](PROMPTS.md). Resumo:

1. Preparar metamizol/dipirona em etanol em caixa de 24 Å, usando Packmol, Superpowers e OpenSpec.
2. Corrigir a identidade química para metamizol neutro e apresentar o fluxo de trabalho.
3. Criar `diario.md`, registrar a conversa e implementar o plano.
4. Criar uma gota de raio 15 Å com o soluto central e etanol ao redor.
5. Publicar o estado atual e os prompts neste repositório GitHub.

## Limitações e próximos passos

Estes arquivos são coordenadas iniciais de empacotamento, não sistemas prontos para dinâmica molecular. Antes de produção ainda é necessário:

1. escolher o motor de dinâmica molecular e o campo de força;
2. revisar protonação e tautomeria para as condições físicas pretendidas;
3. gerar cargas, tipos atômicos, ligações e topologia com metodologia apropriada;
4. minimizar energia e equilibrar temperatura/densidade;
5. para a gota, definir tratamento de evaporação, confinamento ou ambiente externo;
6. avaliar a densidade final após equilíbrio — preferencialmente NPT para o sistema periódico.

## Referências

- [Packmol — repositório oficial](https://github.com/m3g/packmol)
- [Packmol — guia oficial](https://m3g.github.io/packmol/userguide.shtml)
- [Metamizol — PubChem CID 3111](https://pubchem.ncbi.nlm.nih.gov/compound/Metamizole)
- [Etanol — PubChem CID 702](https://pubchem.ncbi.nlm.nih.gov/compound/702)
- [OpenSpec](https://github.com/Fission-AI/openspec)
- [Superpowers](https://github.com/obra/superpowers)

O histórico detalhado, incluindo tentativas que falharam, correções e decisões, está em [`diario.md`](diario.md).
