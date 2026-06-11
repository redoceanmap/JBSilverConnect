from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CheckPhishingCommand:
    message: str


@dataclass(frozen=True)
class PhishingView:
    risk_label: str
    signal_color: str
    alert_staff: bool
    advice: str
