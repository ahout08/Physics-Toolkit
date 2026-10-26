
import math

import pandas as pd
import streamlit as st


# -------------------------------
# PAGE SETUP
# -------------------------------

st.set_page_config(
    page_title="Physics Toolkit",
    page_icon="⚛️",
    layout="wide",
)

G = 9.81

st.title("⚛️ Physics Toolkit")
st.write(
    "Interactive physics calculators and simulations. "
    "Enter values, explore equations, and see how physics works."
)

st.caption("SI units are used throughout unless stated otherwise.")

tabs = st.tabs([
    "Kinematics",
    "Projectile Simulator",
    "Forces",
    "Energy",
    "Circular Motion",
    "Waves & SHM",
    "Electricity",
    "Buoyancy",
])


# -------------------------------
# 1. KINEMATICS
# -------------------------------

with tabs[0]:
    st.header("Kinematics Calculator")
    st.write("Calculate motion using constant acceleration.")

    col1, col2, col3 = st.columns(3)

    with col1:
        u = st.number_input(
            "Initial velocity (m/s)", value=10.0
        )
    with col2:
        a = st.number_input(
            "Acceleration (m/s²)", value=2.0
        )
    with col3:
        t = st.number_input(
            "Time (s)", min_value=0.0, value=5.0
        )

    v = u + a * t
    displacement = u * t + 0.5 * a * t**2

    st.subheader("Results")
    c1, c2 = st.columns(2)
    c1.metric("Final velocity", f"{v:.2f} m/s")
    c2.metric("Displacement", f"{displacement:.2f} m")

    st.latex(r"v=u+at")
    st.latex(r"s=ut+\frac{1}{2}at^2")

    st.caption(
        "Assumes constant acceleration. "
        "Displacement can be negative depending on direction."
    )


# -------------------------------
# 2. PROJECTILE MOTION SIMULATOR
# -------------------------------

with tabs[1]:
    st.header("Projectile Motion Simulator")
    st.write(
        "Move the sliders to change the launch conditions "
        "and observe the trajectory."
    )

    col1, col2 = st.columns(2)

    with col1:
        speed = st.slider(
            "Launch speed (m/s)",
            min_value=1.0,
            max_value=50.0,
            value=20.0,
            step=1.0,
        )

    with col2:
        angle = st.slider(
            "Launch angle (degrees)",
            min_value=0.0,
            max_value=90.0,
            value=45.0,
            step=1.0,
        )

    theta = math.radians(angle)
    ux = speed * math.cos(theta)
    uy = speed * math.sin(theta)

    flight_time = 2 * uy / G
    max_height = uy**2 / (2 * G)
    range_x = speed**2 * math.sin(2 * theta) / G

    c1, c2, c3 = st.columns(3)
    c1.metric("Flight time", f"{flight_time:.2f} s")
    c2.metric("Maximum height", f"{max_height:.2f} m")
    c3.metric("Horizontal range", f"{range_x:.2f} m")

    if flight_time > 0:
        times = [
            flight_time * i / 100
            for i in range(101)
        ]

        positions_x = [ux * time for time in times]
        positions_y = [
            max(0.0, uy * time - 0.5 * G * time**2)
            for time in times
        ]

        graph_data = pd.DataFrame({
            "Horizontal distance (m)": positions_x,
            "Height (m)": positions_y,
        }).set_index("Horizontal distance (m)")

        st.subheader("Trajectory")
        st.line_chart(graph_data, height=350)

    st.latex(r"x=u\cos(\theta)t")
    st.latex(
        r"y=u\sin(\theta)t-\frac{1}{2}gt^2"
    )

    st.caption(
        "Assumes no air resistance and equal launch and landing heights."
    )


# -------------------------------
# 3. FORCES
# -------------------------------

with tabs[2]:
    st.header("Forces and Newton's Laws")

    mass = st.number_input(
        "Mass (kg)", min_value=0.01, value=5.0,
        key="force_mass"
    )
    applied_force = st.number_input(
        "Applied force (N)", value=20.0
    )
    friction = st.number_input(
        "Opposing friction force (N)",
        min_value=0.0,
        value=5.0,
    )

    net_force = applied_force - friction
    acceleration = net_force / mass
    weight = mass * G

    c1, c2, c3 = st.columns(3)
    c1.metric("Net force", f"{net_force:.2f} N")
    c2.metric("Acceleration", f"{acceleration:.2f} m/s²")
    c3.metric("Weight", f"{weight:.2f} N")

    st.latex(r"F_{\text{net}}=ma")
    st.latex(r"W=mg")

    st.caption(
        "The applied force is positive and friction acts in the "
        "opposite direction. Other forces are not included in the "
        "horizontal net-force calculation."
    )


