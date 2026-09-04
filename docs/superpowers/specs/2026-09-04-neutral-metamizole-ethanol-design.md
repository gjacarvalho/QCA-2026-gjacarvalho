# Design: caixa de metamizol neutro em etanol

## Objetivo

Produzir coordenadas iniciais verificáveis de uma molécula de metamizol neutro e 143 moléculas de etanol em uma caixa cúbica de 24 Å, usando Packmol.

## Design aprovado

O soluto será o metamizol neutro C13H17N3O4S (PubChem CID 3111), sem Na+ e sem água. O solvente será etanol all-atom C2H6O (PubChem CID 702). O cálculo usa densidade 0,7893 g cm⁻³ e fornece 142,6, arredondado a 143 moléculas.

As coordenadas de origem serão armazenadas, convertidas mecanicamente e verificadas. O Packmol usará tolerância de 2,0 Å, manterá o soluto no centro e acomodará os etanóis no cubo. A entrega inclui PDB, XYZ, log e relatórios, mas não inclui parâmetros de dinâmica molecular.

Este documento acompanha o detalhamento OpenSpec em `openspec/changes/prepare-neutral-metamizole-ethanol/`.
