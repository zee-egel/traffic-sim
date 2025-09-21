"""Placeholder Q-learning controller that delegates to the actuated policy."""
from __future__ import annotations

from typing import Tuple

from .actuated import ActuatedPolicy
from .policy_base import TrafficSignalPolicy


class QLearningPolicy(TrafficSignalPolicy):
    """Skeleton for future reinforcement-learning based signal control.

    TODOs for a full Q-learning implementation:
    - Encode state features (e.g., queue presence/length per approach).
    - Maintain a Q-table keyed by discretised state/action pairs.
    - Select actions via an epsilon-greedy strategy and update Q-values using
      observed rewards (throughput minus delay is a good starting signal).

    For now we delegate to :class:`ActuatedPolicy` so the simulation remains
    functional while preserving the policy interface.
    """

    def __init__(self) -> None:
        self._delegate = ActuatedPolicy()

    def decide(self, intersection, now_s: float) -> Tuple[str, str]:
        return self._delegate.decide(intersection, now_s)
