"""
DownloadManager orchestrates single‑chapter and full‑series downloads,
deciding mode automatically based on the URL pattern.
"""

import os
import shutil
from pathlib    import Path
from ..config   import RunOptions
from ..drivers.registry import get_driver
from ..logger   import setup_logger
from ..converter.builder import Converter

class DownloadManager:
    def __init__(self, options: RunOptions):
        self.options = options
        self.logger  = setup_logger(
            __name__, options.verbose, options.log_file
        )

    def run(self):
        opts   = self.options
        driver = get_driver(opts.url)
        self.logger.info(f"Using driver: {driver.__class__.__name__}")

        # Decide mode by URL: '/title/' ⇒ full series, '/chapter/' ⇒ single
        is_series = "/title/" in opts.url

        if is_series:
            self._run_series(driver)
        else:
            self._run_single(driver, {
                "url":      opts.url,
                "volume":   None,
                "chapter":  None,
                "title":    None,
                "language": opts.language
            })

    def _run_series(self, driver):
        opts = self.options
        # 1) fetch ALL chapters via API_AGGREGATE
        chapters = driver.list_chapters(self.options.url)

        # 2) filter by language
        filtered = [c for c in chapters if c["language"] == opts.language]
        if not filtered:
            self.logger.error(f"No chapters found for language '{opts.language}'")
            return

        # 3) sort
        reverse = (opts.sort == "desc")
        filtered.sort(key=lambda c: c["chapter"], reverse=reverse)

        # 4) slice by start/end
        start = opts.start_chapter or 1
        end   = opts.end_chapter   or len(filtered)
        selected = filtered[start - 1 : end]

        self.logger.info(
            f"Downloading chapters {start}–{end} of {len(filtered)} "
            f"(lang={opts.language}, sorted={opts.sort})"
        )
        for chap in selected:
            self._run_single(driver, chap)

    def _run_single(self, driver, chap: dict):
        opts = self.options
        url  = chap["url"]
        self.logger.info(f"Processing: {url}")

        # fetch metadata & pages
        meta  = driver.fetch_metadata(url)
        pages = driver.list_pages(meta)
        self.logger.info(f"Found {len(pages)} pages")

        # determine paths
        if "/title/" in opts.url:
            # series mode output
            base_dir = Path(opts.output or "series")
            chap_dir = base_dir / chap["volume"] / f"Chapter_{chap['chapter']}"
            tmp_dir  = chap_dir
            out_path = chap_dir.with_suffix(f".{opts.format}")
        else:
            # single-chapter mode
            tmp_dir  = Path(opts.output or meta["chapter_id"]).with_suffix("")
            out_path = tmp_dir.with_suffix(f".{opts.format}")

        tmp_dir.mkdir(parents=True, exist_ok=True)

        # download pages
        for idx, page in enumerate(pages, start=1):
            ext  = page.split(".")[-1].split("?")[0]
            dest = tmp_dir / f"{idx:04d}.{ext}"
            self.logger.debug(f"Downloading {page} → {dest}")
            driver.download_image(page, dest)

        # convert
        converter = Converter(format=opts.format)
        converter.build(sorted(tmp_dir.iterdir()), out_path)
        self.logger.info(f"Created {out_path}")

        # cleanup raw images
        if not opts.keep_files:
            shutil.rmtree(tmp_dir)
            self.logger.debug(f"Removed temporary folder {tmp_dir}")
