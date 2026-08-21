from whitenoise.storage import CompressedManifestStaticFilesStorage


class LenientManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """
    Same as CompressedManifestStaticFilesStorage, but a {% static %} reference
    to a file missing from the manifest resolves to its plain (unhashed) URL
    instead of raising ValueError and crashing the whole page.

    This site accumulates numbered project/gallery folders (e.g. work/22,
    life/6.jpeg) whose templates sometimes reference photos that were never
    uploaded. Under strict mode that turns a missing photo into a 500 for the
    entire page; leniently, it's just a broken image icon, matching the
    behavior the site already had before switching to manifest storage.
    """

    manifest_strict = False

    def stored_name(self, name):
        # manifest_strict=False only covers files that exist on disk but are
        # absent from a stale manifest (it falls back to hashing them fresh).
        # A file that's missing from disk entirely still raises ValueError
        # from that fallback, so fall back further here: serve it unhashed.
        try:
            return super().stored_name(name)
        except ValueError:
            return name
