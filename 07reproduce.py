import math
import numpy as np

# ---------------- Orbital / SSO calculations ----------------
mu = 398600.4418  # km^3/s^2, WGS84
Re = 6378.137     # km, WGS84 equatorial radius
J2 = 1.08262668e-3
omega_earth = 7.2921150e-5  # rad/s
sidereal_day = 2*math.pi/omega_earth
sun_rate_deg_day = 360.0/365.2422
alt = 550.0
a = Re + alt
e = 0.0

# Solve J2 nodal precession for a circular SSO.
target = sun_rate_deg_day
n = math.sqrt(mu/a**3)
cos_i = -2*a*a*(1-e*e)**2 * math.radians(target/86400.0) / (3*J2*n*Re**2)
i_deg = math.degrees(math.acos(cos_i))
T = 2*math.pi/n
period_min = T/60.0
f_ecl = math.asin(Re/a)/math.pi
max_ecl_min = f_ecl*period_min

# Hohmann-like first impulse from 550 km circular to ellipse apogee 550 km, perigee 300 km.
r_a = Re + 550.0
r_p = Re + 300.0
a_trans = 0.5*(r_a+r_p)
v_circ = math.sqrt(mu/r_a)
v_perigee_trans = math.sqrt(mu*(2/r_p - 1/a_trans))
v_apogee_trans = math.sqrt(mu*(2/r_a - 1/a_trans))
# Initial burn is made at apogee of the transfer ellipse, lowering perigee.
dv_eol = v_circ - v_apogee_trans  # km/s, magnitude

# 10 deg plane change at 550 km.
dv_plane_10 = 2*v_circ*math.sin(math.radians(10/2))

# Power first-order budget.
E_eclipse_Wh = 70.0*(max_ecl_min/60.0)
E_sunlit_Wh = 100.0*((period_min-max_ecl_min)/60.0)
E_orbit_Wh = E_eclipse_Wh + E_sunlit_Wh
array_nominal_W = E_orbit_Wh/( (period_min-max_ecl_min)/60.0 )/0.85
battery_min_Wh = E_eclipse_Wh/(0.8*0.9)*1.3
battery_target_Wh = 90.0
# 1 m^2 array, 400 W/m2 BOL, 25% combined degradation/geometry factor -> 300 W EOL.
array_eol_W_per_m2 = 400.0*0.75
array_area_m2 = 1.0
array_eol_W = array_eol_W_per_m2*array_area_m2
# Radiator: 125 W to reject, 20% margin, epsilon=0.9, T=293K.
sigma = 5.670374419e-8
Q = 125.0*1.2
rad_flux = 0.9*sigma*293.0**4
rad_area_m2 = Q/rad_flux

# HHI synthetic market.
shares = [27,23,18,12,8,7,5]
hhi_pre = sum(s*s for s in shares)
hhi_post = 50**2 + 18**2 + 12**2 + 8**2 + 7**2 + 5**2
hhi_delta = hhi_post-hhi_pre

# Simple revisit simulation used in the preliminary artifact.
# State parameterization: mean argument of latitude u; RAAN drifts secularly at sun_rate_deg_day.
P = 3
S = 2
F = 2
swath_central_deg = 4.0
latitudes = np.arange(30.0, 60.0+1e-9, 0.5)
longitudes = np.arange(-180.0, 180.0, 5.0)
points = np.array([(lat, lon) for lat in latitudes for lon in longitudes])
# 8 days, 1-min sample.
N = int(8*24*60)+1
t = np.arange(N)*60.0
# simplified spherical propagation, circular orbit, no perturbation other than secular RAAN.
inc = math.radians(i_deg)
raan0 = np.radians([360.0*p/P for p in range(P)])
# initial u for Walker-like pattern: u0 = 360*(s/S + F*p/(P*S))
u0 = np.array([[math.radians((360.0*(s/S + F*p/(P*S)))%360.0) for s in range(S)] for p in range(P)])
# Convert orbital plane coordinates into ECI, rotate to Earth-fixed by omega*t.
# For performance, sample satellites x=6 and times=11521, then compute closest central angle to target grid.
def rot_z(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def R3z(th):
    c,s=np.cos(th),np.sin(th)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

def R1x(th):
    c,s=np.cos(th),np.sin(th)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

sat_eci = []
for p in range(P):
    R = R3z(raan0[p])@R1x(inc)
    for s in range(S):
        u = n*t + u0[p,s]  # rad
        cu, su = np.cos(u), np.sin(u)
        r_pf = np.vstack([a*cu, a*su, np.zeros_like(u)])
        r_eci = R @ r_pf
        # Earth fixed
        th = omega_earth*t
        c, ss = np.cos(th), np.sin(th)
        x = c*r_eci[0] + ss*r_eci[1]
        y = -ss*r_eci[0] + c*r_eci[1]
        z = r_eci[2]
        lon = np.degrees(np.arctan2(y,x))
        lat = np.degrees(np.arctan2(z,np.sqrt(x*x+y*y)))
        sat_eci.append(np.vstack([lat,lon]).T)
sat_lla = np.array(sat_eci)  # 6 x time x 2

# For each target point, determine access if great-circle central angle <= swath.
latr = np.radians(latitudes)
lonr = np.radians(longitudes)
max_gap_hours = 0.0
first_access = np.full(len(points), np.nan)
last_access = np.full(len(points), np.nan)
for k,(lat,lon) in enumerate(points):
    lat_t = math.radians(lat); lon_t = math.radians(lon)
    # Build access mask across all sats/times in chunks to control memory.
    best = np.ones(N)*999.0
    for sat in sat_lla:
        lat_s = np.radians(sat[:,0]); lon_s = np.radians(sat[:,1])
        dlon = lon_s-lon_t
        cosc = np.sin(lat_s)*math.sin(lat_t)+np.cos(lat_s)*math.cos(lat_t)*np.cos(dlon)
        cang = np.degrees(np.arccos(np.clip(cosc,-1,1)))
        best = np.minimum(best,cang)
    mask = best <= swath_central_deg
    idx = np.flatnonzero(mask)
    if idx.size:
        if np.isnan(first_access[k]): first_access[k] = idx[0]*60
        last = idx[0]
        for j in idx[1:]:
            gap = (j-last)*60
            if gap > max_gap_hours*3600: max_gap_hours = gap/3600
            last = j
        # Include the cyclic wrap from the last access sample to the first sample after one full run.
        if idx.size > 1:
            cyc = (idx[0] + (N-1-idx[-1]))*60
            if cyc > max_gap_hours*3600: max_gap_hours = cyc/3600
    else:
        max_gap_hours = float('inf')
        break

print('ORBIT')
for k,v in [('a_km',a),('inclination_deg',i_deg),('period_min',period_min),('max_eclipse_min',max_ecl_min),('eclipse_fraction',f_ecl),('eol_dv_mps',dv_eol*1000),('plane_change_10deg_mps',dv_plane_10*1000),('sun_rate_deg_day',sun_rate_deg_day),('launch_plane_spacing_days',120.0/sun_rate_deg_day),('power_orbit_Wh',E_orbit_Wh),('array_nominal_W',array_nominal_W),('battery_min_Wh',battery_min_Wh),('radiator_area_m2',rad_area_m2)]:
    print(f'{k}={v:.10f}')
print('REVISIT')
print(f'points={len(points)}')
print(f'max_gap_hours={max_gap_hours:.6f}')
print(f'Walker_u0_deg={[[round(math.degrees(x)%360,3) for x in row] for row in u0]}')
print('HHI')
print(f'pre={hhi_pre}; post={hhi_post}; delta={hhi_delta}')
