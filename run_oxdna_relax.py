#!/usr/bin/env python3
"""
Reproduce the oxDNA weak → strong → validate pipeline used for
qca_final_corrected / triplex DNA designs.

Expected design inputs in --workdir (already exported from scadnano/oxView):
  <name>.top   topology
  <name>.dat   initial configuration

Produces the same result artifacts as the manual session:
  INPUT_WEAK, INPUT_STRONG, INPUT_VALIDATE
  weak_trajectory.dat, weak_energy.dat, relaxed_weak.conf
  strong_trajectory.dat, strong_energy.dat, relaxed.conf
  validation_trajectory.dat, validation_energy.dat, validation_last.conf

oxDNA itself is a compiled C++ binary; this script writes INPUT files,
runs that binary, and renames last_conf.dat after each stage.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


# Defaults match simulation and design/qca_final_corrected/INPUT_*
DEFAULT_T = "30C"
DEFAULT_DT = "0.005"
DEFAULT_VERLET_SKIN = "0.05"
DEFAULT_RCUT = "2.0"

WEAK_STEPS = "1e4"
STRONG_STEPS = "1e3"
VALIDATE_STEPS = "200000"


def resolve_oxdna(explicit: str | None) -> Path:
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    env = Path(__file__).resolve().parent
    candidates.extend(
        [
            Path(r"C:\Users\original\Downloads\oxDNA\build\bin\oxDNA"),
            Path("/mnt/c/Users/original/Downloads/oxDNA/build/bin/oxDNA"),
            Path.home() / "Downloads" / "oxDNA" / "build" / "bin" / "oxDNA",
        ]
    )
    which = shutil.which("oxDNA")
    if which:
        candidates.append(Path(which))

    for path in candidates:
        if path and path.is_file():
            return path.resolve()
    raise FileNotFoundError(
        "oxDNA binary not found. Pass --oxdna /path/to/oxDNA "
        "(on Windows use the WSL path, e.g. /mnt/c/Users/.../oxDNA/build/bin/oxDNA)."
    )


def find_design_pair(workdir: Path, name: str | None) -> tuple[str, Path, Path]:
    """Return (stem, topology, conf) for the design."""
    if name:
        top = workdir / f"{name}.top"
        conf = workdir / f"{name}.dat"
        if not top.is_file() or not conf.is_file():
            raise FileNotFoundError(f"Need {top.name} and {conf.name} in {workdir}")
        return name, top, conf

    tops = sorted(workdir.glob("*.top"))
    if not tops:
        raise FileNotFoundError(f"No .top file in {workdir}")
    if len(tops) > 1:
        raise FileNotFoundError(
            f"Multiple .top files in {workdir}; pass --name <stem>. Found: "
            + ", ".join(p.stem for p in tops)
        )
    stem = tops[0].stem
    conf = workdir / f"{stem}.dat"
    if not conf.is_file():
        raise FileNotFoundError(f"Missing companion configuration: {conf}")
    return stem, tops[0], conf


def write_input(path: Path, lines: dict[str, str]) -> None:
    body = "\n".join(f"{k} = {v}" for k, v in lines.items()) + "\n"
    path.write_text(body, encoding="utf-8")


def common_io(topology: str, conf_file: str, trajectory: str, energy: str) -> dict[str, str]:
    return {
        "backend": "CPU",
        "backend_precision": "double",
        "T": DEFAULT_T,
        "dt": DEFAULT_DT,
        "verlet_skin": DEFAULT_VERLET_SKIN,
        "rcut": DEFAULT_RCUT,
        "topology": topology,
        "conf_file": conf_file,
        "trajectory_file": trajectory,
        "refresh_vel": "1",
        "no_stdout_energy": "0",
        "restart_step_counter": "1",
        "energy_file": energy,
        "print_conf_ppc": "51",
        "print_energy_every": "1000",
        "time_scale": "linear",
        "external_forces": "0",
    }


def write_stage_inputs(workdir: Path, topology_name: str, initial_conf: str) -> None:
    weak = common_io(
        topology_name, initial_conf, "weak_trajectory.dat", "weak_energy.dat"
    )
    weak.update(
        {
            "steps": WEAK_STEPS,
            "newtonian_steps": "103",
            "diff_coeff": "2.50",
            "thermostat": "john",
            "interaction_type": "DNA_relax",
            "relax_type": "constant_force",
            "relax_strength": "1",
            "print_conf_interval": "2e4",
        }
    )
    write_input(workdir / "INPUT_WEAK", weak)

    strong = common_io(
        topology_name, "relaxed_weak.conf", "strong_trajectory.dat", "strong_energy.dat"
    )
    strong.update(
        {
            "steps": STRONG_STEPS,
            "newtonian_steps": "1",
            "pt": "0.99",
            "thermostat": "john",
            "interaction_type": "DNA_relax",
            "relax_type": "constant_force",
            "relax_strength": "100",
            "print_conf_interval": "2e4",
        }
    )
    write_input(workdir / "INPUT_STRONG", strong)

    validate = common_io(
        topology_name, "relaxed.conf", "validation_trajectory.dat", "validation_energy.dat"
    )
    validate.update(
        {
            "steps": VALIDATE_STEPS,
            "newtonian_steps": "103",
            "diff_coeff": "2.50",
            "thermostat": "john",
            "interaction_type": "DNA",
            "print_conf_interval": "1000",
        }
    )
    write_input(workdir / "INPUT_VALIDATE", validate)


def to_wsl_path(path: Path) -> str:
    """Convert a Windows path to a /mnt/<drive>/... path for WSL."""
    resolved = path.resolve()
    s = str(resolved)
    if len(s) >= 2 and s[1] == ":":
        drive = s[0].lower()
        rest = s[2:].replace("\\", "/")
        return f"/mnt/{drive}{rest}"
    return s.replace("\\", "/")


def run_oxdna(
    oxdna: Path,
    workdir: Path,
    input_name: str,
    use_wsl: bool,
    log_path: Path | None,
) -> None:
    if use_wsl:
        cmd = [
            "wsl",
            "-e",
            to_wsl_path(oxdna),
            input_name,
        ]
        cwd = None  # set via wsl cd
        # Run inside the workdir from WSL so relative topology/conf paths resolve.
        cmd = [
            "wsl",
            "-e",
            "bash",
            "-lc",
            f"cd '{to_wsl_path(workdir)}' && '{to_wsl_path(oxdna)}' {input_name}",
        ]
        run_cwd = None
    else:
        cmd = [str(oxdna), input_name]
        run_cwd = str(workdir)

    print(f"\n=== Running {input_name} ===")
    print(" ".join(cmd))
    proc = subprocess.run(
        cmd,
        cwd=run_cwd,
        text=True,
        capture_output=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if log_path is not None:
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"\n===== {input_name} =====\n")
            fh.write(out)
            if not out.endswith("\n"):
                fh.write("\n")
    # Stream a short summary to the console
    for line in out.splitlines():
        if line.startswith("INFO:") or line.startswith("WARNING:") or line.startswith("ERROR:"):
            print(line)
        elif line.strip() and line.lstrip()[0].isdigit():
            # energy table rows
            print(line)

    if proc.returncode != 0:
        raise RuntimeError(
            f"oxDNA failed on {input_name} (exit {proc.returncode}).\n{out[-2000:]}"
        )


def promote_last_conf(workdir: Path, dest_name: str) -> Path:
    src = workdir / "last_conf.dat"
    if not src.is_file():
        raise FileNotFoundError(
            f"Expected {src.name} after oxDNA run; check the simulation log."
        )
    dest = workdir / dest_name
    if dest.exists():
        dest.unlink()
    src.rename(dest)
    print(f"Saved {dest.name}")
    return dest


def needs_wsl(oxdna: Path) -> bool:
    """Heuristic: ELF Linux binary on Windows should be launched via WSL."""
    if sys.platform != "win32":
        return False
    try:
        with oxdna.open("rb") as fh:
            magic = fh.read(4)
        return magic == b"\x7fELF"
    except OSError:
        return True


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run oxDNA weak/strong relaxation + validation for a DNA design."
    )
    p.add_argument(
        "--workdir",
        type=Path,
        default=Path("simulation and design/qca_final_corrected"),
        help="Folder containing <name>.top and <name>.dat",
    )
    p.add_argument(
        "--name",
        default=None,
        help="Design stem (default: sole .top stem in workdir). "
        "Example: qca_final_corrected",
    )
    p.add_argument(
        "--oxdna",
        default=None,
        help="Path to oxDNA binary (Windows or WSL path).",
    )
    p.add_argument(
        "--stages",
        default="weak,strong,validate",
        help="Comma-separated stages to run: weak,strong,validate "
        "(or write-inputs to only emit INPUT_* files).",
    )
    p.add_argument(
        "--no-wsl",
        action="store_true",
        help="Do not wrap the oxDNA call in wsl (use when already inside Linux/WSL).",
    )
    p.add_argument(
        "--log",
        type=Path,
        default=None,
        help="Append oxDNA stdout/stderr to this file (default: workdir/run_oxdna.log).",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    workdir = args.workdir.resolve()
    if not workdir.is_dir():
        print(f"Workdir not found: {workdir}", file=sys.stderr)
        return 1

    stem, top, conf = find_design_pair(workdir, args.name)
    print(f"Design: {stem}")
    print(f"  topology: {top.name}")
    print(f"  conf:     {conf.name}")

    write_stage_inputs(workdir, top.name, conf.name)
    print("Wrote INPUT_WEAK, INPUT_STRONG, INPUT_VALIDATE")

    stages = [s.strip().lower() for s in args.stages.split(",") if s.strip()]
    if stages == ["write-inputs"]:
        return 0

    oxdna = resolve_oxdna(args.oxdna)
    use_wsl = (not args.no_wsl) and needs_wsl(oxdna)
    log_path = (args.log or (workdir / "run_oxdna.log")).resolve()
    print(f"oxDNA: {oxdna}")
    print(f"WSL:   {use_wsl}")
    print(f"Log:   {log_path}")

    # Stage chain: each promotes last_conf.dat like the original shell session.
    if "weak" in stages:
        run_oxdna(oxdna, workdir, "INPUT_WEAK", use_wsl, log_path)
        promote_last_conf(workdir, "relaxed_weak.conf")

    if "strong" in stages:
        if not (workdir / "relaxed_weak.conf").is_file():
            raise FileNotFoundError("relaxed_weak.conf missing; run weak stage first.")
        run_oxdna(oxdna, workdir, "INPUT_STRONG", use_wsl, log_path)
        promote_last_conf(workdir, "relaxed.conf")

    if "validate" in stages:
        if not (workdir / "relaxed.conf").is_file():
            raise FileNotFoundError("relaxed.conf missing; run strong stage first.")
        run_oxdna(oxdna, workdir, "INPUT_VALIDATE", use_wsl, log_path)
        promote_last_conf(workdir, "validation_last.conf")

    print("\nDone. Result files in:", workdir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 — CLI surface
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
