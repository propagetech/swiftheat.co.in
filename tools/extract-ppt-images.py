#!/usr/bin/env python3
"""Extract PowerPoint media unchanged and create its website placement map."""

from __future__ import annotations

import hashlib
import json
import posixpath
import re
import zipfile
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree

try:
    from PIL import Image
except ImportError:
    Image = None


ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "anotherpptanddocuments" / "web 2.pptx"
OUTPUT_DIRECTORY = ROOT / "imgs" / "ppt-originals"
MAPPING_PATH = ROOT / "data" / "ppt-image-mapping.json"

SEO_NAMES = [
    "swiftheat-technician-electrical-workbench.jpeg",
    "swiftheat-homepage-design-reference.png",
    "swiftheat-factory-photo-collage.png",
    "swiftheat-workshop-cctv-overview.png",
    "strip-heaters-page-design-reference.png",
    "strip-heater-product-range.jpg",
    "strip-heaters-configurator-design-reference.png",
    "strip-heaters-options-design-reference.png",
    "strip-heater-construction-terminal.jpg",
    "finned-strip-heater.jpg",
    "strip-heater-terminal-options.png",
    "mica-strip-heater-with-lead-wires.png",
    "strip-heater-selection-guide-design-reference.png",
    "strip-heater-product-family.jpg",
    "strip-heaters-unused-page-reference.png",
    "tubular-heaters-page-design-reference.png",
    "tubular-heater-product-range.png",
    "tubular-heater-applications-design-reference.png",
    "tubular-heater-bend-shapes.png",
    "tubular-heater-specifications-design-reference.png",
    "tubular-heater-configurator-design-reference.png",
    "tubular-heater-options-design-reference.png",
    "straight-tubular-heater.png",
    "u-shaped-tubular-heater.jpg",
    "m-shaped-tubular-heater.jpg",
    "coiled-tubular-heater.jpg",
    "tubular-heater-options-gallery-reference.png",
    "tubular-heater-selection-guide-design-reference.png",
    "bent-u-tubular-heater.jpg",
    "m-shaped-tubular-heater-dark.jpg",
    "tubular-heater-elements-comparison.png",
    "flanged-immersion-tubular-heater.jpg",
    "tubular-heaters-unused-page-reference.png",
    "temperature-sensors-page-design-reference.png",
    "thermocouple-temperature-sensor-range.jpg",
    "temperature-sensor-applications-design-reference.png",
    "industrial-temperature-sensor-range.jpg",
    "thermocouple-probe-assemblies.png",
    "temperature-sensor-specifications-design-reference.png",
    "temperature-sensor-selection-guide-reference.png",
    "thermocouple-selection-chart.gif",
    "temperature-sensor-downloads-design-reference.png",
    "ceramic-infrared-heaters-page-design-reference.png",
    "ceramic-infrared-heater-elements.jpeg",
    "infrared-heater-applications-design-reference.png",
    "ceramic-infrared-heater-panel-elements.jpg",
    "ceramic-infrared-flat-panel-heater.jpg",
    "infrared-heater-specifications-design-reference.png",
    "infrared-heater-selection-guide-reference.png",
    "ceramic-infrared-heater-product-range.png",
    "infrared-heater-downloads-design-reference.png",
    "swiftheat-capabilities-page-design-reference.png",
    "industrial-heating-element-product-range.png",
    "swiftheat-capabilities-specification-reference.png",
    "swiftheat-engineering-page-design-reference.png",
    "heater-manufacturing-process-collage.png",
    "swiftheat-quality-page-design-reference.png",
    "industrial-quality-assurance-concept.jpeg",
    "swiftheat-quality-testing-design-reference.png",
    "swiftheat-quality-traceability-design-reference.png",
    "swiftheat-quality-certifications-design-reference.png",
    "swiftheat-resources-page-design-reference.png",
    "swiftheat-works-gallery-design-reference.png",
    "swiftheat-wire-winding-machine-operator.jpeg",
    "swiftheat-lathe-machine-operator.jpeg",
    "swiftheat-office-customer-support.jpeg",
    "swiftheat-engineering-design-workstation.jpeg",
    "swiftheat-heater-testing-workshop.jpeg",
    "swiftheat-peenya-factory-entrance.jpeg",
    "swiftheat-contact-page-design-reference.png",
    "swiftheat-about-page-design-reference.png",
    "swiftheat-factory-cctv-overview-reference.png",
    "swiftheat-company-facts-design-reference.png",
    "swiftheat-mission-values-design-reference.png",
    "swiftheat-bengaluru-location-map.jpeg",
]

