"""
Forward dasandpartners.com form submissions into the dasandpartnersengineering.com
admin panel (server-to-server), so every lead/application lands in ONE place.

Flow: Django validates the form (same-origin, CSRF) -> this module POSTs it to the
engineering site's /api/ingest/* endpoint, authenticated by a shared secret
(X-Ingest-Token). If the engineering site is briefly unreachable, the submission is
saved to a local fallback folder so nothing is ever lost; replay with:

    python manage.py replay_leads

Config (settings / env): ENGINEERING_INGEST_URL, INGEST_TOKEN, LEADS_FALLBACK_DIR.
"""
import os
import json
import uuid
import logging
import datetime

from django.conf import settings

logger = logging.getLogger(__name__)


def _fallback_dir():
    d = getattr(settings, "LEADS_FALLBACK_DIR", None) or os.path.join(str(settings.BASE_DIR), "leads_fallback")
    os.makedirs(d, exist_ok=True)
    return d


def _save_fallback(kind, data, cv_bytes=None, cv_name=None):
    """Persist a submission locally so it can be replayed later. Returns the record id."""
    d = _fallback_dir()
    rec_id = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:8]
    rec = {
        "id": rec_id,
        "kind": kind,
        "data": data,
        "cv_name": cv_name,
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
    }
    if cv_bytes and cv_name:
        safe = "".join(c for c in cv_name if c.isalnum() or c in "._-") or "resume"
        cv_path = os.path.join(d, rec_id + "_" + safe)
        with open(cv_path, "wb") as fh:
            fh.write(cv_bytes)
        rec["cv_path"] = cv_path
    with open(os.path.join(d, rec_id + ".json"), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=2)
    logger.warning("Lead saved to local fallback (%s): %s", kind, rec_id)
    return rec_id


def _url(path):
    base = (getattr(settings, "ENGINEERING_INGEST_URL", "") or "").rstrip("/")
    return base + path


def forward_contact(data):
    """Forward a contact / project-enquiry submission. Returns (ok: bool, error: str|None)."""
    token = getattr(settings, "INGEST_TOKEN", "") or ""
    if not token:
        _save_fallback("contact", data)
        logger.error("INGEST_TOKEN not set; contact saved to fallback instead of forwarding")
        return False, "not-configured"
    try:
        import requests
        r = requests.post(_url("/api/ingest/contact"), json=data,
                          headers={"X-Ingest-Token": token}, timeout=10)
        if r.status_code == 200 and r.json().get("ok"):
            return True, None
        _save_fallback("contact", data)
        logger.error("ingest/contact failed: %s %s", r.status_code, r.text[:300])
        return False, "remote-%s" % r.status_code
    except Exception as exc:  # network error, timeout, bad JSON, etc.
        _save_fallback("contact", data)
        logger.error("ingest/contact exception: %s", exc)
        return False, str(exc)


def forward_application(data, cv_file=None):
    """Forward a job application (optional resume file). Returns (ok: bool, error: str|None)."""
    token = getattr(settings, "INGEST_TOKEN", "") or ""
    cv_bytes = cv_file.read() if cv_file else None
    cv_name = getattr(cv_file, "name", None) if cv_file else None
    if not token:
        _save_fallback("application", data, cv_bytes, cv_name)
        logger.error("INGEST_TOKEN not set; application saved to fallback instead of forwarding")
        return False, "not-configured"
    try:
        import requests
        files = None
        if cv_bytes:
            files = {"cv": (cv_name or "resume", cv_bytes,
                            getattr(cv_file, "content_type", "application/octet-stream"))}
        r = requests.post(_url("/api/ingest/application"), data=data, files=files,
                          headers={"X-Ingest-Token": token}, timeout=20)
        if r.status_code == 200 and r.json().get("ok"):
            return True, None
        _save_fallback("application", data, cv_bytes, cv_name)
        logger.error("ingest/application failed: %s %s", r.status_code, r.text[:300])
        return False, "remote-%s" % r.status_code
    except Exception as exc:
        _save_fallback("application", data, cv_bytes, cv_name)
        logger.error("ingest/application exception: %s", exc)
        return False, str(exc)
