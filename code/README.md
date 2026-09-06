# Code

Two original, from-scratch Python scripts supporting the report's technical
demonstrations. Both are independent re-implementations of textbook/paper
algorithms for illustrative synthetic or simulated scenarios; neither uses
code, data, or figures from any cited source.

## Scripts

- **`python/common.py`** - shared figure-output path and dark-theme
  matplotlib styling used by both demo scripts.
- **`python/matched_filter_demo.py`** - Neyman-Pearson matched-filter
  detection of a known pulse buried in white Gaussian noise. Produces
  `figures/matched_filter_pulse.png` (a single detection example at 3 dB SNR)
  and `figures/matched_filter_snr_sweep.png` (detection score vs. SNR from
  -15 to +15 dB, averaged over 30 trials per point). Verified to locate the
  true pulse arrival time with 0 ms error.
- **`python/music_doa_demo.py`** - MUSIC (MUltiple SIgnal Classification)
  direction-of-arrival estimation on a simulated 8-element uniform linear
  array receiving two sources 8 degrees apart at 10 dB SNR, compared against
  a conventional delay-and-sum beamformer. Produces
  `figures/music_doa_pseudospectrum.png`. Verified to resolve both true
  angles exactly, where the conventional beamformer does not.

Run either script from `code/python/` with `python matched_filter_demo.py`
or `python music_doa_demo.py` (requires `numpy` and `matplotlib`). Figures
are written to `../../figures/`.

## What is cited but not included

The report's background material draws on the following, all cited by
title/author in the report's References section and **not present anywhere
in this repository**:

- H. L. Van Trees, *Optimum Array Processing* (textbook, ~139 MB scan;
  copyrighted, not redistributed)
- R. J. Urick, *Principles of Underwater Sound* (textbook; reference
  material built around it, not redistributed)
- Two underwater acoustic signal detection papers (EM-Viterbi clustering
  method; Taylor, Arrowsmith & Anderson's matched-filter/p-value detector,
  JASA 2013)
- A survey paper on underwater acoustic sensor network applications
  (Murad et al., IJCTE 2015)
- R. O. Schmidt's original MUSIC paper (1986) and S. M. Kay's detection
  theory textbook (1998) - cited for the theory behind the two demo scripts
  above, not reproduced
- Texas Instruments TMS320C54x/C55x DSP technical documentation
- Harbin Engineering University lecture materials (array signal
  processing, digital signal processing, principles of underwater sound)
- Found/third-party MATLAB code (MUSIC/DOA scripts, a DOA GUI, and a
  textbook companion demo package) that was reviewed during research for
  this report but does not appear in this repository and was not used to
  produce any figure or result here
