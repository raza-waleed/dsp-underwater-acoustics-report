"""
MUSIC direction-of-arrival (DOA) estimation on a simulated sensor array.

An original, from-scratch implementation of the MUSIC (MUltiple SIgnal
Classification) algorithm (Schmidt, 1986), the subspace-based DOA method
that is the modern successor to the classical beamforming and array
processing theory covered in Van Trees' "Optimum Array Processing" and
in the array-signal-processing coursework this report's Section 5
summarizes. No code from that textbook or its companion demo package is
used; this is a clean re-implementation of the algorithm for a
simulated scenario.

IMPORTANT: this is a SIMULATION, not real hydrophone array data. No
multi-element array recording exists anywhere in this project's
portfolio; the purpose here is to demonstrate working understanding of
the algorithm, not to characterize a real array.

Scenario: a uniform linear array (ULA) of omnidirectional sensors
receives two narrowband plane waves from known, closely-spaced angles,
plus uncorrelated sensor noise. MUSIC exploits the orthogonality
between the signal subspace and the noise subspace of the array
covariance matrix (found via its eigendecomposition) to produce a
pseudospectrum with sharp peaks at the true arrival angles, resolving
sources that a conventional (delay-and-sum) beamformer cannot separate
at the same array aperture.

Outputs (written to ../../figures/):
    music_doa_pseudospectrum.png -- MUSIC vs. conventional beamformer,
                                     showing the resolution improvement
"""

import numpy as np
import matplotlib.pyplot as plt

from common import FIG_DIR, CYAN, ORANGE, MAGENTA, GRID, TEXT, style

style()

N_SENSORS = 8
ELEMENT_SPACING_WAVELENGTHS = 0.5   # half-wavelength spacing, standard for a ULA
TRUE_ANGLES_DEG = [-8.0, 8.0]        # two closely-spaced sources
SNR_DB = 10.0
N_SNAPSHOTS = 200


def steering_vector(theta_deg, n_sensors, d_over_lambda):
    theta = np.radians(theta_deg)
    n = np.arange(n_sensors)
    return np.exp(1j * 2 * np.pi * d_over_lambda * n * np.sin(theta))


def simulate_array_data(angles_deg, n_sensors, d_over_lambda, snr_db, n_snapshots, rng):
    n_sources = len(angles_deg)
    A = np.array([steering_vector(a, n_sensors, d_over_lambda) for a in angles_deg]).T  # (n_sensors, n_sources)

    source_power = 1.0
    signals = (rng.normal(size=(n_sources, n_snapshots)) +
               1j * rng.normal(size=(n_sources, n_snapshots))) / np.sqrt(2) * np.sqrt(source_power)

    noise_power = source_power * 10 ** (-snr_db / 10)
    noise = (rng.normal(size=(n_sensors, n_snapshots)) +
             1j * rng.normal(size=(n_sensors, n_snapshots))) / np.sqrt(2) * np.sqrt(noise_power)

    X = A @ signals + noise  # (n_sensors, n_snapshots)
    return X, noise_power


def music_pseudospectrum(X, n_sources, n_sensors, d_over_lambda, scan_angles_deg):
    R = (X @ X.conj().T) / X.shape[1]
    eigvals, eigvecs = np.linalg.eigh(R)
    order = np.argsort(eigvals)[::-1]
    eigvecs = eigvecs[:, order]
    noise_subspace = eigvecs[:, n_sources:]  # (n_sensors, n_sensors - n_sources)

    spectrum = np.zeros(len(scan_angles_deg))
    for i, theta in enumerate(scan_angles_deg):
        a = steering_vector(theta, n_sensors, d_over_lambda)
        proj = noise_subspace.conj().T @ a
        spectrum[i] = 1.0 / (np.sum(np.abs(proj) ** 2) + 1e-12)
    return spectrum / spectrum.max()


def conventional_beamformer(X, n_sensors, d_over_lambda, scan_angles_deg):
    R = (X @ X.conj().T) / X.shape[1]
    spectrum = np.zeros(len(scan_angles_deg))
    for i, theta in enumerate(scan_angles_deg):
        a = steering_vector(theta, n_sensors, d_over_lambda)
        spectrum[i] = np.real(a.conj().T @ R @ a)
    return spectrum / spectrum.max()


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    X, noise_power = simulate_array_data(
        TRUE_ANGLES_DEG, N_SENSORS, ELEMENT_SPACING_WAVELENGTHS, SNR_DB, N_SNAPSHOTS, rng
    )

    scan_angles = np.linspace(-90, 90, 721)
    music_spec = music_pseudospectrum(X, len(TRUE_ANGLES_DEG), N_SENSORS,
                                       ELEMENT_SPACING_WAVELENGTHS, scan_angles)
    bf_spec = conventional_beamformer(X, N_SENSORS, ELEMENT_SPACING_WAVELENGTHS, scan_angles)

    music_db = 10 * np.log10(music_spec + 1e-6)
    bf_db = 10 * np.log10(bf_spec + 1e-6)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(scan_angles, bf_db, color=ORANGE, label="Conventional (delay-and-sum) beamformer")
    ax.plot(scan_angles, music_db, color=CYAN, label="MUSIC")
    for a in TRUE_ANGLES_DEG:
        ax.axvline(a, color=MAGENTA, linestyle="--", linewidth=1, alpha=0.7)
    ax.set_xlim(-40, 40)
    ax.set_xlabel("angle (degrees)")
    ax.set_ylabel("normalized spectrum (dB)")
    ax.set_title(f"MUSIC vs. Conventional Beamforming, {N_SENSORS}-element ULA\n"
                 f"Two sources at {TRUE_ANGLES_DEG[0]:.0f} deg and {TRUE_ANGLES_DEG[1]:.0f} deg, "
                 f"SNR = {SNR_DB:.0f} dB (simulated data, dashed lines = true angles)")
    ax.legend(facecolor="#0a0e14", edgecolor=GRID, labelcolor=TEXT)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "music_doa_pseudospectrum.png", dpi=120)
    plt.close(fig)

    music_peaks_idx = np.where((np.diff(np.sign(np.diff(music_spec))) < 0))[0] + 1
    top_peaks = sorted(music_peaks_idx, key=lambda i: -music_spec[i])[:2]
    detected_angles = sorted(scan_angles[i] for i in top_peaks)
    print(f"True angles: {TRUE_ANGLES_DEG}")
    print(f"MUSIC-detected peak angles: {[round(a,1) for a in detected_angles]}")
    print("saved music_doa_pseudospectrum.png")
