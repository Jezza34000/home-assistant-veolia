"""Veolia model."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from .const import (
    CONSO,
    CONSO_FIABILITY,
    CUBIC_METER,
    DATA_DATE,
    IDX,
    IDX_FIABILITY,
    LITRE,
)


def _safe_last(seq: Iterable[Any]) -> Any | None:
    """Get last data."""
    try:
        s = list(seq) if not isinstance(seq, list) else seq
        return s[-1] if s else None
    except Exception:
        return None


def _parse_date(s: str) -> date | None:
    """Parse date."""
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def _find_last_for_date(records: list[dict], d: date) -> dict | None:
    """Find last available data for date."""
    for rec in reversed(records or []):
        if _parse_date(rec.get(DATA_DATE, "")) == d:
            return rec
    return None


@dataclass(slots=True)
class VeoliaComputed:
    """Veolia computed data."""

    last_index_m3: float | None
    last_daily_liters: int | None
    last_daily_m3: float | None
    monthly_latest_m3: float | None
    annual_total_m3: float | None
    last_date: date | None
    daily_fiability: str | None
    monthly_fiability: str | None
    daily_stats_liters: list[dict]
    index_stats_m3: list[dict]
    daily_today_liters: int | None
    daily_today_m3: float | None
    daily_today_fiability: str | None


@dataclass(slots=True)
class VeoliaModel:
    """VeoliaModel."""

    raw: Any  # VeoliaAccountData
    computed: VeoliaComputed

    def __getattr__(self, name: str):
        """GetAttr for Switch and BinarySensor."""
        return getattr(self.raw, name)

    @staticmethod
    def from_account_data(raw: Any, *, today: date | None = None) -> VeoliaModel:
        """Read data and populate VeoliaComputed model."""
        daily = raw.daily_consumption or []
        monthly = raw.monthly_consumption or []

        last_daily = _safe_last(daily) or {}
        last_month = _safe_last(monthly) or {}

        last_index_m3 = (last_daily.get(IDX) or {}).get(CUBIC_METER) or (
            last_month.get(IDX) or {}
        ).get(CUBIC_METER)
        last_index_m3 = float(last_index_m3) if last_index_m3 is not None else None

        last_daily_liters = (last_daily.get(CONSO) or {}).get(LITRE)
        last_daily_liters = (
            int(last_daily_liters) if last_daily_liters is not None else None
        )

        last_daily_m3 = (last_daily.get(CONSO) or {}).get(CUBIC_METER)
        last_daily_m3 = float(last_daily_m3) if last_daily_m3 is not None else None

        monthly_latest_m3 = (last_month.get(CONSO) or {}).get(CUBIC_METER)
        monthly_latest_m3 = (
            float(monthly_latest_m3) if monthly_latest_m3 is not None else None
        )

        try:
            annual_total_m3 = float(
                sum(
                    float((m.get(CONSO) or {}).get(CUBIC_METER) or 0.0) for m in monthly
                )
            )
        except Exception:
            annual_total_m3 = None

        d_last = (last_daily or {}).get(DATA_DATE)
        last_date = _parse_date(d_last) if d_last else None

        daily_fiability = (last_daily or {}).get(IDX_FIABILITY)
        monthly_fiability = (last_month or {}).get(CONSO_FIABILITY)

        if today is None:
            today = datetime.now().date()
        rec_today = _find_last_for_date(daily, today)
        if rec_today:
            _c = rec_today.get(CONSO) or {}
            daily_today_liters = int(_c.get(LITRE) or 0)
            daily_today_m3 = float(_c.get(CUBIC_METER) or 0.0)
            daily_today_fiability = rec_today.get(IDX_FIABILITY)
        else:
            daily_today_liters = None
            daily_today_m3 = None
            daily_today_fiability = None

        # Recorder data
        daily_stats_liters: list[dict] = []
        index_stats_m3: list[dict] = []
        try:
            cumul_liters = 0
            for rec in daily:
                d = _parse_date(rec.get(DATA_DATE, ""))
                if not d:
                    continue
                liters = int((rec.get(CONSO) or {}).get(LITRE) or 0)
                cumul_liters += liters
                start_dt = datetime.combine(d, datetime.min.time())
                daily_stats_liters.append(
                    {"start": start_dt, "state": liters, "sum": cumul_liters}
                )

            total_sum = 0.0
            last_state = 0.0
            last_d = None
            for rec in daily:
                d = _parse_date(rec.get(DATA_DATE, ""))
                if not d:
                    continue
                cur_state = float((rec.get(IDX) or {}).get(CUBIC_METER) or 0.0)
                if last_d:
                    gap = (d - last_d).days
                    for i in range(1, gap):
                        fill_d = last_d.fromordinal(last_d.toordinal() + i)
                        fill_dt = datetime.combine(fill_d, datetime.min.time())
                        index_stats_m3.append(
                            {"start": fill_dt, "state": last_state, "sum": total_sum}
                        )
                total_sum += cur_state
                last_state = cur_state
                last_d = d
                start_dt = datetime.combine(d, datetime.min.time())
                index_stats_m3.append(
                    {"start": start_dt, "state": cur_state, "sum": total_sum}
                )
        except Exception:
            daily_stats_liters = []
            index_stats_m3 = []

        comp = VeoliaComputed(
            last_index_m3=last_index_m3,
            last_daily_liters=last_daily_liters,
            last_daily_m3=last_daily_m3,
            monthly_latest_m3=monthly_latest_m3,
            annual_total_m3=annual_total_m3,
            last_date=last_date,
            daily_fiability=daily_fiability,
            monthly_fiability=monthly_fiability,
            daily_stats_liters=daily_stats_liters,
            index_stats_m3=index_stats_m3,
            daily_today_liters=daily_today_liters,
            daily_today_m3=daily_today_m3,
            daily_today_fiability=daily_today_fiability,
        )
        return VeoliaModel(raw=raw, computed=comp)
