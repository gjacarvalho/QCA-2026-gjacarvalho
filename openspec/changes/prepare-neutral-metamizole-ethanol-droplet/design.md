# Design: gota de etanol de raio 15 Å

## Context

O sistema cúbico anterior, as estruturas PubChem preparadas e o Packmol 21.2.3 serão preservados e reutilizados. A gota será um novo artefato independente.

## Cálculo do solvente

```text
V = 4πr³/3 = 4π(15 Å)³/3 = 14 137,166941 Å³
N = 0,7893 × (14 137,166941 × 10⁻²⁴) × NA / 46,06844
N = 145,865265 ≈ 146 moléculas de etanol
```

A contagem inteira corresponde a 0,790029 g cm⁻³ se referida ao volume integral da esfera. Não será subtraído volume parcial do soluto sem dado físico específico.

## Geometry

- centro cartesiano: (15, 15, 15) Å;
- raio solicitado: 15 Å;
- restrição Packmol do solvente: esfera de raio 14,99 Å, margem de 0,01 Å para tolerância numérica;
- soluto: baricentro fixo no centro, sem rotação;
- sistema não periódico, sem CRYST1;
- tolerância intermolecular: 2,0 Å;
- semente fixa para reprodutibilidade.

## Outputs

- `outputs/metamizole_ethanol_droplet_R15.pdb`;
- `outputs/metamizole_ethanol_droplet_R15.xyz`;
- `validation/droplet_R15_report.json`;
- `validation/droplet_R15_report.md`;
- `logs/packmol_droplet_R15.log`.

## Risks / Limitations

- Uma gota finita possui superfície e não representa diretamente etanol bulk periódico.
- O empacotamento não substitui minimização e equilíbrio.
- Evaporação ou manutenção da gota dependerá do protocolo de simulação posterior.
- Não são atribuídos campo de força, cargas ou topologia.

## Open Questions

Nenhuma questão bloqueante: “o solvente” foi interpretado como o etanol já aprovado e “dipirona” como o metamizol neutro já definido.
