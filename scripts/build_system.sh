#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

packmol_bin="$project_root/tools/packmol-venv/bin/packmol"
python_bin="$project_root/tools/packmol-venv/bin/python"

if [[ ! -x "$packmol_bin" ]]; then
  echo "Erro: Packmol local ausente em $packmol_bin" >&2
  echo "Crie o ambiente e instale com:" >&2
  echo "  python3 -m venv tools/packmol-venv" >&2
  echo "  tools/packmol-venv/bin/python -m pip install packmol==21.2.3" >&2
  exit 2
fi

mkdir -p inputs/raw inputs/prepared outputs validation logs

if [[ ! -s inputs/raw/metamizole_cid3111_3d.sdf ]]; then
  curl -fL --retry 3 -o inputs/raw/metamizole_cid3111_3d.sdf \
    'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/3111/record/SDF?record_type=3d'
fi
if [[ ! -s inputs/raw/ethanol_cid702_3d.sdf ]]; then
  curl -fL --retry 3 -o inputs/raw/ethanol_cid702_3d.sdf \
    'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/702/record/SDF?record_type=3d'
fi

{
  "$python_bin" -c 'from importlib.metadata import version; print("packmol", version("packmol"))'
  "$python_bin" --version
  sha256sum inputs/raw/metamizole_cid3111_3d.sdf inputs/raw/ethanol_cid702_3d.sdf
} > logs/tool_versions_and_inputs.txt

"$python_bin" scripts/prepare_structures.py --root "$project_root" > logs/prepare_structures.log

temporary_pdb="outputs/metamizole_ethanol_24A.packmol.pdb"
"$packmol_bin" -i packmol/metamizole_ethanol_24A.inp -o "$temporary_pdb" > logs/packmol.log 2>&1

"$python_bin" scripts/validate_system.py "$temporary_pdb" --root "$project_root" > logs/validation.log

echo "Sistema gerado e validado."
echo "PDB: outputs/metamizole_ethanol_24A.pdb"
echo "XYZ: outputs/metamizole_ethanol_24A.xyz"
echo "Relatório: validation/report.md"
