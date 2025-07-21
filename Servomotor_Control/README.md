# DC Servo Motor Modeling and Simulation

This repository contains MATLAB/Simulink models for DC servo motor analysis based on the mathematical framework from control systems theory.

## Table of Contents
- [Overview](#overview)
- [Mathematical Model](#mathematical-model)
- [Block Diagram Development](#block-diagram-development)
- [Transfer Functions](#transfer-functions)
- [Simulink Implementation](#simulink-implementation)
- [Results](#results)
- [Usage](#usage)
- [Files](#files)

## Overview

A DC servo motor is used as an actuator to drive a load with high precision. This project implements the complete mathematical model including:
- Electrical dynamics (armature circuit)
- Electromechanical conversion
- Mechanical dynamics
- Back EMF feedback

## Mathematical Model

### Motor Parameters

| Parameter | Symbol | Description | Units |
|-----------|--------|-------------|-------|
| `Ra` | R<sub>a</sub> | Armature resistance | Ω |
| `La` | L<sub>a</sub> | Armature inductance | H |
| `Kb` | K<sub>b</sub> | Back EMF constant | V⋅s/rad |
| `KT` | K<sub>T</sub> | Motor torque constant | N⋅m/A |
| `J` | J | Moment of inertia | kg⋅m² |
| `B0` | B<sub>0</sub> | Friction coefficient | N⋅m⋅s/rad |

### Fundamental Equations

#### 1. Torque Production (Equation 2.84)
```
T = KT × ia
```
**Where:**
- `T` = motor torque (N⋅m)
- `KT` = motor torque constant (N⋅m/A)
- `ia` = armature current (A)

#### 2. Back EMF Generation (Equation 2.85)
```
eb = Kb × θ̇
```
**Where:**
- `eb` = back EMF (V)
- `Kb` = back EMF constant (V⋅s/rad)
- `θ̇` = angular velocity (rad/s)

#### 3. Electrical System (Equation 2.86)
```
Ra × ia + La × (dia/dt) + eb = ea
```
**Where:**
- `ea` = applied armature voltage (V)
- `Ra` = armature resistance (Ω)
- `La` = armature inductance (H)

#### 4. Mechanical System (Equation 2.91)
```
J × (d²θ/dt²) + B0 × (dθ/dt) = T
```
**Where:**
- `θ` = angular displacement (rad)
- `J` = moment of inertia (kg⋅m²)
- `B0` = friction coefficient (N⋅m⋅s/rad)

### Laplace Domain Analysis

#### Transfer Function Blocks (Figure 2.55)

**Block (i) - Electrical Subsystem:**
```
Ia(s)/[Ea(s) - Eb(s)] = 1/(Ra + s×La)
```

**Block (ii) - Torque Conversion:**
```
T(s) = KT × Ia(s)
```

**Block (iii) - Mechanical Subsystem:**
```
θ(s)/T(s) = 1/(J×s² + B0×s)
```

**Block (iv) - Back EMF Feedback:**
```
Eb(s) = Kb × s × θ(s)
```

#### Complete System Transfer Function (Equation 2.94)
```
θ(s)/Ea(s) = KT / [s(Ra + s×La)(J×s + B0) + Kb×KT]
```

#### Simplified Model (La ≈ 0, Equation 2.95)
When armature inductance is neglected:
```
θ(s)/Ea(s) = (KT/Ra) / [s×(J×s + B)]
```

Where the equivalent friction coefficient is:
```
B = B0 + (Kb×KT)/Ra
```

#### Time Constant Form (Equation 2.97)
```
θ(s)/Ea(s) = KM / [s×(τm×s + 1)]
```

**Where:**
- **Motor gain constant:** `KM = KT/(Ra×J)`
- **Motor time constant:** `τm = J/B`

## Block Diagram Development

The DC servo motor can be represented as an interconnection of four main blocks:

### Individual Transfer Function Blocks
1. **Electrical Block:** Converts voltage difference to current
2. **Torque Block:** Converts current to torque  
3. **Mechanical Block:** Converts torque to angular position
4. **Back EMF Block:** Provides velocity feedback

### Complete System (Figure 2.56)
The complete block diagram shows:
- **Forward path:** `Ea(s) → [Block i] → [Block ii] → [Block iii] → θ(s)`
- **Feedback path:** `θ(s) → [Block iv] → Eb(s) → [Summing junction]`

## Transfer Functions

### Complete Model
For the full system including armature inductance:
```matlab
num = KT;
den_temp = conv([La, Ra], [J, B0]);
den = conv([1, 0], den_temp);
den(end) = den(end) + Kb*KT;
H_complete = tf(num, den);
```

### Simplified Model  
Neglecting armature inductance (La ≈ 0):
```matlab
B_equiv = B0 + (Kb*KT)/Ra;
num = KT/Ra;
den = [J, B_equiv, 0];
H_simplified = tf(num, den);
```

### Time Constant Form
```matlab
KM = KT/(Ra*J);
tau_m = J/B_equiv;
num = KM;
den = [tau_m, 1, 0];
H_time_constant = tf(num, den);
```

## Simulink Implementation

### Block Configuration

#### Transfer Function Blocks
- **Electrical (Block i):** 
  - Numerator: `1`
  - Denominator: `[La Ra]`

- **Mechanical (Block iii):**
  - Numerator: `1` 
  - Denominator: `[J B0 0]`

- **Back EMF (Block iv):**
  - Use Derivative block + Gain block
  - Derivative: `inf` (pure differentiator)
  - Gain: `Kb`

#### Gain Blocks
- **Torque (Block ii):** Gain = `KT`

### Parameter File
Create `motor_params.m`:
```matlab
%% DC Motor Parameters
Ra = 2.0;      % Armature resistance (Ohms)
La = 0.5;      % Armature inductance (H)
Kb = 0.015;    % Back emf constant (V⋅s/rad)
KT = 0.015;    % Torque constant (N⋅m/A)
J = 0.001;     % Moment of inertia (kg⋅m²)
B0 = 0.0001;   % Friction coefficient (N⋅m⋅s/rad)

fprintf('Motor parameters loaded successfully!\n');
```

## Results

### Expected Behavior for Step Input

#### Current Response
- **Initial spike:** High starting current (≈ Ea/Ra)
- **Exponential decay:** As back EMF builds up
- **Steady state:** Low current to overcome friction

#### Torque Response  
- **Follows current pattern:** T = KT × ia
- **High initial torque:** For rapid acceleration
- **Low steady torque:** To maintain constant speed

#### Back EMF Response
- **Starts at zero:** No initial velocity
- **Exponential rise:** As motor spins up
- **Steady value:** Balances with applied voltage minus resistive drop

#### Position Response
- **Exponential approach:** To constant velocity
- **Continuous increase:** At steady-state velocity
- **Final slope:** Represents steady angular velocity

## Usage

### Running the Simulation

1. **Load parameters:**
   ```matlab
   motor_params
   ```

2. **Run Simulink model:**
   ```matlab
   sim('dc_servo_motor')
   ```

3. **Analyze results:**
   ```matlab
   analyze_results
   ```

### Modifying Parameters

To study different motor characteristics, modify values in `motor_params.m`:

- **Increase Ra:** Slower response, higher damping
- **Increase J:** Slower response, longer settling time  
- **Increase Kb:** Better speed regulation, more damping
- **Increase KT:** Higher torque capability, faster response

### Validation

Compare Simulink results with analytical transfer function:
```matlab
motor_params;
H_analytical = tf(KT, conv([1,0], conv([La,Ra],[J,B0])) + [0,0,0,Kb*KT]);
step(H_analytical);
```

## Files

```
📁 DC_Motor_Project/
├── 📄 motor_params.m          # Motor parameter definitions
├── 📄 dc_servo_motor.slx      # Main Simulink model
├── 📄 run_simulation.m        # Simulation runner script
├── 📄 analyze_results.m       # Results analysis script
└── 📄 README.md               # This documentation
```

## Key Physical Insights

1. **Back EMF provides natural speed regulation** - as motor spins faster, back EMF increases, reducing net driving voltage

2. **Current is highest at startup** - when there's no back EMF to oppose applied voltage

3. **Steady-state current depends on load** - determined by friction and external torques

4. **Motor acts as position integrator** - constant voltage input produces constant velocity output

5. **Time constant τm = J/B** - determines how quickly motor reaches steady state

## References

Based on control systems theory for DC servo motor modeling and analysis, specifically equations 2.84 through 2.97 covering:
- Armature controlled DC servo motor modeling
- Block diagram representation 
- Transfer function development
- Simplified analysis techniques

---

> **Note:** This model follows the exact mathematical development from standard control systems textbooks and provides a foundation for advanced control system design.
