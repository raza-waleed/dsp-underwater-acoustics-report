"""
Matched-filter detection of a known pulse in noise.

This is an original, from-scratch illustration of the classical
Neyman-Pearson matched-filter detector (Kay, 1998), the same detection
framework summarized in Section 4 of the report from two cited underwater
acoustics detection papers. No code or data from those papers is used;
this is a clean re-implementation of the underlying theory for a simple
synthetic scenario, built to show the concept, not to reproduce either
paper's results.

Scenario: a known pulse (a Gaussian-windowed tone, a simple stand-in for
an acoustic transient) arrives at an unknown time within a longer noisy
record. The matched filter is the pulse itself, correlated against the
record; its output should peak sharply at the true arrival sample. The
detector's peak score is then measured as SNR is swept, to show the
detection-theory prediction that performance degrades gracefully, not
catastrophically, as SNR falls.

This exact technique, matched filtering a known reference pulse against
a much longer real recording, was used for real in the lake-trial
report (sync_ping_detection.py), where it achieved correlation scores
above 0.99 against a real recording. This script demonstrates why that
worked: matched filtering is the provably optimal linear detector for a
known signal in white Gaussian noise.

Outputs (written to ../../figures/):
    matched_filter_pulse.png     -- the pulse, the noisy record, and the
                                     matched-filter output
    matched_filter_snr_sweep.png -- detection score vs. SNR
"""

import numpy as np
import matplotlib.pyplot as plt

from common import FIG_DIR, CYAN, ORANGE, GRID, TEXT, style

style()

FS = 2000.0          # Hz, sample rate of the synthetic record
RECORD_LEN_S = 2.0    # seconds
PULSE_LEN_S = 0.05     # seconds
PULSE_FC = 150.0       # Hz, pulse center frequency
TRUE_ARRIVAL_S = 1.2   # seconds, where the pulse is placed in the record


def make_pulse(fs, duration_s, fc):
    n = int(duration_s * fs)
    t = np.arange(n) / fs
    window = np.exp(-((t - duration_s / 2) ** 2) / (2 * (duration_s / 6) ** 2))
    return window * np.cos(2 * np.pi * fc * t)


def make_record(fs, record_len_s, pulse, arrival_s, snr_db, rng):
    n = int(record_len_s * fs)
    record = rng.normal(size=n)  # unit-variance white Gaussian noise
    pulse_power = np.mean(pulse ** 2)
    noise_power = 1.0
    # scale the pulse so that mean(pulse_scaled**2)/noise_power = 10**(snr_db/10)
    target_pulse_power = noise_power * 10 ** (snr_db / 10)
    scale = np.sqrt(target_pulse_power / pulse_power)
    scaled_pulse = pulse * scale

    i0 = int(arrival_s * fs)
    record[i0:i0 + len(pulse)] += scaled_pulse
    return record, i0


def matched_filter_score(record, pulse):
    corr = np.correlate(record, pulse, mode="valid")
    norm = np.linalg.norm(pulse) * np.sqrt(
        np.convolve(record ** 2, np.ones(len(pulse)), mode="valid")
    )
    norm[norm == 0] = 1e-12
    return np.abs(corr) / norm


def plot_pulse_example():
    rng = np.random.default_rng(0)
    pulse = make_pulse(FS, PULSE_LEN_S, PULSE_FC)
    record, i0 = make_record(FS, RECORD_LEN_S, pulse, TRUE_ARRIVAL_S, snr_db=3.0, rng=rng)
    score = matched_filter_score(record, pulse)

    t_record = np.arange(len(record)) / FS
    t_score = np.arange(len(score)) / FS
    peak_idx = np.argmax(score)

    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    axes[0].plot(np.arange(len(pulse)) / FS, pulse, color=CYAN)
    axes[0].set_title("Known pulse (matched-filter template)")
    axes[1].plot(t_record, record, color=CYAN, linewidth=0.5)
    axes[1].axvline(TRUE_ARRIVAL_S, color=ORANGE, linestyle="--", label="true arrival")
    axes[1].set_title("Noisy record containing the pulse at an unknown time (SNR = 3 dB)")
    axes[1].legend(facecolor="#0a0e14", edgecolor=GRID, labelcolor=TEXT)
    axes[2].plot(t_score, score, color=CYAN)
    axes[2].axvline(t_score[peak_idx], color=ORANGE, linestyle="--",
                     label=f"detected arrival (error = {(t_score[peak_idx]-TRUE_ARRIVAL_S)*1000:.1f} ms)")
    axes[2].set_title("Matched-filter output (normalized correlation)")
    axes[2].set_xlabel("time (s)")
    axes[2].legend(facecolor="#0a0e14", edgecolor=GRID, labelcolor=TEXT)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "matched_filter_pulse.png", dpi=120)
    plt.close(fig)
    print(f"Peak detection score: {score[peak_idx]:.3f} at t={t_score[peak_idx]:.4f}s "
          f"(true arrival {TRUE_ARRIVAL_S}s)")


def plot_snr_sweep():
    rng = np.random.default_rng(1)
    pulse = make_pulse(FS, PULSE_LEN_S, PULSE_FC)
    snr_range = np.arange(-15, 16, 1)
    n_trials = 30
    mean_scores = []
    for snr_db in snr_range:
        trial_scores = []
        for _ in range(n_trials):
            record, i0 = make_record(FS, RECORD_LEN_S, pulse, TRUE_ARRIVAL_S, snr_db, rng)
            score = matched_filter_score(record, pulse)
            trial_scores.append(score.max())
        mean_scores.append(np.mean(trial_scores))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(snr_range, mean_scores, "o-", color=CYAN)
    ax.set_xlabel("input SNR (dB)")
    ax.set_ylabel("mean peak matched-filter score")
    ax.set_title(f"Matched-filter detection score vs. SNR ({n_trials} trials per point)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "matched_filter_snr_sweep.png", dpi=120)
    plt.close(fig)
    print("saved matched_filter_snr_sweep.png")


if __name__ == "__main__":
    plot_pulse_example()
    plot_snr_sweep()
