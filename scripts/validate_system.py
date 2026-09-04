#!/usr/bin/env python3
"""Finaliza PDB/XYZ e valida composição, caixa e contatos periódicos."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import argparse
import json
import math


BOX = (24.0, 24.0, 24.0)
TOLERANCE = 2.0
NUMERIC_ALLOWANCE = 0.01


@dataclass(frozen=True)
class PDBAtom:
    serial: int
    name: str
    residue: str
    chain: str
    resid: int
    x: float
    y: float
    z: float
    element: str

    @property
    def molecule(self) -> tuple[str, int, str]:
        return self.chain, self.resid, self.residue


def parse_pdb(path: Path) -> tuple[list[str], list[PDBAtom], tuple[float, float, float] | None]:
    lines = path.read_text(encoding="utf-8").splitlines()
    atoms: list[PDBAtom] = []
    box = None
    for line in lines:
        if line.startswith("CRYST1"):
            box = (float(line[6:15]), float(line[15:24]), float(line[24:33]))
        if line.startswith(("ATOM  ", "HETATM")):
            atoms.append(
                PDBAtom(
                    serial=int(line[6:11]),
                    name=line[12:16].strip(),
                    residue=line[17:20].strip(),
                    chain=line[21:22].strip(),
                    resid=int(line[22:26]),
                    x=float(line[30:38]),
                    y=float(line[38:46]),
                    z=float(line[46:54]),
                    element=line[76:78].strip(),
                )
            )
    return lines, atoms, box


def add_exact_cryst1(source: Path, target: Path) -> None:
    lines = source.read_text(encoding="utf-8").splitlines()
    lines = [line for line in lines if not line.startswith("CRYST1")]
    cryst1 = "CRYST1   24.000   24.000   24.000  90.00  90.00  90.00 P 1           1"
    insertion = 1 if lines and lines[0].startswith(("HEADER", "TITLE", "REMARK")) else 0
    lines.insert(insertion, cryst1)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_xyz(path: Path, atoms: list[PDBAtom]) -> None:
    lines = [str(len(atoms)), 'metamizole + 143 ethanol; box="24.0 24.0 24.0" Angstrom']
    lines.extend(f"{a.element:<2s} {a.x:12.6f} {a.y:12.6f} {a.z:12.6f}" for a in atoms)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def periodic_distance(a: PDBAtom, b: PDBAtom) -> float:
    diffs = []
    for av, bv, length in zip((a.x, a.y, a.z), (b.x, b.y, b.z), BOX):
        delta = av - bv
        delta -= round(delta / length) * length
        diffs.append(delta)
    return math.sqrt(sum(delta * delta for delta in diffs))


def distance_fingerprint(atoms: list[PDBAtom]) -> list[float]:
    distances = []
    for i, atom_a in enumerate(atoms):
        for atom_b in atoms[i + 1 :]:
            distances.append(
                math.sqrt((atom_a.x - atom_b.x) ** 2 + (atom_a.y - atom_b.y) ** 2 + (atom_a.z - atom_b.z) ** 2)
            )
    return sorted(distances)


def fingerprint_deviation(reference: list[PDBAtom], observed: list[PDBAtom]) -> float:
    ref = distance_fingerprint(reference)
    obs = distance_fingerprint(observed)
    if len(ref) != len(obs):
        return float("inf")
    return max((abs(a - b) for a, b in zip(ref, obs)), default=0.0)


def formula(counter: Counter[str]) -> str:
    order = ["C", "H"] + sorted(e for e in counter if e not in {"C", "H"})
    return "".join(f"{e}{counter[e] if counter[e] != 1 else ''}" for e in order if counter[e])


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_check(checks: list[dict], name: str, passed: bool, observed, expected) -> None:
    checks.append({"name": name, "pass": bool(passed), "observed": observed, "expected": expected})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packed_pdb", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    packed = args.packed_pdb if args.packed_pdb.is_absolute() else root / args.packed_pdb
    final_pdb = root / "outputs/metamizole_ethanol_24A.pdb"
    final_xyz = root / "outputs/metamizole_ethanol_24A.xyz"
    add_exact_cryst1(packed, final_pdb)
    _, atoms, box = parse_pdb(final_pdb)
    write_xyz(final_xyz, atoms)

    checks: list[dict] = []
    add_check(checks, "total_atoms", len(atoms) == 1325, len(atoms), 1325)
    add_check(checks, "box_lengths_angstrom", box == BOX, box, BOX)
    in_bounds = all(-0.001 <= v <= 24.001 for atom in atoms for v in (atom.x, atom.y, atom.z))
    coordinate_ranges = {
        axis: [min(getattr(a, axis) for a in atoms), max(getattr(a, axis) for a in atoms)]
        for axis in ("x", "y", "z")
    }
    add_check(checks, "coordinates_in_box", in_bounds, coordinate_ranges, {"each_axis": [0.0, 24.0]})

    molecules: dict[tuple[str, int, str], list[PDBAtom]] = defaultdict(list)
    for atom in atoms:
        molecules[atom.molecule].append(atom)
    mtz = [group for key, group in molecules.items() if key[2] == "MTZ"]
    etl = [group for key, group in molecules.items() if key[2] == "ETL"]
    add_check(checks, "molecule_count", len(molecules) == 144, len(molecules), 144)
    add_check(checks, "metamizole_count", len(mtz) == 1, len(mtz), 1)
    add_check(checks, "ethanol_count", len(etl) == 143, len(etl), 143)

    mtz_formulas = [formula(Counter(a.element for a in group)) for group in mtz]
    etl_formulas = [formula(Counter(a.element for a in group)) for group in etl]
    add_check(checks, "metamizole_formula", mtz_formulas == ["C13H17N3O4S"], mtz_formulas, ["C13H17N3O4S"])
    add_check(
        checks,
        "ethanol_formulas",
        len(etl_formulas) == 143 and set(etl_formulas) == {"C2H6O"},
        dict(Counter(etl_formulas)),
        {"C2H6O": 143},
    )

    solute_barycenter = tuple(sum(getattr(atom, axis) for atom in mtz[0]) / len(mtz[0]) for axis in ("x", "y", "z")) if mtz else None
    centered = solute_barycenter is not None and all(abs(value - 12.0) <= 0.002 for value in solute_barycenter)
    add_check(checks, "metamizole_barycenter_angstrom", centered, solute_barycenter, [12.0, 12.0, 12.0])

    _, mtz_template, _ = parse_pdb(root / "inputs/prepared/metamizole_neutral.pdb")
    _, etl_template, _ = parse_pdb(root / "inputs/prepared/ethanol.pdb")
    mtz_geometry_deviation = fingerprint_deviation(mtz_template, mtz[0]) if mtz else float("inf")
    etl_geometry_deviations = [fingerprint_deviation(etl_template, group) for group in etl]
    max_etl_geometry_deviation = max(etl_geometry_deviations, default=float("inf"))
    add_check(
        checks,
        "metamizole_rigid_geometry_max_deviation_angstrom",
        mtz_geometry_deviation <= 0.005,
        mtz_geometry_deviation,
        "<= 0.005",
    )
    add_check(
        checks,
        "ethanol_rigid_geometry_max_deviation_angstrom",
        max_etl_geometry_deviation <= 0.005,
        max_etl_geometry_deviation,
        "<= 0.005",
    )

    minimum = float("inf")
    minimum_pair = None
    for i, atom_a in enumerate(atoms):
        for atom_b in atoms[i + 1 :]:
            if atom_a.molecule == atom_b.molecule:
                continue
            distance = periodic_distance(atom_a, atom_b)
            if distance < minimum:
                minimum = distance
                minimum_pair = {
                    "atom_1": [atom_a.serial, atom_a.name, list(atom_a.molecule)],
                    "atom_2": [atom_b.serial, atom_b.name, list(atom_b.molecule)],
                }
    add_check(
        checks,
        "minimum_periodic_intermolecular_distance_angstrom",
        minimum >= TOLERANCE - NUMERIC_ALLOWANCE,
        round(minimum, 6),
        f">= {TOLERANCE - NUMERIC_ALLOWANCE:.2f} (Packmol tolerance {TOLERANCE:.2f})",
    )

    xyz_lines = final_xyz.read_text(encoding="utf-8").splitlines()
    xyz_atoms = []
    for line in xyz_lines[2:]:
        element, x, y, z = line.split()
        xyz_atoms.append((element, float(x), float(y), float(z)))
    same_coordinates = len(xyz_atoms) == len(atoms) and all(
        xa[0] == pa.element
        and abs(xa[1] - pa.x) < 1e-9
        and abs(xa[2] - pa.y) < 1e-9
        and abs(xa[3] - pa.z) < 1e-9
        for xa, pa in zip(xyz_atoms, atoms)
    )
    add_check(checks, "pdb_xyz_coordinate_consistency", same_coordinates, same_coordinates, True)

    solvent_density = 143 * 46.06844 / 6.02214076e23 / (24.0**3 * 1.0e-24)
    status = "pass" if all(check["pass"] for check in checks) else "fail"
    report = {
        "status": status,
        "system": {
            "solute": "neutral metamizole, PubChem CID 3111",
            "solvent": "ethanol, PubChem CID 702",
            "box_angstrom": BOX,
            "packmol_tolerance_angstrom": TOLERANCE,
            "ethanol_target_density_g_cm3": 0.7893,
            "ethanol_count_continuous": 142.63405338366834,
            "ethanol_count_used": 143,
            "solvent_only_density_from_integer_count_g_cm3": solvent_density,
        },
        "coordinate_ranges_angstrom": coordinate_ranges,
        "metamizole_barycenter_angstrom": solute_barycenter,
        "rigid_geometry_max_deviation_angstrom": {
            "metamizole": mtz_geometry_deviation,
            "ethanol": max_etl_geometry_deviation,
        },
        "minimum_periodic_intermolecular_distance_angstrom": minimum,
        "minimum_pair": minimum_pair,
        "checks": checks,
        "files": {
            str(final_pdb.relative_to(root)): file_hash(final_pdb),
            str(final_xyz.relative_to(root)): file_hash(final_xyz),
            str(packed.relative_to(root)): file_hash(packed),
        },
    }
    validation_dir = root / "validation"
    validation_dir.mkdir(parents=True, exist_ok=True)
    json_path = validation_dir / "report.json"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = [
        f"# Validação do sistema\n",
        f"- Status: **{status.upper()}**",
        f"- Átomos: {len(atoms)}",
        f"- Moléculas: {len(molecules)} (metamizol: {len(mtz)}; etanol: {len(etl)})",
        f"- Caixa: {box[0]:.3f} × {box[1]:.3f} × {box[2]:.3f} Å" if box else "- Caixa: ausente",
        f"- Faixas: x={coordinate_ranges['x']}, y={coordinate_ranges['y']}, z={coordinate_ranges['z']} Å",
        f"- Menor distância intermolecular periódica: {minimum:.6f} Å",
        f"- Densidade de etanol representada pela contagem inteira: {solvent_density:.6f} g cm⁻³",
        "\n## Checks\n",
    ]
    summary.extend(f"- [{'x' if c['pass'] else ' '}] {c['name']}: observado `{c['observed']}`; esperado `{c['expected']}`" for c in checks)
    (validation_dir / "report.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
