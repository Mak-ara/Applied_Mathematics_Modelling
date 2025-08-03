import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt

class TrafficIntersection:
    """Simple 2-phase traffic intersection model"""

    def __init__(self, arrival_rates, saturation_flows, lost_time=6):
        """
        arrival_rates: [λ1, λ2] vehicles/second for each approach
        saturation_flows: [μ1, μ2] vehicles/second when green
        lost_time: total lost time per cycle (seconds)
        """
        self.arrival_rates = np.array(arrival_rates)
        self.saturation_flows = np.array(saturation_flows)
        self.lost_time = lost_time

    def webster_delay(self, green_times, cycle_length):
        """Calculate average delay per vehicle using Webster's formula"""
        g1, g2 = green_times
        C = cycle_length

        # Degree of saturation for each approach
        x1 = (self.arrival_rates[0] / self.saturation_flows[0]) * (C / g1)
        x2 = (self.arrival_rates[1] / self.saturation_flows[1]) * (C / g2)

        # Check stability constraint
        if x1 >= 0.95 or x2 >= 0.95:
            return float('inf'), float('inf'), x1, x2

        # Webster's delay formula
        d1 = (C * (1 - g1/C)**2) / (2 * (1 - x1)) + (x1**2) / (2 * self.saturation_flows[0] * (1 - x1))
        d2 = (C * (1 - g2/C)**2) / (2 * (1 - x2)) + (x2**2) / (2 * self.saturation_flows[1] * (1 - x2))

        return d1, d2, x1, x2

    def total_delay(self, green_times, cycle_length):
        """Total system delay (objective function)"""
        d1, d2, x1, x2 = self.webster_delay(green_times, cycle_length)
        if d1 == float('inf'):
            return float('inf')

        # Total delay = arrival_rate × delay_per_vehicle
        return self.arrival_rates[0] * d1 + self.arrival_rates[1] * d2

    def simulate_queues(self, green_times, cycle_length, num_cycles=3):
        """Simulating queue evolution over multiple cycles"""
        g1, g2 = green_times
        dt = 0.1  # time step
        time_points = np.arange(0, num_cycles * cycle_length, dt)

        q1_history = []
        q2_history = []
        q1, q2 = 0, 0  # initial queue lengths

        for t in time_points:
            # Determine current phase
            cycle_time = t % cycle_length
            phase1_active = cycle_time < g1
            phase2_active = g1 <= cycle_time < (g1 + g2)

            # Queue dynamics: dq/dt = arrivals - departures
            if phase1_active:
                dq1_dt = self.arrival_rates[0] - self.saturation_flows[0]
                dq2_dt = self.arrival_rates[1]
            elif phase2_active:
                dq1_dt = self.arrival_rates[0]
                dq2_dt = self.arrival_rates[1] - self.saturation_flows[1]
            else:  # lost time
                dq1_dt = self.arrival_rates[0]
                dq2_dt = self.arrival_rates[1]

            # Update queues 
            q1 = max(0, q1 + dq1_dt * dt)
            q2 = max(0, q2 + dq2_dt * dt)

            q1_history.append(q1)
            q2_history.append(q2)

        return time_points, np.array(q1_history), np.array(q2_history)

    def optimize_timing(self, cycle_length=90):
        """Find optimal green time split for given cycle length"""

        def objective(g1):
            g2 = cycle_length - g1 - self.lost_time
            if g2 <= 0:
                return float('inf')
            return self.total_delay([g1, g2], cycle_length)

        # Optimize g1 (g2 is determined by constraint)
        result = minimize_scalar(objective, bounds=(10, cycle_length - self.lost_time - 10),
                               method='bounded')

        optimal_g1 = result.x
        optimal_g2 = cycle_length - optimal_g1 - self.lost_time

        return optimal_g1, optimal_g2, result.fun

# Example usage
if __name__ == "__main__":
    # Create intersection: North-South vs East-West
    # Arrival rates: 0.3 and 0.2 vehicles/second
    # Saturation flows: 0.5 and 0.45 vehicles/second when green
    intersection = TrafficIntersection(
        arrival_rates=[0.3, 0.2],
        saturation_flows=[0.5, 0.45]
    )

    # Find optimal timing
    g1_opt, g2_opt, min_delay = intersection.optimize_timing(cycle_length=90)

    print(f"Optimal Green Times:")
    print(f"Approach 1: {g1_opt:.1f} seconds")
    print(f"Approach 2: {g2_opt:.1f} seconds")
    print(f"Total System Delay: {min_delay:.2f} vehicle-seconds per cycle")

    # Compare with equal split
    g1_equal = g2_equal = (90 - 6) / 2  # Equal green times
    equal_delay = intersection.total_delay([g1_equal, g2_equal], 90)

    print(f"\nEqual Split Comparison:")
    print(f"Equal green times: {g1_equal:.1f} seconds each")
    print(f"Equal split delay: {equal_delay:.2f} vehicle-seconds per cycle")
    print(f"Improvement: {((equal_delay - min_delay) / equal_delay * 100):.1f}%")

    # Analyze delays
    d1_opt, d2_opt, x1_opt, x2_opt = intersection.webster_delay([g1_opt, g2_opt], 90)
    print(f"\nTraffic Analysis:")
    print(f"Saturation ratios: {x1_opt:.3f}, {x2_opt:.3f}")
    print(f"Average delays: {d1_opt:.1f}s, {d2_opt:.1f}s per vehicle")

    # Simulate and plot queue evolution
    time, q1, q2 = intersection.simulate_queues([g1_opt, g2_opt], 90)

    plt.figure(figsize=(12, 4))
    plt.plot(time, q1, label='Approach 1 Queue', linewidth=2)
    plt.plot(time, q2, label='Approach 2 Queue', linewidth=2)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Queue Length (vehicles)')
    plt.title('Queue Evolution with Optimal Timing')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # Sensitivity analysis
    print(f"\nSensitivity Analysis:")
    cycle_lengths = [60, 75, 90, 105, 120]
    for C in cycle_lengths:
        g1, g2, delay = intersection.optimize_timing(C)
        print(f"Cycle {C}s: g1={g1:.1f}s, g2={g2:.1f}s, delay={delay:.1f}")
