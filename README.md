# Hybrid QCA–DNA Memory — Research Work

**QCA computes · DNA remembers · The interface is the research contribution**

This repository documents **original architectural and quantitative research** on a two-tier hybrid memory system: Quantum-Dot Cellular Automata (QCA) as the fast electrostatic processor, and DNA as persistent molecular / sequence memory. The contribution is **not** a new oxDNA solver or a generic CAD tutorial. It is a **criteria-driven hybrid model**: mechanism selection, physical compatibility analysis, quantitative design targets, DNA nanostructure design, and role separation between compute and memory.

Defense narrative: [`QCA-DNA Hybrid Models.pdf`](./QCA-DNA%20Hybrid%20Models.pdf)

---

## Research problem (why this work exists)

Published clocked QCA can “store” bits, but the cited RAM architecture keeps information alive by **continuous circulation in clocked loops**, not CMOS-like static memory (Walus et al., 2004). That is a **processor–memory gap**: QCA is strong at picosecond-scale polarization logic, weak as a persistent store.

**Research question:** How can QCA’s fast electrostatic state be coupled to a physically distinct DNA memory tier—without destroying the strengths of either side—when the two systems speak different state variables (polarization / field vs conformation or nucleotide sequence)?

---

## What is original in this research

Individual building blocks are drawn from published physics/chemistry. **The research contribution is the hybrid integration, selection logic, quantitative compatibility, and architectural role assignment.**

| Research contribution | What was done | Why it matters |
|-----------------------|---------------|----------------------------------|
| **Problem framing** | Treat Walus’s circulating QCA-RAM limitation as the starting gap, not “QCA has no memory” | Positions the work as an interface / architecture problem, not a gadget demo |
| **Role separation** | Assign QCA → fast logic; DNA → persistence / positioning after timescale comparison (~ps QCA vs seconds-scale DNA photoswitch) | Prevents misuse of DNA chemistry inside the critical logic path |
| **Two-tier hybrid memory** | **Model I** (local reversible molecular state) + **Model II** (high-density sequence backing store) | One DNA mechanism cannot optimize both local checkpointing and bulk digital density |
| **Write-path selection** | Reject direct QCA-field writing of DNA (Debye screening in buffer); select **QCSE → discriminator → powered 365/450 nm source → 13-3** | Selection by physical criteria, not fashion |
| **Discriminator insight** | Treat ~4.3 nm QCSE shift as a **sensing signal**, not the photochemical wavelength itself | Makes the optical bridge scientifically defensible |
| **Readback architecture** | Conformation → charged reporter displacement → field-sensitive QCA receiver (Blair-scale targets) | Closes the Model-I loop back into QCA electrostatics |
| **Environment split** | Optical write in aqueous buffer; electrostatic readback in engineered low-screening geometry | Handles screening by architecture, not by wishful physics |
| **Model-II electrical bridge** | QCA → electrometer → binary word → DNA encode / synthesize / PCR-access / sequence | Uses QCA’s native charge state; avoids unnecessary optics for sequence payload |
| **DNA design + structural evidence** | Corrected five-helix scadnano topology; oxDNA validation interpreted within model limits | Shows the researcher designed and stress-tested the molecular scaffold |
| **Modeling discipline** | Explicit boundary: oxDNA supports geometry/topology; published experiments remain authority for azobenzene / Hoogsteen switching | Honest scientific scope—signals research maturity |

---

## Key structural research result

Early work designed a five-helix DNA scaffold (scadnano) as an interface / positioning platform and validated it with coarse-grained oxDNA MD.

> The corrected DNA topology remained covalently intact through 2×10⁵ simulation steps, and the majority of the designed duplex base-pair geometry was retained. Local disruption was concentrated near terminal and crossover regions.

**Research interpretation (not a software claim):** structural survival justifies DNA as a nanoscale memory / positioning platform. It does **not** justify placing DNA chemistry inside the QCA critical logic path. Timescale comparison then drove the architecture: DNA becomes the slower persistent / checkpoint layer.

---

## Model I — Local reversible molecular-state memory

**Stored variable:** compact / open **conformation** of Trinh 13-3 (azobenzene-modified intramolecular triplex)—not charge and not sequence.

**Selected write chain (project integration):**

```text
QCA field  →  QCSE (ΔI / Δλ)  →  discriminator  →  powered 365 or blue/450 nm  →  13-3 state
```

| Block | Published foundation | Project contribution |
|-------|----------------------|----------------------|
| QCA polarization | Lent / Tougaw | Selected processor output state |
| QCSE transducer | Kuo et al. (field→optical response) | Use local QCA field as control input |
| Discriminator + source | Optical/electronic control principle | Separate sensing from exact photochemical wavelength / dose |
| 13-3 switch | Trinh et al. | Interpret compact/open as memory 0/1 |
| Charged reporter (e.g. AuNP) | DNA-origami nanoparticle placement | Convert conformation into a field difference |
| Field-sensitive QCA receiver | Blair-scale electrostatic input | Recover stored state as QCA polarization |

**Quantitative handles used in the design:**

| Quantity | Value | Design use |
|----------|-------|------------|
| QCA propagation | ~2 ps/cell; ~10 ps/5 cells | Keep QCA in the fast path |
| QCSE contrast / shift / speed | 69% ΔF/F; ~4.3 nm; &lt;3.5 μs | Discriminator input; DNA (not QCSE) sets Model-I latency |
| 13-3 UV / blue kinetics | t₁/₂ &lt;1 s (UV); 17 s (blue) | Commit/checkpoint write; reset dominates local latency |
| Blair receiver target | E₀/100 ≈ 4.207 mV/nm | Readback field design target |
| Coulomb reporter fields | ~57.6 → 3.60 mV/nm at 5→20 nm (1e, εᵣ=1) | Distance / charge / orientation as design variables |
| Debye length (1× PBS) | ~0.7 nm | Reject direct static-field DNA write at ~10 nm |