SLIDE_PAGES = {
    1: ["index.html"],
    2: ["products/strip-heaters/index.html"],
    3: ["products/strip-heaters/index.html"],
    4: ["products/strip-heaters/index.html"],
    5: ["products/strip-heaters/index.html"],
    6: ["products/strip-heaters/index.html"],
    7: ["products/tubular-heaters/index.html"],
    8: ["products/tubular-heaters/index.html"],
    9: ["products/tubular-heaters/index.html"],
    10: ["products/tubular-heaters/index.html"],
    11: ["products/tubular-heaters/index.html"],
    12: ["products/tubular-heaters/index.html"],
    13: ["products/tubular-heaters/index.html"],
    14: ["products/tubular-heaters/index.html"],
    15: ["products/thermocouples-and-sensors/index.html"],
    16: ["products/thermocouples-and-sensors/index.html"],
    17: ["products/thermocouples-and-sensors/index.html"],
    18: ["products/thermocouples-and-sensors/index.html"],
    19: ["products/thermocouples-and-sensors/index.html"],
    20: ["products/ceramic-infrared-heaters/index.html"],
    21: ["products/ceramic-infrared-heaters/index.html"],
    22: ["products/ceramic-infrared-heaters/index.html"],
    23: ["products/ceramic-infrared-heaters/index.html"],
    24: ["products/ceramic-infrared-heaters/index.html"],
    25: ["products/ceramic-infrared-heaters/index.html"],
    26: ["capabilities/index.html"],
    27: ["quality/index.html"],
    28: ["quality/index.html"],
    29: ["quality/index.html"],
    30: ["quality/index.html"],
    31: ["quality/index.html"],
    32: ["resources/index.html"],
    33: ["resources/index.html"],
    34: ["contact/index.html"],
    35: ["about/index.html"],
    36: ["about/index.html"],
    37: ["about/index.html", "contact/index.html"],
}

PLACEMENTS = {
    1: [("index.html", ".hero-dark .shot img", "source for homepage works collage")],
    3: [
        ("index.html", ".hero-dark .shot img", "source for homepage works collage"),
        ("about/index.html", ".hero .shot img", "source for about-page works collage"),
    ],
    6: [("products/strip-heaters/index.html", ".hero .figure-photo img", "hero product range")],
    9: [("products/strip-heaters/index.html", "#construction img", "construction detail")],
    10: [("products/strip-heaters/index.html", "#options .opts li:nth-child(2) .optshot", "finned profile option")],
    11: [("products/strip-heaters/index.html", "#options .opts li:nth-child(1) .optshot", "plain profile option")],
    12: [("products/strip-heaters/index.html", "#options .optgroup:nth-of-type(2)", "flying-lead termination option")],
    14: [("products/strip-heaters/index.html", "#selection img", "selection product family")],
    17: [("products/tubular-heaters/index.html", ".hero .figure-photo img", "hero product range")],
    19: [("products/tubular-heaters/index.html", "#options", "bend-form visual guide")],
    23: [("products/tubular-heaters/index.html", "#options .opts li:nth-child(1) .optshot", "straight bend form")],
    24: [("products/tubular-heaters/index.html", "#options .opts li:nth-child(2) .optshot", "U bend form")],
    25: [("products/tubular-heaters/index.html", "#options .opts li:nth-child(3) .optshot", "M bend form alternate")],
    26: [("products/tubular-heaters/index.html", "#options .opts li:nth-child(4) .optshot", "coiled form alternate")],
    29: [("products/tubular-heaters/index.html", "#selection img", "selection-guide source")],
    30: [("products/tubular-heaters/index.html", "#options .opts li:nth-child(3) .optshot", "M bend form")],
    31: [("products/tubular-heaters/index.html", "#selection img", "selection comparison source")],
    32: [("products/tubular-heaters/index.html", "#options .opts li:nth-child(4) .optshot", "flanged or coiled form")],
    35: [("products/thermocouples-and-sensors/index.html", ".hero .figure-photo img", "hero sensor range")],
    37: [("products/thermocouples-and-sensors/index.html", "#construction img", "sensor family source")],
    38: [("products/thermocouples-and-sensors/index.html", "#construction img", "probe construction source")],
    41: [("products/thermocouples-and-sensors/index.html", "#selection img", "selection chart")],
    44: [("products/ceramic-infrared-heaters/index.html", ".hero .figure-photo img", "hero infrared range")],
    46: [("products/ceramic-infrared-heaters/index.html", "#construction img", "construction product family")],
    47: [("products/ceramic-infrared-heaters/index.html", "#options .optshot img", "flat-panel option")],
    50: [("products/ceramic-infrared-heaters/index.html", "#selection img", "selection product range")],
    53: [("capabilities/index.html", ".hero .shot img", "capabilities hero product range")],
    56: [("capabilities/index.html", ".band img", "engineering process collage")],
    64: [("resources/index.html", ".three .shot:nth-child(2) img", "wire-winding operator")],
    65: [
        ("resources/index.html", ".hero .shot img", "resources hero"),
        ("resources/index.html", ".three .shot:nth-child(1) img", "lathe operator"),
    ],
    66: [("resources/index.html", ".three .shot:nth-child(3) img", "office support")],
    67: [("resources/index.html", ".three .shot:nth-child(4) img", "engineering workstation")],
    68: [("resources/index.html", ".three .shot:nth-child(5) img", "heater testing workshop")],
    69: [
        ("resources/index.html", ".three .shot:nth-child(6) img", "factory entrance"),
        ("contact/index.html", ".shot img", "factory entrance"),
    ],
    75: [("contact/index.html", ".shot", "location reference; use as a linked image only if desired")],
}


