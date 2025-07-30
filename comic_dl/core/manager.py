"""
DownloadManager orchestrates downloads with concurrency, proxy rotation, delay,
and automatically detects single‑chapter vs series.
"""

import os
import shutil
import time
import random
from pathlib             import Path
from concurrent.futures  import ThreadPoolExecutor, as_completed

from ..config            import RunOptions
from ..drivers.registry  import get_driver
from ..logger            import setup_logger
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

        is_series = "/title/" in opts.url
        if is_series:
            self._run_series(driver)
        else:
            chap = {
                "url":      opts.url,
                "volume":   None,
                "chapter":  None,
                "title":    None,
                "language": opts.language
            }
            self._run_single(driver, chap)

    def _run_series(self, driver):
        opts = self.options
        chapters = driver.list_chapters(opts.url)
        filtered = [c for c in chapters if c["language"] == opts.language]
        if not filtered:
            self.logger.error(f"No chapters found for language '{opts.language}'")
            return

        reverse = (opts.sort == "desc")
        filtered.sort(key=lambda c: c["chapter"], reverse=reverse)

        start = opts.start_chapter or 1
        end   = opts.end_chapter   or len(filtered)
        selected = filtered[start-1:end]

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

        meta  = driver.fetch_metadata(url)
        pages = driver.list_pages(meta)
        self.logger.info(f"Found {len(pages)} pages")

        # Determine tmp & output paths
        if "/title/" in opts.url:
            base_dir = Path(opts.output or "series")
            chap_dir = base_dir / chap["volume"] / f"Chapter_{chap['chapter']}"
            tmp_dir  = chap_dir
            out_path = chap_dir.with_suffix(f".{opts.format}")
        else:
            tmp_dir  = Path(opts.output or meta["chapter_id"]).with_suffix("")
            out_path = tmp_dir.with_suffix(f".{opts.format}")

        tmp_dir.mkdir(parents=True, exist_ok=True)

        # Concurrent downloads
        with ThreadPoolExecutor(max_workers=opts.threads) as exe:
            futures = []
            for idx, page in enumerate(pages, start=1):
                ext   = page.split(".")[-1].split("?")[0]
                dest  = tmp_dir / f"{idx:04d}.{ext}"
                proxy = random.choice(opts.proxies) if opts.proxies else None
                futures.append(
                    exe.submit(self._dl_task, driver, page, dest, proxy)
                )
            for f in as_completed(futures):
                f.result()

        # Convert to CBZ/PDF
        converter = Converter(format=opts.format)
        converter.build(sorted(tmp_dir.iterdir()), out_path)
        self.logger.info(f"Created {out_path}")

        # Cleanup raw images
        if not opts.keep_files:
            shutil.rmtree(tmp_dir)
            self.logger.debug(f"Removed temporary folder {tmp_dir}")

    def _dl_task(self, driver, page_url, dest, proxy):
        driver.download_image(page_url, dest, proxy)
        time.sleep(self.options.delay)