# -------------------------------
# 4. WORK, ENERGY AND POWER
# -------------------------------

with tabs[3]:
    st.header("Work, Energy and Power")

    mass_e = st.number_input(
        "Object mass (kg)", min_value=0.0, value=2.0,
        key="energy_mass"
    )
    velocity_e = st.number_input(
        "Speed (m/s)", min_value=0.0, value=5.0
    )
    height_e = st.number_input(
        "Height (m)", min_value=0.0, value=10.0
    )

    force_e = st.number_input(
        "Applied force (N)", min_value=0.0, value=10.0
    )
    distance_e = st.number_input(
        "Distance moved (m)", min_value=0.0, value=4.0
    )
    time_e = st.number_input(
        "Time taken (s)", min_value=0.01, value=2.0
    )
    force_angle = st.slider(
        "Angle between force and displacement (degrees)",
        0.0, 180.0, 0.0, 1.0,
    )

    kinetic = 0.5 * mass_e * velocity_e**2
    potential = mass_e * G * height_e
    work = (
        force_e * distance_e
        * math.cos(math.radians(force_angle))
    )
    power = work / time_e

    c1, c2 = st.columns(2)
    c1.metric("Kinetic energy", f"{kinetic:.2f} J")
    c2.metric("Gravitational potential energy", f"{potential:.2f} J")

    c3, c4 = st.columns(2)
    c3.metric("Work done", f"{work:.2f} J")
    c4.metric("Average power", f"{power:.2f} W")

    st.latex(r"E_k=\frac{1}{2}mv^2")
    st.latex(r"E_p=mgh")
    st.latex(r"W=Fd\cos(\theta)")
    st.latex(r"P=\frac{W}{t}")


# -------------------------------
# 5. CIRCULAR MOTION
# -------------------------------

with tabs[4]:
    st.header("Circular Motion")

    mass_c = st.number_input(
        "Mass (kg)", min_value=0.01, value=2.0,
        key="circular_mass"
    )
    speed_c = st.number_input(
        "Speed (m/s)", min_value=0.0, value=6.0
    )
    radius_c = st.number_input(
        "Radius (m)", min_value=0.01, value=3.0
    )

    centripetal_a = speed_c**2 / radius_c
    centripetal_f = mass_c * centripetal_a
    angular_v = speed_c / radius_c
    period_c = (
        2 * math.pi / angular_v
        if angular_v > 0 else None
    )

    c1, c2 = st.columns(2)
    c1.metric(
        "Centripetal acceleration",
        f"{centripetal_a:.2f} m/s²"
    )
    c2.metric(
        "Centripetal force",
        f"{centripetal_f:.2f} N"
    )

    c3, c4 = st.columns(2)
    c3.metric("Angular speed", f"{angular_v:.2f} rad/s")
    c4.metric(
        "Period",
        f"{period_c:.2f} s" if period_c is not None else "Undefined"
    )

    st.latex(r"a_c=\frac{v^2}{r}")
    st.latex(r"F_c=\frac{mv^2}{r}")
    st.latex(r"\omega=\frac{v}{r}")


# -------------------------------
# 6. WAVES AND SIMPLE HARMONIC MOTION
# -------------------------------

with tabs[5]:
    st.header("Waves and Oscillations")

    st.subheader("Wave Calculator")

    frequency = st.number_input(
        "Frequency (Hz)", min_value=0.0, value=5.0
    )
    wavelength = st.number_input(
        "Wavelength (m)", min_value=0.0, value=2.0
    )

    wave_speed = frequency * wavelength

    c1, c2, c3 = st.columns(3)
    c1.metric("Wave speed", f"{wave_speed:.2f} m/s")
    c2.metric(
        "Period",
        f"{1 / frequency:.3f} s" if frequency > 0 else "Undefined"
    )
    c3.metric(
        "Angular frequency",
        f"{2 * math.pi * frequency:.2f} rad/s"
    )

    st.latex(r"v=f\lambda")
    st.latex(r"T=\frac{1}{f}")
    st.latex(r"\omega=2\pi f")

    st.divider()
    st.subheader("Mass-Spring Oscillation")

    mass_s = st.number_input(
        "Mass attached to spring (kg)",
        min_value=0.01, value=0.5,
    )
    spring_k = st.number_input(
        "Spring constant (N/m)",
        min_value=0.01, value=20.0,
    )

    period_s = 2 * math.pi * math.sqrt(mass_s / spring_k)
    frequency_s = 1 / period_s

    c1, c2 = st.columns(2)
    c1.metric("Oscillation period", f"{period_s:.3f} s")
    c2.metric("Oscillation frequency", f"{frequency_s:.3f} Hz")

    st.latex(r"T=2\pi\sqrt{\frac{m}{k}}")

    st.caption(
        "The spring formula assumes an ideal mass-spring oscillator "
        "with negligible damping."
    )


