thonimport json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

logger = logging.getLogger(__name__)

class JSONExporter:
    """Export scraped products to a JSON file."""

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("Output directory ensured at %s", self.output_dir)

    def export(self, products: Iterable[Dict[str, Any]], filename_prefix: str) -> Path:
        products_list: List[Dict[str, Any]] = list(products)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        output_path = self.output_dir / filename

        logger.info(
            "Writing %d product(s) to %s",
            len(products_list),
            output_path,
        )

        try:
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(
                    products_list,
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
        except OSError as exc:  # noqa: BLE001
            logger.exception("Failed to write output file %s: %s", output_path, exc)
            raise

        return output_path