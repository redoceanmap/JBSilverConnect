from __future__ import annotations

from jb.apps.phishing.app.dtos.phishing_dto import PhishingView
from jb.apps.phishing.domain.entities.phishing_assessment_entity import PhishingAssessment


def to_view(assessment: PhishingAssessment) -> PhishingView:
    return PhishingView(
        risk_label=assessment.risk_label(),
        signal_color=assessment.signal_color(),
        alert_staff=assessment.should_alert_staff(),
        advice=assessment.advice(),
    )
