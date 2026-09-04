#!/usr/bin/env python3
"""Finaliza e valida a gota não periódica de metamizol em etanol."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import argparse
import json
import math

from validate_system import add_check, file_hash, fingerprint_deviation, formula, parse_pdb


CENTER = (15.0, 15.0, 15.0)
RADIUS = 15.0
TOLERANCE = 2.0
NUMERIC_ALLOWANCE = 0.01


def write_xyz(path: Path, atoms) -> None:
    lines = [str(len(atoms)), 'nonperiodic ethanol droplet; center="15.0 15.0 15.0" radius=15.0 Angstrom']
    lines.extend(f"{a.element:<2s} {a.x:12.6f} {a.y:12.6f} {a.z:12.6f}" for a in atoms)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def direct_distance(atom_a, atom_b) -> float:
    return math.sqrt((atom_a.x - atom_b.x) ** 2 + (atom_a.y - atom_b.y) ** 2 + (atom_a.z - atom_b.z) ** 2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packed_pdb", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    packed = args.packed_pdb if args.packed_pdb.is_absolute() else root / args.packed_pdb
    final_pdb = root / "outputs/metamizole_ethanol_droplet_R15.pdb"
    final_xyz = root / "outputs/metamizole_ethanol_droplet_R15.xyz"
    final_pdb.write_text(packed.read_text(encoding="utf-8"), encoding="utf-8")
    _, atoms, box = parse_pdb(final_pdb)
    write_xyz(final_xyz, atoms)

    checks: list[dict] = []
    add_check(checks, "total_atoms", len(atoms) == 1352, len(atoms), 1352)
    add_check(checks, "nonperiodic_no_cryst1", box is None, box, None)

    molecules = defaultdict(list)
    for atom in atoms:
        molecules[atom.molecule].append(atom)
    mtz = [group for key, group in molecules.items() if key[2] == "MTZ"]
    etl = [group for key, group in molecules.items() if key[2] == "ETL"]
    add_check(checks, "molecule_count", len(molecules) == 147, len(molecules), 147)
    add_check(checks, "metamizole_count", len(mtz) == 1, len(mtz), 1)
    add_check(checks, "ethanol_count", len(etl) == 146, len(etl), 146)

    mtz_formulas = [formula(Counter(a.element for a in group)) for group in mtz]
    etl_formulas = [formula(Counter(a.element for a in group)) for group in etl]
    add_check(checks, "metamizole_formula", mtz_formulas == ["C13H17N3O4S"], mtz_formulas, ["C13H17N3O4S"])
    add_check(
        checks,
        "ethanol_formulas",
        len(etl_formulas) == 146 and set(etl_formulas) == {"C2H6O"},
        dict(Counter(etl_formulas)),
        {"C2H6O": 146},
    )

    barycenter = tuple(sum(getattr(a, axis) for a in mtz[0]) / len(mtz[0]) for axis in ("x", "y", "z")) if mtz else None
    centered = barycenter is not None and all(abs(value - target) <= 0.002 for value, target in zip(barycenter, CENTER))
    add_check(checks, "metamizole_barycenter_angstrom", centered, barycenter, CENTER)

    radial = []
    for atom in atoms:
        distance = math.sqrt((atom.x - CENTER[0]) ** 2 + (atom.y - CENTER[1]) ** 2 + (atom.z - CENTER[2]) ** 2)
        radial.append((distance, atom))
    max_radius, outermost = max(radial, key=lambda item: item[0])
    add_check(checks, "maximum_radius_angstrom", max_radius <= RADIUS + 0.002, max_radius, "<= 15.002")

    _, mtz_template, _ = parse_pdb(root / "inputs/prepared/metamizole_neutral.pdb")
    _, etl_template, _ = parse_pdb(root / "inputs/prepared/ethanol.pdb")
    mtz_deviation = fingerprint_deviation(mtz_template, mtz[0]) if mtz else float("inf")
    etl_deviation = max((fingerprint_deviation(etl_template, group) for group in etl), default=float("inf"))
    add_check(checks, "metamizole_rigid_geometry_max_deviation_angstrom", mtz_deviation <= 0.005, mtz_deviation, "<= 0.005")
    add_check(checks, "ethanol_rigid_geometry_max_deviation_angstrom", etl_deviation <= 0.005, etl_deviation, "<= 0.005")

    minimum = float("inf")
    minimum_pair = None
    for i, atom_a in enumerate(atoms):
        for atom_b in atoms[i + 1 :]:
            if atom_a.molecule == atom_b.molecule:
                continue
            distance = direct_distance(atom_a, atom_b)
            if distance < minimum:
                minimum = distance
                minimum_pair = {
                    "atom_1": [atom_a.serial, atom_a.name, list(atom_a.molecule)],
                    "atom_2": [atom_b.serial, atom_b.name, list(atom_b.molecule)],
                }
    add_check(
        checks,
        "minimum_direct_intermolecular_distance_angstrom",
        minimum >= TOLERANCE - NUMERIC_ALLOWANCE,
        minimum,
        ">= 1.99 (Packmol tolerance 2.00)",
    )

    xyz_lines = final_xyz.read_text(encoding="utf-8").splitlines()
    xyz_atoms = [(parts[0], *map(float, parts[1:])) for parts in (line.split() for line in xyz_lines[2:])]
    consistent = len(xyz_atoms) == len(atoms) and all(
        xa[0] == pa.element
        and abs(xa[1] - pa.x) < 1e-9
        and abs(xa[2] - pa.y) < 1e-9
        and abs(xa[3] - pa.z) < 1e-9
        for xa, pa in zip(xyz_atoms, atoms)
    )
    add_check(checks, "pdb_xyz_coordinate_consistency", consistent, consistent, True)

    volume = 4.0 * math.pi * RADIUS**3 / 3.0
    represented_density = 146 * 46.06844 / 6.02214076e23 / (volume * 1.0e-24)
    status = "pass" if all(check["pass"] for check in checks) else "fail"
    report = {
        "status": status,
        "system": {
            "geometry": "nonperiodic spherical droplet",
            "center_angstrom": CENTER,
            "requested_radius_angstrom": RADIUS,
            "packmol_solvent_constraint_radius_angstrom": 14.99,
            "solute": "neutral metamizole, PubChem CID 3111",
            "solvent": "ethanol, PubChem CID 702",
            "packmol_tolerance_angstrom": TOLERANCE,
            "ethanol_target_density_g_cm3": 0.7893,
            "ethanol_count_continuous": 145.865265059201,
            "ethanol_count_used": 146,
            "solvent_only_density_from_integer_count_g_cm3": represented_density,
        },
        "metamizole_barycenter_angstrom": barycenter,
        "maximum_observed_radius_angstrom": max_radius,
        "outermost_atom": [outermost.serial, outermost.name, list(outermost.molecule)],
        "minimum_direct_intermolecular_distance_angstrom": minimum,
        "minimum_pair": minimum_pair,
        "rigid_geometry_max_deviation_angstrom": {"metamizole": mtz_deviation, "ethanol": etl_deviation},
        "checks": checks,
        "files": {
            str(final_pdb.relative_to(root)): file_hash(final_pdb),
            str(final_xyz.relative_to(root)): file_hash(final_xyz),
            str(packed.relative_to(root)): file_hash(packed),
        },
    }
    validation_dir = root / "validation"
    json_path = validation_dir / "droplet_R15_report.json"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = [
        "# Validação da gota R15\n",
        f"- Status: **{status.upper()}**",
        f"- Átomos: {len(atoms)}",
        f"- Moléculas: {len(molecules)} (metamizol: {len(mtz)}; etanol: {len(etl)})",
        f"- Centro do metamizol: {barycenter} Å",
        f"- Raio máximo observado: {max_radius:.6f} Å",
        f"- Menor distância intermolecular direta: {minimum:.6f} Å",
        f"- Densidade representada pela contagem inteira: {represented_density:.6f} g cm⁻³",
        "\n## Checks\n",
    ]
    summary.extend(f"- [{'x' if c['pass'] else ' '}] {c['name']}: observado `{c['observed']}`; esperado `{c['expected']}`" for c in checks)
    (validation_dir / "droplet_R15_report.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
