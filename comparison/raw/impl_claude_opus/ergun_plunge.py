"""Fluid resistance of a French-press coffee cake (packed bed) plus mesh filter.

Ergun equation for the cake in series with a Darcy-type mesh resistance.
All quantities are SI.
"""
import math

from CoolProp.CoolProp import PropsSI

D_FINES = 30e-6  # diameter of fines particles, d_f (m)
P_ATM = 101325.0  # pressure for water properties (Pa)


def plunge(d, T, m_coffee=0.015, plunge_time=20.0, fines_fraction=0.15,
           D_press=0.085, eps_bed=0.40, rho_bulk=400.0, R_mesh=2.0e8,
           V_liquid=2.3e-4, sphericity=0.75):
    """Pressure drop and force needed to plunge a French press.

    Parameters
    ----------
    d : float            nominal grind diameter (m)
    T : float            water temperature (K), 273.16 to 373
    m_coffee : float     dry coffee mass (kg)
    plunge_time : float  time to push the plunger down (s)
    fines_fraction : float  mass fraction of fines, w_f (-)
    D_press : float      press inner diameter (m)
    eps_bed : float      bed porosity, eps (-), in (0, 1)
    rho_bulk : float     cake bulk density (kg/m^3)
    R_mesh : float       mesh filter resistance (1/m)
    V_liquid : float     liquid volume pushed through the cake (m^3)
    sphericity : float   particle sphericity, phi (-)

    Returns
    -------
    dict with float values:
      k (m^2) viscous-limit permeability; dP, dP_cake, dP_mesh (Pa);
      force (N); Re_b (-) bed Reynolds number; f_p (-) Ergun friction factor;
      inertial_share (-) inertial fraction of the cake dP/L; d32 (m) Sauter
      mean diameter; d_s (m) effective Ergun diameter; L_cake (m) cake
      thickness; u (m/s) superficial velocity.
    """
    if not 273.16 <= T <= 373.0:
        raise ValueError("T must be within 273.16-373 K")
    if not d > 0:
        raise ValueError("d must be > 0")
    if not 0.0 < eps_bed < 1.0:
        raise ValueError("eps_bed must be in (0, 1)")
    if not 0.0 <= fines_fraction <= 1.0:
        raise ValueError("fines_fraction must be in [0, 1]")
    if not 0.0 < sphericity <= 1.0:
        raise ValueError("sphericity must be in (0, 1]")
    for name, val in (("m_coffee", m_coffee), ("plunge_time", plunge_time),
                      ("D_press", D_press), ("rho_bulk", rho_bulk),
                      ("V_liquid", V_liquid)):
        if not val > 0:
            raise ValueError(f"{name} must be > 0")
    if R_mesh < 0:
        raise ValueError("R_mesh must be >= 0")

    rho = PropsSI("D", "T", T, "P", P_ATM, "Water")  # water density (kg/m^3)
    mu = PropsSI("V", "T", T, "P", P_ATM, "Water")   # water viscosity (Pa s)

    w_f = fines_fraction
    d32 = 1.0 / (w_f / D_FINES + (1.0 - w_f) / d)   # Sauter mean diameter (m)
    d_s = sphericity * d32                          # effective diameter (m)

    A = math.pi * D_press**2 / 4.0                  # cross-section area (m^2)
    L_cake = m_coffee / (rho_bulk * A)              # cake thickness (m)
    u = V_liquid / (A * plunge_time)                # superficial velocity (m/s)

    eps = eps_bed
    viscous = 150.0 * mu * (1 - eps)**2 * u / (eps**3 * d_s**2)  # (Pa/m)
    inertial = 1.75 * rho * (1 - eps) * u**2 / (eps**3 * d_s)    # (Pa/m)
    dPdL = viscous + inertial                                    # (Pa/m)

    dP_cake = dPdL * L_cake          # cake pressure drop (Pa)
    dP_mesh = mu * u * R_mesh        # mesh pressure drop (Pa)
    dP = dP_cake + dP_mesh           # total pressure drop (Pa)
    force = dP * A                   # plunger force (N)

    k = d_s**2 * eps**3 / (150.0 * (1 - eps)**2)          # permeability (m^2)
    Re_b = rho * u * d_s / (mu * (1 - eps))               # bed Reynolds (-)
    f_p = dPdL * d_s * eps**3 / (rho * u**2 * (1 - eps))  # friction factor (-)
    inertial_share = inertial / dPdL                      # (-)

    return {k_: float(v) for k_, v in dict(
        k=k, dP=dP, dP_cake=dP_cake, dP_mesh=dP_mesh, force=force, Re_b=Re_b,
        f_p=f_p, inertial_share=inertial_share, d32=d32, d_s=d_s,
        L_cake=L_cake, u=u).items()}
