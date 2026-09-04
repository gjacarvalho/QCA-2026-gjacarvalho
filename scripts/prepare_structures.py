#!/usr/bin/env python3
"""Converte coordenadas SDF V2000 do PubChem em entradas PDB do Packmol."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import argparse
import json
import re


@dataclass(frozen=True)
class Atom:
    element: str
    x: float
    y: float
    z: float


def parse_sdf_v2000(path: Path) -> tuple[list[Atom], int, int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 5 or "V2000" not in lines[3]:
        raise ValueError(f"{path}: somente SDF V2000 é aceito")
    try:
        atom_count = int(lines[3][0:3])
        bond_count = int(lines[3][3:6])
    except ValueError as exc:
        raise ValueError(f"{path}: linha de contagens SDF inválida") from exc

    atoms: list[Atom] = []
    for index, line in enumerate(lines[4 : 4 + atom_count], start=1):
        try:
            atoms.append(
                Atom(
                    element=line[31:34].strip(),
                    x=float(line[0:10]),
                    y=float(line[10:20]),
                    z=float(line[20:30]),
                )
            )
        except (ValueError, IndexError) as exc:
            raise ValueError(f"{path}: átomo SDF inválido na posição {index}") from exc

    if len(atoms) != atom_count or any(not re.fullmatch(r"[A-Z][a-z]?", a.element) for a in atoms):
        raise ValueError(f"{path}: contagem ou símbolos de elementos inválidos")

    charge_total = 0
    for line in lines[4 + atom_count + bond_count :]:
        if line.startswith("M  CHG"):
            fields = line.split()
            nentries = int(fields[2])
            charges = fields[4 : 4 + 2 * nentries : 2]
            charge_total += sum(int(value) for value in charges)
        if line == "M  END":
            break
    return atoms, bond_count, charge_total


def formula_string(elements: Counter[str]) -> str:
    order = ["C", "H"] + sorted(e for e in elements if e not in {"C", "H"})
    return "".join(f"{element}{elements[element] if elements[element] != 1 else ''}" for element in order if elements[element])


def write_pdb(path: Path, atoms: list[Atom], residue: str) -> None:
    per_element: Counter[str] = Counter()
    lines = [f"REMARK  Generated mechanically from PubChem SDF; no charges or parameters assigned"]
    for serial, atom in enumerate(atoms, start=1):
        per_element[atom.element] += 1
        atom_name = f"{atom.element}{per_element[atom.element]}"[:4]
        lines.append(
            f"HETATM{serial:5d} {atom_name:^4s} {residue:>3s} A{1:4d}    "
            f"{atom.x:8.3f}{atom.y:8.3f}{atom.z:8.3f}{1.00:6.2f}{0.00:6.2f}          {atom.element:>2s}"
        )
    lines.extend(["TER", "END"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    definitions = [
        {
            "name": "metamizole",
            "cid": 3111,
            "input": root / "inputs/raw/metamizole_cid3111_3d.sdf",
            "output": root / "inputs/prepared/metamizole_neutral.pdb",
            "residue": "MTZ",
            "expected": Counter({"C": 13, "H": 17, "N": 3, "O": 4, "S": 1}),
        },
        {
            "name": "ethanol",
            "cid": 702,
            "input": root / "inputs/raw/ethanol_cid702_3d.sdf",
            "output": root / "inputs/prepared/ethanol.pdb",
            "residue": "ETL",
            "expected": Counter({"C": 2, "H": 6, "O": 1}),
        },
    ]

    report = {"status": "pass", "structures": []}
    for item in definitions:
        atoms, bonds, formal_charge = parse_sdf_v2000(item["input"])
        observed = Counter(atom.element for atom in atoms)
        if observed != item["expected"]:
            raise ValueError(
                f"{item['name']}: fórmula observada {formula_string(observed)}, "
                f"esperada {formula_string(item['expected'])}"
            )
        if formal_charge != 0:
            raise ValueError(f"{item['name']}: carga formal SDF {formal_charge}, esperada 0")
        item["output"].parent.mkdir(parents=True, exist_ok=True)
        write_pdb(item["output"], atoms, item["residue"])
        report["structures"].append(
            {
                "name": item["name"],
                "pubchem_cid": item["cid"],
                "formula": formula_string(observed),
                "atoms": len(atoms),
                "bonds_in_source_sdf": bonds,
                "formal_charge_in_source_sdf": formal_charge,
                "source": str(item["input"].relative_to(root)),
                "prepared": str(item["output"].relative_to(root)),
            }
        )

    report_path = root / "validation/input_structures.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
