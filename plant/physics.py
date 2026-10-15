"""Physics core of the AI Barista Plant. Plain functions, SI units everywhere, no Streamlit calls.

Unit operations
  E-101  kettle (heater)                 hot water feed
  R-101  French press chamber            batch extraction (material balance) + cooling (energy balance)
  F-101  plunger filter                  Darcy flow through grounds cake + mesh (Kozeny-Carman)
  T-101  cup                             Stokes settling of fines

Literature sources (see docs/derivations.html for the full list)
  [M16] Moroney et al., "Coffee extraction kinetics in a well mixed system", J. Math. Industry 7 (2016).
  [C15] Corrochano et al., "A new methodology to estimate the steady-state permeability of roast and
        ground coffee in packed beds", J. Food Eng. 150 (2015).
  [SCA] SCAA Golden Cup brewing control chart: strength 1.15-1.35 %, extraction yield 18-22 %.
"""
import numpy as np
from scipy.integrate import solve_ivp
import CoolProp.CoolProp as CP

G = 9.81            # gravitational acceleration, m/s^2
P_ATM = 101325.0    # atmospheric pressure, Pa

# ---- Coffee properties (literature) ----
RHO_SOLID = 1337.0      # intrinsic density of coffee solid, kg/m^3 [C15]
EPS_PARTICLE = 0.53     # porosity inside a coffee particle, - [C15]
X_EXTRACTABLE = 0.30    # extractable (soluble) mass fraction of roasted coffee, - [M16: 0.28-0.32]
C_SAT = 212.4           # solubility of coffee solubles in water, kg/m^3 [M16]
CELL_SIZE = 30e-6       # diameter of one coffee cell, m [M16]
D_REF = 322e-6          # reference grind (Sauter diameter of fine grind), m [M16]
TAU_D_REF = 42.2        # diffusion time scale at D_REF and 90 C, s [M16]
TAU_S_REF = 1.18        # surface dissolution time scale at D_REF and 90 C, s [M16]
T_REF = 363.15          # reference temperature for the time scales, K (90 C)
CP_COFFEE = 1700.0      # specific heat of dry coffee grounds, J/(kg K)  (ASSUMED, typical food-solid value)

# ---- Target cup [SCA] ----
TDS_RANGE = (0.0115, 0.0135)   # strength = dissolved mass / beverage mass, -
EY_RANGE = (0.18, 0.22)        # extraction yield = dissolved mass / dry coffee mass, -


def water(T):
    """Water properties at temperature T (K) and 1 atm, from CoolProp (IAPWS-95).
    Returns density rho (kg/m^3), viscosity mu (Pa s), specific heat cp (J/(kg K))."""
    if not 273.16 < T < 373.0:
        raise ValueError(f"Water temperature {T - 273.15:.1f} C is outside the liquid range 0-100 C.")
    rho = CP.PropsSI("D", "T", T, "P", P_ATM, "Water")
    mu = CP.PropsSI("V", "T", T, "P", P_ATM, "Water")
    cp = CP.PropsSI("C", "T", T, "P", P_ATM, "Water")
    return rho, mu, cp


# =====================================================================================
# R-101: French press batch (extraction + cooling)
# =====================================================================================
def fast_fraction(d):
    """Fraction of extractables in broken cells at the particle surface (-), for grind diameter d (m):
    volume of a surface shell one cell thick, 1 - (1 - 2 m / d)^3 (geometric model)."""
    return 1 - (1 - 2 * CELL_SIZE / d) ** 3


def time_scales(d, T):
    """Surface dissolution time tau_s (s) and kernel diffusion time tau_d (s) for grind d (m) at T (K).
    tau_d ~ d^2 / D_eff (diffusion), tau_s ~ d^3 (fits both [M16] grinds), and both scale with
    mu/T because the Stokes-Einstein diffusivity is D_eff ~ T/mu."""
    _, mu, _ = water(T)
    _, mu_ref, _ = water(T_REF)
    temp_factor = (mu / T) / (mu_ref / T_REF)
    return TAU_S_REF * (d / D_REF) ** 3 * temp_factor, TAU_D_REF * (d / D_REF) ** 2 * temp_factor