---

## Model II — High-density sequence memory

**Stored variable:** covalent **A/T/G/C sequence** (backing-store tier). Optical transduction is intentionally removed once QCA is read electrically.

```text
QCA polarization → electrometer → binary word → DNA encoding → oligo synthesis
                 → PCR-addressed pool → sequencing + decoding  (rewrite: gBlock / OE-PCR / resynthesis)
```

**Research point:** Model II is not a duplicate of Model I. Local conformation memory cannot provide Organick-scale density/addressability; sequence storage cannot provide direct near-QCA conformational readback. The hybrid is strongest as a **hierarchy**.

| Operation | Physical meaning (keep distinct) |
|-----------|----------------------------------|
| **Write** | Encoding + oligonucleotide synthesis |
| **Access** | PCR primer selection / amplification |
| **Read** | Sequencing + computational decoding |
| **Rewrite** | gBlock / OE-PCR / resynthesis (Yazdi routes) |

---

## Research methodology (multi-tool, correct physical boundary)

Tools answer different questions. Using several tools is part of the research method—not “running standard code for its own sake.”

| Tool | Research question answered | Must not be over-claimed |
|------|----------------------------|---------------------------|
| QCADesigner | Correct QCA logic / clocking / polarization? | DNA chemistry or storage kinetics |
| scadnano | Can DNA geometry / domains / anchors be specified? | Azobenzene photochemistry |
| NUPACK | Obvious competing sequence structures? | Full 3D mechanics / azo switching |
| oxDNA | Is backbone / ensemble mechanically reasonable? | Full cis/trans azo + Hoogsteen chemistry in the standard model |
| Experiment (CD / UV–vis / PAGE / FRET, etc.) | Does 13-3 switch after modification? | QCA field response |
| PCR + sequencing | Can Model-II files be selected / reconstructed? | The initial binary→DNA write event |

**Triplex modeling note (research honesty):** a DNA-only oxDNA control can remain covalently stable yet fail to reproduce the experimental triplex state when azobenzenes, cis/trans interactions, and required Hoogsteen chemistry are omitted. That is a **modeling boundary**, not evidence against the published 13-3 switch.

---

## Simulation package in this repository

Supporting computational evidence for the DNA structural claim (five-helix corrected design and related cases). Automation script: `run_oxdna_relax.py` (orchestrates the same weak → strong → validate protocol used in the research sessions).

### Key result sentence (again)

> The corrected DNA topology remained covalently intact through 2×10⁵ simulation steps, and the majority of the designed duplex base-pair geometry was retained. Local disruption was concentrated near terminal and crossover regions.

### Pipeline used for structural validation

| Stage | Interaction | Role in the research |
|-------|-------------|----------------------|
| Weak relax (`INPUT_WEAK`) | `DNA_relax`, strength 1 | Remove export strain gently |
| Strong relax (`INPUT_STRONG`) | `DNA_relax`, strength 100 | Enforce backbone geometry |
| Validate (`INPUT_VALIDATE`) | `DNA`, **2×10⁵ steps** | Physical MD survival test of the corrected topology |

Typical artifacts: `.sc` / `.top` / `.dat` design exports; `relaxed_weak.conf` → `relaxed.conf` → `validation_last.conf`; energy and trajectory files; oxView / glTF inspection exports.

### Reproduce the validation run

```bash
python run_oxdna_relax.py --workdir "<path-to-design-folder>"
```

Requires a built oxDNA binary (Linux/WSL). Optional: `--stages write-inputs` to emit INPUT files only; `--oxdna PATH` for a custom binary.

---

## How to present this:

1. **Gap:** QCA lacks CMOS-like static memory in the cited RAM architecture → circulating loops.
2. **Contribution:** a **hybrid interface architecture**—not reinventing QCA cells or inventing DNA from scratch.
3. **Model I:** QCA field → QCSE sense → discriminator → exact UV/blue write → 13-3 conformation memory → charged reporter → QCA receiver.
4. **Model II:** electrometer bridge into sequence-tier DNA storage (encode / synthesize / PCR / sequence / rewrite).
5. **Evidence:** criteria tables, Debye / Coulomb / latency numbers, and DNA topology that stayed intact for **2×10⁵** oxDNA steps with duplex retention and localized terminal/crossover disruption.
6. **Novelty statement:** *integration, mechanism selection, and quantitative compatibility*—with clear boundaries on what simulation can and cannot claim.

---

## Selected foundations (cited; not claimed as invented here)

- Walus et al., QCADesigner / QCA RAM limitation (2004)
- Lent & Tougaw, QCA polarization logic
- Kuo et al., QCSE nanoscale field→optical response (2018)
- Trinh et al., reversible 13-3 photoresponsive triplex (2022)
- Blair, field-sensitive QCA receiver scale
- Organick et al., random-access DNA storage (2018)
- Yazdi et al., rewritable DNA storage (2015)
- DNA-origami nanoparticle placement literature (Wang, Ko, Hartl, Thacker, …)

Full criteria tables, calculations, and defense positioning: [`QCA-DNA Hybrid Models.pdf`](./QCA-DNA%20Hybrid%20Models.pdf)

---

## Status

Academic research materials for committee defense and supporting simulation. oxDNA is an external engine used as a **structural validation tool** within stated physical limits; the hybrid memory models and selection analysis are the research product.
