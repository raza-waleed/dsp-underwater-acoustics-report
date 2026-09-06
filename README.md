# Digital Signal Processing for Underwater Acoustic Channels

A report connecting the theoretical foundations of underwater
acoustic DSP (processor architecture, channel properties, detection theory,
array signal processing, and OFDM) to real, previously validated results
from two other reports in this portfolio: a transducer/hydrophone tank
characterization and a lake-trial OFDM/QPSK channel study.

Open [`dsp-underwater-acoustics-report.html`](dsp-underwater-acoustics-report.html)
in a browser to read the report, or read it live at
[waleedraza.dev/underwater-acoustics/dsp-foundations](https://waleedraza.dev/underwater-acoustics/dsp-foundations/).
The two demo scripts are also mirrored on [Hugging Face](https://huggingface.co/spaces/waleedraza93/dsp-underwater-acoustics-report)
(a plain code mirror, not a trained model).

## What this is

This report does not present new field measurements. Instead, it presents
five background topics in the report's own words, cites every external
source (textbooks, papers, reference material) by title and author without
reproducing any of it, and builds two original computational demonstrations
from scratch (a matched-filter detector and a MUSIC direction-of-arrival
estimator) to show working understanding of the two most algorithmically
involved topics. It then draws explicit, verifiable connections to real
results already published elsewhere in this portfolio:

- Matched filtering (the subject of the detection-theory literature cited
  here) is the exact technique that detected a real synchronization pulse
  at correlation scores above 0.99 in the lake trial.
- The OFDM scheme described here is the same one independently
  reconstructed from a real underwater recording to 0.001% error vector
  magnitude in the lake trial.
- Shallow-water channel properties described here (frequency-
  dependent attenuation, short coherence time) were independently measured
  in the lake trial's real data.

See [`code/README.md`](code/README.md) for details on the two original demo
scripts and a full list of what is cited but intentionally not included in
this repository.

## Related reports in this portfolio

- [Underwater Acoustic Transducer & Hydrophone Systems](https://github.com/raza-waleed/acoustic-measurement-report) - tank characterization report
- [Underwater Acoustic OFDM/QPSK Communication](https://github.com/raza-waleed/underwater-acoustic-ofdm-lake-trial) - lake trial report

## Contents

```
dsp-underwater-acoustics-report.html   the report
code/python/                           original demo scripts (see code/README.md)
figures/                               generated figures used by the report
```
