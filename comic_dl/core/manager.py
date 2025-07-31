import shutil
import random
from pathlib            import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict

from ..config           import RunOptions
from ..drivers.registry import get_driver
from ..logger           import setup_logger
from ..converter.builder import Converter

class DownloadManager:
    def __init__(self, options: RunOptions):
        self.opts   = options
        self.logger = setup_logger(__name__, options.verbose, options.log_file)

    def run(self):
        driver = get_driver(self.opts.url)
        self.logger.info(f"Using driver: {driver.__class__.__name__}")

        if driver.is_series_url(self.opts.url):
            self._run_series(driver)
        else:
            self._run_single_chapter(driver)

    def _run_series(self, driver):
        opts         = self.opts

        raw_series = driver.download_series_content(self.opts.url)
        series_meta = driver.fetch_series_metadata(raw_series)

        # filter, sort, slice
        filtered = [c for c in series_meta["chapters"] if (c.get("language") or opts.language) == opts.language]
        filtered.sort(key=lambda c: c["chapter"], reverse=(opts.sort=="desc"))
        start = opts.start_chapter or 1
        end   = opts.end_chapter   or len(filtered)
        selected = filtered[start-1:end]

        for chap in selected:
            self._run_single_chapter(driver, chap["url"], series_meta["series_title"])

    def _run_single_chapter(self, driver, chapter_url = None, series_title = None):
        opts         = self.opts

        raw_chap = driver.download_chapter_content(chapter_url or self.opts.url)
        chap_meta = driver.fetch_chapter_metadata(raw_chap)

        series_title = series_title or chap_meta.get("series_title", "")
        if not chap_meta.get("series_title"):
            chap_meta["series_title"] = series_title

        self._download_task(driver, chap_meta)

    def _download_task(self, driver, chap_meta: Dict):
        opts     = self.opts
        series   = chap_meta.get("series_title","")
        chapter  = chap_meta["chapter_id"]
        pages    = chap_meta["pages"]

        root = Path(opts.output or ".")
        if series:
            root = root / series
        tmp_dir = root / chapter
        final_path = tmp_dir.with_suffix(f".{opts.format}")

        tmp_dir.mkdir(parents=True, exist_ok=True)

        with ThreadPoolExecutor(max_workers=opts.threads) as exe:
            futures = []
            for idx, url in enumerate(pages,1):
                ext = url.split(".")[-1].split("?")[0]
                dest = tmp_dir / f"{idx:04d}.{ext}"
                proxy = random.choice(opts.proxies) if opts.proxies else None
                self.logger.info(f"Downloading Image: {idx}.{ext}")
                futures.append(exe.submit(driver.download_image, url, dest, proxy))
            for f in as_completed(futures):
                pass

        Converter(format=opts.format).build(sorted(tmp_dir.iterdir()), final_path)
        if not opts.keep_files:
            shutil.rmtree(tmp_dir)

