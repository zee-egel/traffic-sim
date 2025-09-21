# traffic-sim

A tiny object-oriented traffic simulation prototype featuring a single
intersection, basic vehicle spawning, and interchangeable traffic signal
policies. The demo renders an ASCII snapshot every tick and reports simple
metrics when it finishes.

## Running the demo

```bash
python -m traffic_sim
```

You should see a stream of two-line ASCII frames such as:

```
NS:...C..C..............
EW:....C................
SUMMARY: {'entered': X, 'exited': Y, 'avg_travel_time_s': Z.ZZ}
```

## Switching policies

The demo defaults to the fixed-cycle controller. To try the actuated policy,
edit `traffic_sim/__main__.py` and replace the policy instantiation with:

```python
from traffic_sim.control.actuated import ActuatedPolicy
policy = ActuatedPolicy(min_green=6.0, max_green=20.0, yellow=2.0, queue_window_m=25.0)
```

A placeholder `QLearningPolicy` is included in `traffic_sim/control/rl_qlearning.py`
for future reinforcement-learning experiments.
