"""
Peak-to-average power ratio of the lake trial's actual, validated OFDM scheme.

This is an original, from-scratch computation, not a reproduction of any
third-party code. It builds a synthetic realization of the exact OFDM
structure recovered and validated in this portfolio's lake-trial report
(a real-valued 8192-point IFFT, 512 active QPSK subcarriers occupying a
3 kHz sub-band), then computes the peak-to-average power ratio (PAPR) of
the resulting time-domain waveform across many random symbol
realizations, producing a PAPR complementary cumulative distribution
function (CCDF), the standard way PAPR performance is reported in the
OFDM literature.

The two named PAPR-reduction techniques discussed alongside this result
in the report, partial transmit sequence (PTS) and selected mapping
(SLM), are cited to their original papers (Muller & Huber, 1997; Bauml,
Fischer & Huber, 1996) and are not implemented or reproduced here; this
script only measures how large the problem actually is for this
portfolio's own real OFDM scheme, which is the number those techniques
would need to improve on.

Output (written to ../../figures/):
    ofdm_papr_ccdf.png -- PAPR CCDF for the real 512-active-subcarrier,
                           8192-point lake-trial OFDM structure
"""
import numpy as np
import matplotlib.pyplot as plt

from common import FIG_DIR, CYAN, ORANGE, GRID, TEXT, style

style()

NFFT = 8192          # real lake-trial FFT size
N_ACTIVE = 512        # real lake-trial active subcarriers per sub-band
N_TRIALS = 20_000     # independent random OFDM symbol realizations
RNG = np.random.default_rng(11)


def make_ofdm_symbol(n_active, nfft, rng):
    """One real-valued OFDM time-domain symbol: n_active QPSK subcarriers
    placed consecutively in the positive-frequency half of an nfft-point
    real IFFT (conjugate-symmetric construction), matching the lake
    trial's own real-valued-FFT convention."""
    half = nfft // 2
    spectrum = np.zeros(half + 1, dtype=complex)
    qpsk_alphabet = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]) / np.sqrt(2)
    start_bin = 100  # arbitrary in-band placement; PAPR is insensitive to it
    symbols = rng.choice(qpsk_alphabet, size=n_active)
    spectrum[start_bin:start_bin + n_active] = symbols
    return np.fft.irfft(spectrum, n=nfft)


def papr_db(x):
    peak = np.max(x ** 2)
    avg = np.mean(x ** 2)
    return 10 * np.log10(peak / avg)


def main():
    paprs = np.array([
        papr_db(make_ofdm_symbol(N_ACTIVE, NFFT, RNG)) for _ in range(N_TRIALS)
    ])

    sorted_papr = np.sort(paprs)
    ccdf = 1.0 - np.arange(1, N_TRIALS + 1) / N_TRIALS

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.semilogy(sorted_papr, ccdf, color=CYAN, linewidth=1.6)
    ax.set_xlabel("PAPR0 (dB)")
    ax.set_ylabel("P(PAPR > PAPR0)")
    ax.set_title(f"PAPR CCDF, {N_ACTIVE} active QPSK subcarriers, "
                 f"{NFFT}-point real IFFT\n({N_TRIALS:,} random symbol realizations "
                 "of the lake trial's own validated OFDM structure)")
    ax.grid(True, color=GRID, alpha=0.4)

    p99 = sorted_papr[int(0.99 * N_TRIALS)]
    p999 = sorted_papr[int(0.999 * N_TRIALS)]
    for p, label, color in [(p99, "99%", ORANGE), (p999, "99.9%", "white")]:
        ax.axvline(p, color=color, linestyle="--", linewidth=1,
                    label=f"{label}: PAPR = {p:.1f} dB")
    ax.legend(facecolor="#0a0e14", edgecolor=GRID, labelcolor=TEXT)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "ofdm_papr_ccdf.png", dpi=130)
    plt.close(fig)

    print(f"Mean PAPR: {paprs.mean():.2f} dB")
    print(f"99% CCDF point: {p99:.2f} dB")
    print(f"99.9% CCDF point: {p999:.2f} dB")
    print("saved ofdm_papr_ccdf.png")


if __name__ == "__main__":
    main()
