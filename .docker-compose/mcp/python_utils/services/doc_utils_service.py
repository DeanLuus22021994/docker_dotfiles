#!/usr/bin/env python3
"""
Documentation utilities service for Docker Compose Utils project.

Enhanced for Python 3.14 with free-threaded execution,
concurrent interpreters, and improved parallelism.
"""

import asyncio
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast
from urllib.parse import urljoin

if sys.version_info >= (3, 14):
    try:
        from concurrent.futures import ProcessPoolExecutor as InterpreterPoolExecutor
        _has_interpreters = True
    except ImportError:
        InterpreterPoolExecutor = None
        _has_interpreters = False
else:
    InterpreterPoolExecutor = None
    _has_interpreters = False

try:
    import requests
except ImportError:
    requests = None

if TYPE_CHECKING:
    from requests import Session

if TYPE_CHECKING or requests:
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

from ..models.link_models import ComponentInfo, LinkResult


class DocUtils:
    """
    Enhanced documentation utilities leveraging Python 3.14 features.

    Features:
    - Free-threaded execution for true parallelism
    - Concurrent interpreters for isolated execution
    - Improved pathlib operations
    - Enhanced error handling and type safety
    """

    def __init__(self, docs_path: str = "docs", use_interpreters: bool = True) -> None:
        self.docs_path = Path(docs_path)
        self.base_url = "https://user.github.io/docker-examples/"
        self.use_interpreters = use_interpreters and _has_interpreters

        if requests:
            self.session: Session | None = requests.Session()
            retry_strategy = Retry(
                total=3, status_forcelist=[429, 500, 502, 503, 504], backoff_factor=1
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)
        else:
            self.session = None

    def find_markdown_files(self) -> list[Path]:
        return list(self.docs_path.rglob("*.md"))

    def extract_links(self, file_path: Path) -> list[str]:
        links: list[str] = []
        try:
            content = file_path.read_text(encoding="utf-8")

            md_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            for _, url in md_links:
                if not url.startswith(("http://", "https://", "#")):
                    links.append(urljoin(self.base_url, url))
                else:
                    links.append(url)

            html_links = re.findall(r'href=["\']([^"\']+)["\']', content)
            for url in html_links:
                if url.startswith(("http://", "https://")):
                    links.append(url)

        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)

        return list(set(links))

    def check_links_concurrent(self, max_workers: int = 10) -> dict[str, list[str]]:
        results: dict[str, list[str]] = {"valid": [], "broken": [], "skipped": []}

        md_files = self.find_markdown_files()
        all_links: set[str] = set()

        for file_path in md_files:
            links = self.extract_links(file_path)
            all_links.update(links)

        print(f"🔍 Found {len(all_links)} unique links to check...")

        if not all_links:
            return results

        from concurrent.futures import ProcessPoolExecutor

        executor_class: type[ThreadPoolExecutor] | type[ProcessPoolExecutor]
        if self.use_interpreters and _has_interpreters and InterpreterPoolExecutor is not None:
            print("🚀 Using InterpreterPoolExecutor for true parallelism")
            executor_class = InterpreterPoolExecutor
        else:
            print("⚡ Using ThreadPoolExecutor for concurrent execution")
            executor_class = ThreadPoolExecutor

        with executor_class(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self._check_single_link, url) for url in all_links
            ]

            for future in as_completed(futures):
                result: LinkResult = future.result()
                if result.error_message and "skipped" in result.error_message:
                    results["skipped"].append(result.url)
                elif result.is_valid:
                    results["valid"].append(result.url)
                else:
                    status_info = (
                        f" (status: {result.status_code})" if result.status_code else ""
                    )
                    results["broken"].append(f"{result.url}{status_info}")

        return results

    def _check_single_link(self, url: str) -> LinkResult:
        import time

        start_time = time.time()

        try:
            if any(
                skip_domain in url
                for skip_domain in ["localhost", "127.0.0.1", "0.0.0.0"]
            ):
                return LinkResult(
                    url=url,
                    is_valid=True,
                    error_message="skipped",
                    response_time=time.time() - start_time,
                )

            if not self.session:
                return LinkResult(
                    url=url,
                    is_valid=False,
                    error_message="requests not available",
                    response_time=time.time() - start_time,
                )

            response = self.session.head(url, timeout=10, allow_redirects=True)

            if response.status_code == 405:
                response = self.session.get(url, timeout=10, allow_redirects=True)

            return LinkResult(
                url=url,
                is_valid=response.status_code < 400,
                status_code=response.status_code,
                response_time=time.time() - start_time,
            )

        except Exception as e:
            return LinkResult(
                url=url,
                is_valid=False,
                error_message=str(e),
                response_time=time.time() - start_time,
            )

    def generate_component_inventory(
        self, src_path: str = "src"
    ) -> dict[str, list[dict[str, Any]]]:
        components: dict[str, list[dict[str, Any]]] = {
            "pages": [],
            "components": [],
            "hooks": [],
            "utils": [],
        }

        src_dir = Path(src_path)

        extensions = ["*.jsx", "*.js", "*.tsx", "*.ts"]
        component_files: list[Path] = []
        for ext in extensions:
            component_files.extend(src_dir.rglob(ext))

        for file_path in component_files:
            try:
                relative_path = file_path.relative_to(src_dir)
                content = file_path.read_text(encoding="utf-8")
                size_bytes = file_path.stat().st_size

                category = self._determine_category(str(relative_path))

                component_info = self._extract_component_info(
                    content, file_path, category
                )

                if component_info:
                    component_info.size_bytes = size_bytes
                    components[category].append(component_info.to_dict())

            except Exception as e:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)

        return components

    def _determine_category(self, relative_path: str) -> str:
        path_lower = relative_path.lower()

        if "page" in path_lower or "screen" in path_lower:
            return "pages"
        elif "hook" in path_lower:
            return "hooks"
        elif "util" in path_lower or "helper" in path_lower:
            return "utils"
        else:
            return "components"

    def _extract_component_info(
        self, content: str, file_path: Path, category: str
    ) -> ComponentInfo | None:
        component_name = self._extract_component_name(content, file_path.name)

        exports = self._extract_exports(content)

        imports = self._extract_imports(content)

        return ComponentInfo(
            name=component_name,
            file=str(file_path.relative_to(file_path.parents[2])),
            path=str(file_path),
            category=category,
            exports=exports,
            imports=imports,
            size_bytes=0,
        )

    def _extract_component_name(self, content: str, filename: str) -> str:
        patterns = [
            r"export default (\w+)",
            r"export \{ default as (\w+) \}",
            r"(?:export )?(?:const|function|class) (\w+)",
            r"module\.exports = (\w+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)

        return (
            filename.replace(".jsx", "")
            .replace(".js", "")
            .replace(".tsx", "")
            .replace(".ts", "")
        )

    def _extract_exports(self, content: str) -> list[str]:
        exports: list[str] = []

        named_exports = re.findall(
            r"export (?:const|function|class|let|var) (\w+)", content
        )
        exports.extend(named_exports)

        export_statements = re.findall(r"export \{([^}]+)\}", content)
        for statement in export_statements:
            items = [item.split(" as ")[0].strip() for item in statement.split(",")]
            exports.extend(items)

        return list(set(exports))

    def _extract_imports(self, content: str) -> list[str]:
        imports: list[str] = []

        es6_imports = re.findall(r'import .* from ["\']([^"\']+)["\']', content)
        imports.extend(es6_imports)

        cjs_imports = re.findall(r'require\(["\']([^"\']+)["\']', content)
        imports.extend(cjs_imports)

        return list(set(imports))

    def copy_file(self, src: Path, dst: Path, follow_symlinks: bool = True) -> bool:
        try:
            if hasattr(src, "copy"):
                src.copy(dst, follow_symlinks=follow_symlinks)
            else:
                import shutil

                shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
            return True
        except Exception as e:
            print(f"Error copying {src} to {dst}: {e}", file=sys.stderr)
            return False

    def move_file(self, src: Path, dst: Path) -> bool:
        try:
            if hasattr(src, "move"):
                src.move(dst)
            else:
                import shutil

                shutil.move(src, dst)
            return True
        except Exception as e:
            print(f"Error moving {src} to {dst}: {e}", file=sys.stderr)
            return False

    async def async_check_links(
        self, urls: list[str], max_concurrency: int = 10
    ) -> dict[str, list[str]]:
        results: dict[str, list[str]] = {"valid": [], "broken": [], "skipped": []}

        if not self.session:
            results["broken"] = [f"{url} (requests not available)" for url in urls]
            return results

        semaphore = asyncio.Semaphore(max_concurrency)

        assert self.session is not None

        async def check_single_url(url: str) -> tuple[str, bool, str]:
            async with semaphore:
                try:
                    if any(
                        skip_domain in url
                        for skip_domain in ["localhost", "127.0.0.1", "0.0.0.0"]
                    ):
                        return url, True, "skipped"

                    session = cast(Session, self.session)
                    response = await asyncio.to_thread(
                        session.head, url, timeout=10, allow_redirects=True
                    )

                    if response.status_code == 405:
                        response = await asyncio.to_thread(
                            session.get, url, timeout=10, allow_redirects=True
                        )

                    return (
                        url,
                        response.status_code < 400,
                        f"status: {response.status_code}",
                    )

                except Exception as e:
                    return url, False, str(e)

        tasks = [check_single_url(url) for url in urls]
        completed_results: list[tuple[str, bool, str] | BaseException] = await asyncio.gather(*tasks, return_exceptions=True)

        for result in completed_results:
            if isinstance(result, BaseException):
                print(f"Async task error: {result}", file=sys.stderr)
                continue

            url, is_valid, reason = result
            if "skipped" in reason:
                results["skipped"].append(url)
            elif is_valid:
                results["valid"].append(url)
            else:
                results["broken"].append(f"{url} ({reason})")

        return results