def brew(d, T_water, t_steep, m_coffee=0.015, m_water=0.250, T_amb=295.15, UA=1.0,
         m_vessel=0.35, cp_vessel=840.0, preheated=False, n_points=200):
    """Simulate one French press batch.
    d: grind diameter (m), T_water: kettle water temperature (K), t_steep: steep time (s),
    m_coffee: dry coffee mass (kg), m_water: water mass (kg), T_amb: room temperature (K),
    UA: overall heat-loss conductance of the press (W/K), m_vessel: press mass (kg),
    cp_vessel: press specific heat (J/(kg K)), glass by default, preheated: True if the press was
    rinsed with hot water first (vessel starts at T_water instead of T_amb).

    States: F = undissolved fast (surface) solubles (kg), S = solubles inside particles (kg),
            m_l = solubles dissolved in the bulk liquid (kg), T = brew temperature (K).
    Material balance: F + S + m_l = X_EXTRACTABLE * m_coffee at all times."""
    if not 100e-6 <= d <= 2000e-6:
        raise ValueError("Grind diameter must be between 100 and 2000 micrometres for this model.")
    if t_steep <= 0 or m_coffee <= 0 or m_water <= 0:
        raise ValueError("Steep time and masses must be positive.")

    # Energy balance, step 1: adiabatic mixing of hot water with room-temperature grounds and vessel
    _, _, cp_w = water(T_water)
    C_total = m_water * cp_w + m_coffee * CP_COFFEE + m_vessel * cp_vessel     # J/K
    T_vessel = T_water if preheated else T_amb
    T0 = (m_water * cp_w * T_water + m_coffee * CP_COFFEE * T_amb + m_vessel * cp_vessel * T_vessel) / C_total

    V_particles = m_coffee / (RHO_SOLID * (1 - EPS_PARTICLE))   # particle volume, m^3
    V_kernel = EPS_PARTICLE * V_particles                       # liquid inside particles, m^3
    rho_w0, _, _ = water(T_water)
    V_bulk = m_water / rho_w0 - V_kernel                        # bulk liquid around the particles, m^3
    M_E = X_EXTRACTABLE * m_coffee
    phi = fast_fraction(d)

    def rhs(t, y):
        F, S, m_l, T = y
        tau_s, tau_d = time_scales(d, T)
        c = m_l / V_bulk                        # bulk concentration, kg/m^3
        c_k = S / V_kernel                      # concentration inside particles, kg/m^3
        dF = -(F / tau_s) * (1 - c / C_SAT)     # surface dissolution, slows near saturation
        dS = -(V_kernel / tau_d) * (c_k - c)    # diffusion out of particles
        dT = -UA * (T - T_amb) / C_total        # energy balance, step 2: heat loss to room
        return [dF, dS, -dF - dS, dT]

    t_eval = np.linspace(0, t_steep, n_points)
    sol = solve_ivp(rhs, (0, t_steep), [phi * M_E, (1 - phi) * M_E, 0.0, T0],
                    t_eval=t_eval, method="LSODA", rtol=1e-8, atol=1e-12)
    if not sol.success:
        raise RuntimeError(f"ODE solver failed: {sol.message}")
    F, S, m_l, T = sol.y
    # Beverage: bulk liquid only (liquid inside the particles stays in the grounds)
    rho_end, _, _ = water(T[-1])
    m_bev = V_bulk * rho_end + m_l[-1]
    return {
        "t": sol.t, "T": T, "c": m_l / V_bulk, "F": F, "S": S, "m_l": m_l, "T0": T0,
        "TDS": m_l[-1] / m_bev, "EY": m_l[-1] / m_coffee, "m_beverage": m_bev,
        "balance_error": np.max(np.abs(F + S + m_l - M_E)) / M_E,
        "tau_s": time_scales(d, T0)[0], "tau_d": time_scales(d, T0)[1],
    }


