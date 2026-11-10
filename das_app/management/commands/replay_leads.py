"""
Re-forward lead submissions that were saved locally (because the engineering admin
was briefly unreachable) back into the dasandpartnersengineering.com admin panel.

    python manage.py replay_leads

Reads das_app/ingest.py's fallback folder (LEADS_FALLBACK_DIR); on a successful
forward the local copy (and any resume file) is deleted. Safe to run repeatedly, e.g.
from cron.
"""
import os
import glob
import json

import requests
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Re-forward locally-saved leads to the engineering admin (/api/ingest/*)."

    def handle(self, *args, **options):
        d = getattr(settings, "LEADS_FALLBACK_DIR", None) or os.path.join(str(settings.BASE_DIR), "leads_fallback")
        token = getattr(settings, "INGEST_TOKEN", "") or ""
        base = (getattr(settings, "ENGINEERING_INGEST_URL", "") or "").rstrip("/")
        if not token:
            self.stderr.write("INGEST_TOKEN is not set — cannot replay.")
            return
        files = sorted(glob.glob(os.path.join(d, "*.json")))
        if not files:
            self.stdout.write("No pending leads to replay.")
            return

        sent = failed = 0
        for fp in files:
            try:
                with open(fp, encoding="utf-8") as fh:
                    rec = json.load(fh)
            except Exception as exc:
                self.stderr.write(f"skip {os.path.basename(fp)}: {exc}")
                failed += 1
                continue

            kind = rec.get("kind")
            data = rec.get("data", {}) or {}
            cv_path = rec.get("cv_path")
            fh_cv = None
            try:
                if kind == "application":
                    files_arg = None
                    if cv_path and os.path.exists(cv_path):
                        fh_cv = open(cv_path, "rb")
                        files_arg = {"cv": (rec.get("cv_name") or "resume", fh_cv)}
                    r = requests.post(base + "/api/ingest/application", data=data, files=files_arg,
                                      headers={"X-Ingest-Token": token}, timeout=20)
                else:
                    r = requests.post(base + "/api/ingest/contact", json=data,
                                      headers={"X-Ingest-Token": token}, timeout=15)
                ok = (r.status_code == 200 and r.json().get("ok"))
            except Exception as exc:
                ok = False
                self.stderr.write(f"{os.path.basename(fp)}: {exc}")
            finally:
                if fh_cv:
                    fh_cv.close()

            if ok:
                sent += 1
                for p in (fp, cv_path):
                    if p and os.path.exists(p):
                        try:
                            os.remove(p)
                        except OSError:
                            pass
            else:
                failed += 1
                self.stderr.write(f"still failing: {os.path.basename(fp)}")

        self.stdout.write(self.style.SUCCESS(f"Replay complete. sent={sent} failed={failed}"))
