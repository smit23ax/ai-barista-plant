"""Fluid-only pressure loss through a coffee cake and French-press mesh."""

from math import pi

from CoolProp.CoolProp import PropsSI


def plunge(
    d, T, m_coffee=0.015, plunge_time=20.0, fines_fraction=0.15,
    D_press=0.085, eps_bed=0.40, rho_bulk=400.0, R_mesh=2.0e8,
    V_liquid=2.3e-4, sphericity=0.75,
):
    """Calculate fluid resistance using the Ergun equation.

    Args:
        d: Nominal grind diameter (m).
        T: Water temperature (K).
        m_coffee: Dry coffee mass (kg).
        plunge_time: Time to push the liquid through the bed (s).
        fines_fraction: Mass fraction of 30-micrometer fines (dimensionless).
        D_press: Inner diameter of press (m).
        eps_bed: Packed-bed void fraction (dimensionless).
        rho_bulk: Dry cake bulk density (kg/m^3).
        R_mesh: Mesh hydraulic resistance (1/m).
        V_liquid: Volume of liquid pushed through bed (m^3).
        sphericity: Particle sphericity (dimensionless).

    Returns:
        Dictionary of floats with k (permeability, m^2), dP (total pressure
        drop, Pa), dP_cake (cake pressure drop, Pa), dP_mesh (mesh pressure
        drop, Pa), force (plunger force, N), Re_b (bed Reynolds number,
        dimensionless), f_p (Ergun friction factor, dimensionless),
        inertial_share (fraction of cake pressure gradient, dimensionless),
        d32 (Sauter mean diameter, m), d_s (effective particle diameter, m),
        L_cake (cake thickness, m), and u (superficial velocity, m/s).
    """
    if not (273.16 <= T <= 373.0):
        raise ValueError("T must be between 273.16 and 373 K")
    if d <= 0:
        raise ValueError("d must be positive")
    if not (0 < eps_bed < 1):
        raise ValueError("eps_bed must be strictly between 0 and 1")
    if (m_coffee <= 0 or plunge_time <= 0 or D_press <= 0 or
            rho_bulk <= 0 or V_liquid <= 0 or sphericity <= 0 or
            not 0 <= fines_fraction <= 1 or R_mesh < 0):
        raise ValueError("Non-physical bed, flow, or mesh parameter")

    rho = PropsSI("Dmass", "T", T, "P", 101325.0, "Water")  # kg/m^3
    mu = PropsSI("VISCOSITY", "T", T, "P", 101325.0, "Water")  # Pa s

    d_f = 30e-6  # Diameter of fines (m)
    d32 = 1.0 / (fines_fraction / d_f + (1 - fines_fraction) / d)  # m
    d_s = sphericity * d32  # Effective particle diameter (m)
    A = pi * D_press**2 / 4  # Cross-sectional flow area (m^2)
    L_cake = m_coffee / (rho_bulk * A)  # Cake thickness (m)
    u = V_liquid / (A * plunge_time)  # Superficial velocity (m/s)

    eps = eps_bed  # Bed porosity (dimensionless)
    viscous = 150 * mu * (1 - eps)**2 * u / (eps**3 * d_s**2)  # Pa/m
    inertial = 1.75 * rho * (1 - eps) * u**2 / (eps**3 * d_s)  # Pa/m
    gradient = viscous + inertial  # Cake pressure gradient (Pa/m)

    dP_cake = gradient * L_cake  # Pa
    dP_mesh = mu * u * R_mesh  # Pa
    dP = dP_cake + dP_mesh  # Pa
    force = dP * A  # N
    k = d_s**2 * eps**3 / (150 * (1 - eps)**2)  # m^2
    Re_b = rho * u * d_s / (mu * (1 - eps))  # Dimensionless
    f_p = gradient * d_s * eps**3 / (rho * u**2 * (1 - eps))
    inertial_share = inertial / gradient  # Dimensionless, cake only

    return {name: float(value) for name, value in {
        "k": k, "dP": dP, "dP_cake": dP_cake, "dP_mesh": dP_mesh,
        "force": force, "Re_b": Re_b, "f_p": f_p,
        "inertial_share": inertial_share, "d32": d32, "d_s": d_s,
        "L_cake": L_cake, "u": u,
    }.items()}
