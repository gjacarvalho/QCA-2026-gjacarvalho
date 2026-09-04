# Validação da gota R15

- Status: **PASS**
- Átomos: 1352
- Moléculas: 147 (metamizol: 1; etanol: 146)
- Centro do metamizol: (15.0, 14.999921052631578, 15.000131578947368) Å
- Raio máximo observado: 15.000363 Å
- Menor distância intermolecular direta: 2.171610 Å
- Densidade representada pela contagem inteira: 0.790029 g cm⁻³

## Checks

- [x] total_atoms: observado `1352`; esperado `1352`
- [x] nonperiodic_no_cryst1: observado `None`; esperado `None`
- [x] molecule_count: observado `147`; esperado `147`
- [x] metamizole_count: observado `1`; esperado `1`
- [x] ethanol_count: observado `146`; esperado `146`
- [x] metamizole_formula: observado `['C13H17N3O4S']`; esperado `['C13H17N3O4S']`
- [x] ethanol_formulas: observado `{'C2H6O': 146}`; esperado `{'C2H6O': 146}`
- [x] metamizole_barycenter_angstrom: observado `(15.0, 14.999921052631578, 15.000131578947368)`; esperado `(15.0, 15.0, 15.0)`
- [x] maximum_radius_angstrom: observado `15.00036272894759`; esperado `<= 15.002`
- [x] metamizole_rigid_geometry_max_deviation_angstrom: observado `0.0009896443829155999`; esperado `<= 0.005`
- [x] ethanol_rigid_geometry_max_deviation_angstrom: observado `0.0012669363435566794`; esperado `<= 0.005`
- [x] minimum_direct_intermolecular_distance_angstrom: observado `2.1716097715749942`; esperado `>= 1.99 (Packmol tolerance 2.00)`
- [x] pdb_xyz_coordinate_consistency: observado `True`; esperado `True`