# =====================================================================================
# F-101: plunger filtration
# =====================================================================================
def permeability(d, eps_bed):
    """Kozeny-Carman permeability k = d^2 eps^3 / (180 (1 - eps)^2) (m^2).
    d: particle diameter (m), eps_bed: bed porosity (-).
    [C15] shows this formula can over-predict coffee-bed permeability several-fold, so treat it as an estimate."""
    return d**2 * eps_bed**3 / (180 * (1 - eps_bed) ** 2)


def sauter_diameter(d, fines_fraction, d_fine=CELL_SIZE):
    """Sauter (surface-weighted) mean diameter d32 (m) of a grind with main size d (m) plus a mass fraction
    fines_fraction (-) of fines of size d_fine (m):  1/d32 = w/d_fine + (1 - w)/d.
    Permeability depends on surface area, so a little fines dominates d32 (see [M16]: 27 um for all grains
    vs 322 um for grains above 50 um)."""
    return 1 / (fines_fraction / d_fine + (1 - fines_fraction) / d)


def plunge(d, T, m_coffee=0.015, plunge_time=20.0, fines_fraction=0.15, D_press=0.085, eps_bed=0.40,
           rho_bulk=400.0, R_mesh=2.0e8, V_liquid=2.3e-4):
    """Force (N) to push the plunger down in plunge_time (s).
    Darcy's law through the grounds cake (thickness L_cake, m) in series with the mesh (resistance R_mesh, 1/m):
        dP = mu * u * (L_cake / k + R_mesh),  u = V_liquid / (A * plunge_time) superficial velocity (m/s)
    k from Kozeny-Carman with the Sauter diameter. D_press: press inner diameter (m), eps_bed: cake porosity (-),
    rho_bulk: cake bulk density (kg/m^3) [C15: 360-480], V_liquid: liquid pushed through the cake (m^3).
    R_mesh, eps_bed and fines_fraction are ASSUMED values; calibrate them by plunging a real press on a scale."""
    _, mu, _ = water(T)
    A = np.pi * D_press**2 / 4
    L_cake = m_coffee / (rho_bulk * A)
    d32 = sauter_diameter(d, fines_fraction)
    k = permeability(d32, eps_bed)
    u = V_liquid / (A * plunge_time)
    dP_cake = mu * u * L_cake / k
    dP_mesh = mu * u * R_mesh
    return {"force": (dP_cake + dP_mesh) * A, "dP": dP_cake + dP_mesh, "dP_cake": dP_cake,
            "dP_mesh": dP_mesh, "k": k, "d32": d32, "L_cake": L_cake, "u": u}


# =====================================================================================
# T-101: settling of fines in the cup
# =====================================================================================
def settling(d_fine, T, depth=0.08):
    """Stokes terminal velocity v = (rho_p - rho) g d^2 / (18 mu) (m/s) of a water-filled fine particle,
    time to settle through the cup depth (s), and particle Reynolds number Re_p = rho v d / mu (-).
    Stokes' law holds for Re_p < 0.1 (flag 'valid')."""
    rho, mu, _ = water(T)
    rho_p = RHO_SOLID * (1 - EPS_PARTICLE) + rho * EPS_PARTICLE     # wet particle density, kg/m^3
    v = (rho_p - rho) * G * d_fine**2 / (18 * mu)
    Re_p = rho * v * d_fine / mu
    return {"v": v, "t_settle": depth / v, "Re_p": Re_p, "valid": Re_p < 0.1, "rho_p": rho_p}


def in_target(TDS, EY):
    """True if a cup lands inside the SCA ideal box."""
    return TDS_RANGE[0] <= TDS <= TDS_RANGE[1] and EY_RANGE[0] <= EY <= EY_RANGE[1]