# -------------------------------
# 7. ELECTRICITY
# -------------------------------

with tabs[6]:
    st.header("Electricity Calculator")

    voltage = st.number_input(
        "Voltage (V)", min_value=0.0, value=12.0
    )
    resistance = st.number_input(
        "Resistance (Ω)", min_value=0.01, value=6.0
    )

    current = voltage / resistance
    electrical_power = voltage * current

    c1, c2 = st.columns(2)
    c1.metric("Current", f"{current:.3f} A")
    c2.metric("Electrical power", f"{electrical_power:.2f} W")

    st.latex(r"V=IR")
    st.latex(r"P=VI")

    st.divider()
    st.subheader("Equivalent Resistance")

    connection = st.radio(
        "Circuit connection",
        ["Series", "Parallel"],
        horizontal=True,
    )

    r1 = st.number_input(
        "Resistor 1 (Ω)", min_value=0.01, value=4.0
    )
    r2 = st.number_input(
        "Resistor 2 (Ω)", min_value=0.01, value=6.0
    )

    if connection == "Series":
        equivalent = r1 + r2
        st.latex(r"R_{\text{eq}}=R_1+R_2")
    else:
        equivalent = 1 / (1 / r1 + 1 / r2)
        st.latex(
            r"\frac{1}{R_{\text{eq}}}"
            r"=\frac{1}{R_1}+\frac{1}{R_2}"
        )

    st.metric("Equivalent resistance", f"{equivalent:.2f} Ω")


# -------------------------------
# 8. BUOYANCY
# -------------------------------

with tabs[7]:
    st.header("Buoyant Force Calculator")
    st.write(
        "Explore whether an object floats, sinks, or is neutrally "
        "buoyant in a fluid."
    )

    col1, col2 = st.columns(2)

    with col1:
        mass_b = st.number_input(
            "Object mass (kg)",
            min_value=0.001,
            value=0.5,
            key="buoyancy_mass",
        )
        volume_b = st.number_input(
            "Object volume (m³)",
            min_value=0.000001,
            value=0.001,
            format="%.6f",
        )

    with col2:
        fluid_density = st.number_input(
            "Fluid density (kg/m³)",
            min_value=1.0,
            value=1000.0,
        )
        gravity_b = st.number_input(
            "Gravitational field strength (m/s²)",
            min_value=0.01,
            value=9.81,
        )

    object_density = mass_b / volume_b
    weight_b = mass_b * gravity_b
    full_buoyancy = fluid_density * volume_b * gravity_b

    st.subheader("Results")

    c1, c2, c3 = st.columns(3)
    c1.metric("Object density", f"{object_density:.2f} kg/m³")
    c2.metric("Object weight", f"{weight_b:.3f} N")

    if object_density < fluid_density:
        submerged_fraction = object_density / fluid_density
        buoyancy_actual = weight_b
        net_force_b = 0.0

        c3.metric("Buoyant force when floating", f"{buoyancy_actual:.3f} N")
        st.success("Prediction: The object floats.")
        st.write(
            f"Approximately {submerged_fraction * 100:.1f}% "
            "of the object's volume is submerged when floating "
            "at equilibrium."
        )

    elif math.isclose(
        object_density, fluid_density, rel_tol=1e-9
    ):
        buoyancy_actual = weight_b
        net_force_b = 0.0

        c3.metric("Buoyant force", f"{buoyancy_actual:.3f} N")
        st.info(
            "Prediction: The object is neutrally buoyant "
            "in the ideal model."
        )

    else:
        buoyancy_actual = full_buoyancy
        net_force_b = weight_b - full_buoyancy

        c3.metric(
            "Buoyant force when fully submerged",
            f"{buoyancy_actual:.3f} N",
        )
        st.warning("Prediction: The object sinks.")

    st.metric(
        "Net downward force when fully submerged",
        f"{net_force_b:.3f} N",
    )

    st.latex(r"F_B=\rho_{\text{fluid}}gV_{\text{displaced}}")
    st.latex(r"W=mg")
    st.latex(r"\rho_{\text{object}}=\frac{m}{V}")

    st.caption(
        "The model assumes a stationary fluid, no other vertical "
        "forces, and an object that is fully submerged when sinking. "
        "It does not model drag or motion through the fluid."
    )


# -------------------------------
# FOOTER
# -------------------------------

st.divider()
st.caption(
    "Physics Toolkit | Educational project | "
    "Check assumptions and units when using calculated results."
)