def get_slide_media(archive: zipfile.ZipFile) -> tuple[dict[str, list[int]], dict[int, str]]:
    media_slides: dict[str, list[int]] = {}
    slide_notes: dict[int, str] = {}
    namespace = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    relationship_tag = "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"

    for slide_number in range(1, 38):
        slide_path = f"ppt/slides/slide{slide_number}.xml"
        slide_root = ElementTree.fromstring(archive.read(slide_path))
        slide_notes[slide_number] = " | ".join(
            node.text.strip()
            for node in slide_root.findall(".//a:t", namespace)
            if node.text and node.text.strip()
        )
        relationship_path = f"ppt/slides/_rels/slide{slide_number}.xml.rels"
        relationship_root = ElementTree.fromstring(archive.read(relationship_path))
        for relationship in relationship_root.findall(relationship_tag):
            target = relationship.attrib.get("Target", "")
            if "/media/" in target:
                media_slides.setdefault(posixpath.basename(target), []).append(slide_number)

    return media_slides, slide_notes


def get_dimensions(data: bytes) -> tuple[int | None, int | None]:
    if Image is None:
        return None, None

    with Image.open(BytesIO(data)) as image:
        return image.width, image.height


def get_media_number(path: str) -> int:
    match = re.search(r"image(\d+)", path)
    if match is None:
        raise ValueError(f"Unexpected media filename: {path}")

    return int(match.group(1))


def main() -> None:
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    MAPPING_PATH.parent.mkdir(parents=True, exist_ok=True)
    html_pages = sorted({page for pages in SLIDE_PAGES.values() for page in pages})
    html_content = {
        page: (ROOT / page).read_text(encoding="utf-8")
        for page in html_pages
        if (ROOT / page).is_file()
    }

    with zipfile.ZipFile(PRESENTATION) as archive:
        media_paths = sorted(
            (path for path in archive.namelist() if path.startswith("ppt/media/")),
            key=get_media_number,
        )
        if len(media_paths) != len(SEO_NAMES):
            raise ValueError(f"Expected {len(SEO_NAMES)} media files, found {len(media_paths)}")

        media_slides, slide_notes = get_slide_media(archive)
        records = []

        for media_path, seo_name in zip(media_paths, SEO_NAMES, strict=True):
            media_number = get_media_number(media_path)
            data = archive.read(media_path)
            output_path = OUTPUT_DIRECTORY / seo_name
            output_path.write_bytes(data)
            width, height = get_dimensions(data)
            slides = media_slides.get(Path(media_path).name, [])
            placements = [
                {"html": html, "selector": selector, "purpose": purpose}
                for html, selector, purpose in PLACEMENTS.get(media_number, [])
            ]
            role = "page-reference" if "reference" in seo_name else "content-image"

            records.append(
                {
                    "source": media_path,
                    "file": output_path.relative_to(ROOT).as_posix(),
                    "role": role,
                    "width": width,
                    "height": height,
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "slides": slides,
                    "slideNotes": [slide_notes[slide] for slide in slides if slide_notes[slide]],
                    "relatedHtml": sorted({page for slide in slides for page in SLIDE_PAGES.get(slide, [])}),
                    "integratedHtml": [
                        page for page, content in html_content.items() if seo_name in content
                    ],
                    "suggestedPlacements": placements,
                    "altText": seo_name.rsplit(".", 1)[0].replace("-", " ") if role == "content-image" else "",
                }
            )

    mapping = {
        "sourcePresentation": PRESENTATION.relative_to(ROOT).as_posix(),
        "preservation": "Files in imgs/ppt-originals are byte-for-byte copies of embedded PowerPoint media.",
        "usageNote": "Use content-image records for HTML. Page-reference records are review screenshots and should not be published as page imagery.",
        "integrationNote": "integratedHtml lists pages currently using each original; suggestedPlacements records other reviewed slots.",
        "count": len(records),
        "images": records,
    }
    MAPPING_PATH.write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {len(records)} original images to {OUTPUT_DIRECTORY.relative_to(ROOT)}")
    print(f"Wrote mapping to {MAPPING_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
