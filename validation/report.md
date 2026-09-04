# Validação do sistema

- Status: **PASS**
- Átomos: 1325
- Moléculas: 144 (metamizol: 1; etanol: 143)
- Caixa: 24.000 × 24.000 × 24.000 Å
- Faixas: x=[0.099, 23.931], y=[0.1, 23.919], z=[0.1, 23.905] Å
- Menor distância intermolecular periódica: 2.198706 Å
- Densidade de etanol representada pela contagem inteira: 0.791325 g cm⁻³

## Checks

- [x] total_atoms: observado `1325`; esperado `1325`
- [x] box_lengths_angstrom: observado `(24.0, 24.0, 24.0)`; esperado `(24.0, 24.0, 24.0)`
- [x] coordinates_in_box: observado `{'x': [0.099, 23.931], 'y': [0.1, 23.919], 'z': [0.1, 23.905]}`; esperado `{'each_axis': [0.0, 24.0]}`
- [x] molecule_count: observado `144`; esperado `144`
- [x] metamizole_count: observado `1`; esperado `1`
- [x] ethanol_count: observado `143`; esperado `143`
- [x] metamizole_formula: observado `['C13H17N3O4S']`; esperado `['C13H17N3O4S']`
- [x] ethanol_formulas: observado `{'C2H6O': 143}`; esperado `{'C2H6O': 143}`
- [x] metamizole_barycenter_angstrom: observado `(12.0, 11.999894736842105, 12.000131578947368)`; esperado `[12.0, 12.0, 12.0]`
- [x] metamizole_rigid_geometry_max_deviation_angstrom: observado `0.0009896443829155999`; esperado `<= 0.005`
- [x] ethanol_rigid_geometry_max_deviation_angstrom: observado `0.001432231841018261`; esperado `<= 0.005`
- [x] minimum_periodic_intermolecular_distance_angstrom: observado `2.198706`; esperado `>= 1.99 (Packmol tolerance 2.00)`
- [x] pdb_xyz_coordinate_consistency: observado `True`; esperado `True`
