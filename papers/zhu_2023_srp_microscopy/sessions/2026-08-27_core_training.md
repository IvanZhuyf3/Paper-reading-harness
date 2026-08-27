# CORE Training Session — 2026-08-27

**Paper:** Stimulated Raman photothermal microscopy toward ultrasensitive chemical imaging
**Identifier:** DOI 10.1126/sciadv.adi2181
**Runner:** TRAINING
**Level:** CORE
**Paper-model source:** fresh reconstruction from source PDF
**Human had not read paper at entry:** YES
**Current state:** KNOWLEDGE

## Disclosure note

The supplied filename/title exposes part of the author solution. During KNOWLEDGE and IDEA, prompts must not use that solution detail to select or steer questions.

## 1. KNOWLEDGE

### Knowledge node K1 — SRS signal formation and detection

Prompt:

> 在 stimulated Raman scattering（SRS）中，pump 与 Stokes 两束光满足 Raman resonance 时，样品和两束光分别发生什么变化？实验上通常检测的“信号”是什么？

Human response:

> srl和srg，通常测这两个过程带来的光强变化

Fact check / pretraining:

- Correct: the optical readout is stimulated Raman loss (SRL) on the pump or stimulated Raman gain (SRG) on the Stokes, measured as a small intensity modulation.
- Missing sample-side statement: one pump photon is converted into one Stokes photon while the energy difference excites the resonant molecular vibration, with `ℏ(ωpump − ωStokes) = ℏΩvib`.
- Typical detection modulates one beam and detects the transferred modulation on the other, commonly with phase-sensitive/lock-in detection.

### Knowledge node K2 — Detectability of a small fractional signal

Prompt:

> 如果 SRS 信号只是叠加在强 pump 或 Stokes 光束上的一个很小的相对光强变化，最低可检测浓度主要受什么约束？为什么不能简单地无限增加入射光功率来改善它？

Human response:

> limited modulation depth和shot noise limit。光太强会有photo damage

Fact check / pretraining:

- Correct: the desired modulation rides on a much larger optical carrier and is constrained by modulation depth and the detected beam's shot noise.
- Increasing photon flux can improve shot-noise-limited SNR only sublinearly, while sample power tolerance and photodamage impose a practical ceiling.

**KNOWLEDGE status:** sufficient for CORE IDEA rollout.

## 2. IDEA

### Source-anchored problem state exposed before rollout

```text
I1 — SRS provides fast, chemically specific vibrational imaging.
     [SOURCE: PDF p.1, Introduction, paragraph beginning
      "Stimulated Raman scattering (SRS) microscopy..."]

I2 — Its detection sensitivity is constrained by small modulation depth
     and shot noise on the detected pump/Stokes beam.
     [SOURCE: PDF p.1, Introduction, paragraph beginning
      "Stimulated Raman scattering (SRS) microscopy..."]

I3 — Increasing photon number is constrained by sample power tolerance.
     [SOURCE: PDF p.1, Introduction, paragraph beginning
      "Stimulated Raman scattering (SRS) microscopy..."]

I4 — Existing noise-reduction approaches have limited practical gain in
     complex imaging systems; existing signal-amplification approaches
     often require special molecules or nanostructures.
     [SOURCE: PDF p.1, Introduction, paragraph beginning
      "Pushing the fundamental limit of..."]

GAP — Seek a broadly applicable route to substantially improve SRS
      detection sensitivity without relying on those special targets or
      unlimited optical power.
     [AGENT INTERPRETATION of the source-anchored Introduction claims]
```

Prompt:

> 在这个问题状态下，你会尝试什么路线？

Human proposal(s):

- H-I1 — Convert the measurement modality and combine SRS with a more
  sensitive readout modality, for example photothermal (PT) detection.

Structural clarification prompt:

> 在你的 PT 路线中，SRS 事件产生的哪个中间物理量携带 Raman-specific information，而 PT readout 具体测量这个量的什么变化？

**Human declared rollout complete:** NO
