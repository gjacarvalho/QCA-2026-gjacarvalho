#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

packmol_bin="$project_root/tools/packmol-venv/bin/packmol"
python_bin="$project_root/tools/packmol-venv/bin/python"

if [[ ! -x "$packmol_bin" ]]; then
  echo "Erro: Packmol local ausente em $packmol_bin" >&2
  echo "Execute as instruções de instalação em README.md." >&2
  exit 2
fi
if [[ ! -s inputs/raw/metamizole_cid3111_3d.sdf || ! -s inputs/raw/ethanol_cid702_3d.sdf ]]; then
  echo "Erro: estruturas SDF ausentes. Execute scripts/build_system.sh para obtê-las." >&2
  exit 3
fi

mkdir -p inputs/prepared outputs validation logs
"$python_bin" scripts/prepare_structures.py --root "$project_root" > logs/prepare_structures_droplet_R15.log

packed_pdb="outputs/metamizole_ethanol_droplet_R15.packmol.pdb"
"$packmol_bin" -i packmol/metamizole_ethanol_droplet_R15.inp -o "$packed_pdb" > logs/packmol_droplet_R15.log 2>&1
"$python_bin" scripts/validate_droplet.py "$packed_pdb" --root "$project_root" > logs/validation_droplet_R15.log

echo "Gota gerada e validada."
echo "PDB: outputs/metamizole_ethanol_droplet_R15.pdb"
echo "XYZ: outputs/metamizole_ethanol_droplet_R15.xyz"
echo "Relatório: validation/droplet_R15_report.md"
