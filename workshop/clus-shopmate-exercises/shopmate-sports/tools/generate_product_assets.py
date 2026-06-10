#!/usr/bin/env python3
"""Generate local product artwork for the ShopMate Sports demo app."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


APP_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = APP_DIR / "static" / "assets" / "products"

PRODUCTS = [
    {
        "id": "roadflow-880",
        "name": "RoadFlow 880",
        "kind": "shoe",
        "base": "#1f2937",
        "accent": "#02b8df",
        "highlight": "#ffffff",
        "bg1": "#dbeafe",
        "bg2": "#f8fafc",
    },
    {
        "id": "paceforge-racer",
        "name": "PaceForge Racer",
        "kind": "shoe",
        "base": "#121826",
        "accent": "#c8ff00",
        "highlight": "#0a60ff",
        "bg1": "#dcfce7",
        "bg2": "#f7fee7",
    },
    {
        "id": "trailridge-gtx",
        "name": "TrailRidge GTX",
        "kind": "shoe",
        "base": "#24523a",
        "accent": "#b46a3c",
        "highlight": "#111418",
        "bg1": "#d9f99d",
        "bg2": "#f7fee7",
    },
    {
        "id": "studio-knit",
        "name": "StudioKnit Trainer",
        "kind": "shoe",
        "base": "#27324a",
        "accent": "#d5778a",
        "highlight": "#eee5d5",
        "bg1": "#fce7f3",
        "bg2": "#fff7ed",
    },
    {
        "id": "courtline-rally",
        "name": "CourtLine Rally",
        "kind": "shoe",
        "base": "#f8fafc",
        "accent": "#1f7a54",
        "highlight": "#1c2c46",
        "bg1": "#dcfce7",
        "bg2": "#f8fafc",
    },
    {
        "id": "cloudrest-slide",
        "name": "CloudRest Slide",
        "kind": "slide",
        "base": "#111418",
        "accent": "#0a60ff",
        "highlight": "#f8fafc",
        "bg1": "#e0f2fe",
        "bg2": "#f8fafc",
    },
    {
        "id": "aeromesh-tee",
        "name": "AeroMesh Training Tee",
        "kind": "tee",
        "base": "#111418",
        "accent": "#02b8df",
        "highlight": "#f8fafc",
        "bg1": "#dbeafe",
        "bg2": "#f8fafc",
    },
    {
        "id": "stride-short",
        "name": "Stride 5 Inch Short",
        "kind": "short",
        "base": "#e4006d",
        "accent": "#0a60ff",
        "highlight": "#111418",
        "bg1": "#fce7f3",
        "bg2": "#e0f2fe",
    },
    {
        "id": "summit-pack",
        "name": "Summit Day Pack",
        "kind": "pack",
        "base": "#1f2937",
        "accent": "#f28c28",
        "highlight": "#687484",
        "bg1": "#ffedd5",
        "bg2": "#e0f2fe",
    },
    {
        "id": "tempo-cap",
        "name": "Tempo Run Cap",
        "kind": "cap",
        "base": "#f8fafc",
        "accent": "#0a60ff",
        "highlight": "#111418",
        "bg1": "#dbeafe",
        "bg2": "#f8fafc",
    },
]


def background(product: dict[str, str]) -> str:
    return f"""
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{product['bg1']}"/>
      <stop offset="1" stop-color="{product['bg2']}"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="22" stdDeviation="18" flood-color="#111418" flood-opacity="0.18"/>
    </filter>
  </defs>
  <rect width="900" height="640" fill="url(#bg)"/>
  <path d="M0 512 C170 470 273 596 446 522 C604 456 715 402 900 452 L900 640 L0 640 Z" fill="#ffffff" opacity="0.65"/>
  <circle cx="748" cy="132" r="94" fill="{product['accent']}" opacity="0.16"/>
  <circle cx="138" cy="142" r="62" fill="{product['highlight']}" opacity="0.20"/>
"""


def label(product: dict[str, str]) -> str:
    return f"""
  <text x="56" y="568" fill="#111418" font-family="Arial, Helvetica, sans-serif" font-size="31" font-weight="800">{escape(product['name'])}</text>
  <text x="56" y="604" fill="#5e6874" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700">ShopMate Sports</text>
"""


def shoe(product: dict[str, str]) -> str:
    base = product["base"]
    accent = product["accent"]
    highlight = product["highlight"]
    return f"""
  <g filter="url(#shadow)" transform="translate(88 160)">
    <path d="M102 256 C150 178 242 126 353 118 C454 111 532 145 595 199 C639 236 686 257 735 266 C742 323 698 361 625 363 L159 363 C90 360 59 319 102 256 Z" fill="{base}"/>
    <path d="M151 280 C207 222 288 193 393 194 C491 195 553 228 617 278 C509 306 316 318 151 280 Z" fill="{accent}" opacity="0.9"/>
    <path d="M90 329 C207 354 519 363 734 320 C760 343 743 388 680 399 C533 425 263 424 98 396 C43 386 40 341 90 329 Z" fill="#f8fafc"/>
    <path d="M106 376 C252 405 533 405 694 377" fill="none" stroke="#111418" stroke-width="9" stroke-linecap="round" opacity="0.72"/>
    <path d="M201 239 L313 207 M236 262 L352 224 M282 276 L392 236" stroke="{highlight}" stroke-width="11" stroke-linecap="round" opacity="0.92"/>
    <path d="M552 199 C580 231 614 254 657 267" fill="none" stroke="{highlight}" stroke-width="13" stroke-linecap="round" opacity="0.75"/>
    <path d="M131 402 L157 430 M220 410 L245 442 M313 414 L338 446 M407 415 L431 447 M501 412 L526 442 M599 404 L626 432" stroke="#111418" stroke-width="8" stroke-linecap="round" opacity="0.7"/>
  </g>
"""


def slide(product: dict[str, str]) -> str:
    return f"""
  <g filter="url(#shadow)" transform="translate(110 184)">
    <path d="M128 267 C226 234 491 233 649 263 C704 274 726 312 706 350 C686 389 620 408 514 408 L162 408 C80 406 50 348 79 309 C90 294 106 280 128 267 Z" fill="#f8fafc"/>
    <path d="M133 314 C272 349 514 346 678 313" fill="none" stroke="#111418" stroke-width="12" stroke-linecap="round" opacity="0.75"/>
    <path d="M216 204 C326 148 506 148 606 210 C630 225 638 256 624 283 C515 254 331 253 201 284 C184 255 190 218 216 204 Z" fill="{product['base']}"/>
    <path d="M261 231 C350 202 474 202 570 233" fill="none" stroke="{product['accent']}" stroke-width="18" stroke-linecap="round"/>
    <path d="M199 290 C321 260 512 259 638 288" fill="none" stroke="{product['highlight']}" stroke-width="8" stroke-linecap="round" opacity="0.68"/>
  </g>
"""


def tee(product: dict[str, str]) -> str:
    return f"""
  <g filter="url(#shadow)" transform="translate(224 92)">
    <path d="M146 55 L226 94 L306 55 L439 140 L380 232 L334 208 L334 481 L118 481 L118 208 L72 232 L13 140 Z" fill="{product['base']}"/>
    <path d="M146 55 C177 106 274 106 306 55 L275 40 C250 58 202 58 177 40 Z" fill="{product['accent']}"/>
    <path d="M144 182 L306 182 M144 236 L306 236 M144 290 L306 290 M144 344 L306 344" stroke="{product['accent']}" stroke-width="9" stroke-linecap="round" opacity="0.55"/>
    <path d="M122 208 L72 232 L37 178 M330 208 L380 232 L415 178" stroke="{product['highlight']}" stroke-width="8" stroke-linecap="round" opacity="0.75"/>
  </g>
"""


def short(product: dict[str, str]) -> str:
    return f"""
  <g filter="url(#shadow)" transform="translate(216 126)">
    <path d="M86 62 L392 62 L430 414 L288 414 L241 238 L196 414 L49 414 Z" fill="{product['base']}"/>
    <path d="M86 62 L392 62 L383 141 L94 141 Z" fill="#111418" opacity="0.88"/>
    <path d="M241 238 L241 86" stroke="{product['accent']}" stroke-width="10" stroke-linecap="round"/>
    <path d="M99 174 C144 196 186 196 225 174 M257 174 C307 197 352 197 389 174" fill="none" stroke="{product['highlight']}" stroke-width="8" stroke-linecap="round" opacity="0.78"/>
    <path d="M98 99 L378 99" stroke="{product['accent']}" stroke-width="8" stroke-linecap="round"/>
  </g>
"""


def pack(product: dict[str, str]) -> str:
    return f"""
  <g filter="url(#shadow)" transform="translate(236 86)">
    <path d="M156 71 C166 32 203 12 242 12 C282 12 317 32 328 71" fill="none" stroke="{product['highlight']}" stroke-width="28" stroke-linecap="round"/>
    <path d="M111 80 L374 80 C424 80 460 121 455 174 L430 451 C427 486 397 513 361 513 L125 513 C90 513 60 486 56 451 L31 174 C26 121 61 80 111 80 Z" fill="{product['base']}"/>
    <path d="M86 254 C167 294 312 294 399 254 L383 429 C381 451 363 468 340 468 L145 468 C122 468 104 451 102 429 Z" fill="{product['highlight']}" opacity="0.52"/>
    <path d="M102 149 L382 149 M118 210 L366 210" stroke="{product['accent']}" stroke-width="13" stroke-linecap="round"/>
    <path d="M60 199 L7 263 M426 199 L478 263" stroke="#111418" stroke-width="22" stroke-linecap="round" opacity="0.56"/>
    <circle cx="243" cy="339" r="38" fill="{product['accent']}"/>
  </g>
"""


def cap(product: dict[str, str]) -> str:
    return f"""
  <g filter="url(#shadow)" transform="translate(128 172)">
    <path d="M118 230 C154 116 269 54 408 64 C536 73 622 149 653 254 C526 213 302 205 118 230 Z" fill="{product['base']}"/>
    <path d="M302 69 C276 135 267 188 274 224" fill="none" stroke="{product['accent']}" stroke-width="13" stroke-linecap="round"/>
    <path d="M409 64 C417 126 416 181 405 224" fill="none" stroke="{product['accent']}" stroke-width="13" stroke-linecap="round"/>
    <path d="M116 230 C248 213 458 213 653 254 C682 260 698 290 685 314 C664 353 550 348 414 318 C285 290 176 286 81 310 C49 318 29 291 42 265 C51 248 76 236 116 230 Z" fill="{product['accent']}"/>
    <path d="M172 220 C300 200 475 207 607 239" fill="none" stroke="{product['highlight']}" stroke-width="9" stroke-linecap="round" opacity="0.72"/>
  </g>
"""


RENDERERS = {
    "shoe": shoe,
    "slide": slide,
    "tee": tee,
    "short": short,
    "pack": pack,
    "cap": cap,
}


def render(product: dict[str, str]) -> str:
    body = RENDERERS[product["kind"]](product)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="640" viewBox="0 0 900 640" role="img" aria-label="{escape(product['name'])}">
{background(product)}
{body}
{label(product)}
</svg>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    converter = shutil.which("rsvg-convert")
    if not converter:
        raise SystemExit("rsvg-convert is required to create PNG assets")

    for product in PRODUCTS:
        svg_path = OUT_DIR / f"{product['id']}.svg"
        png_path = OUT_DIR / f"{product['id']}.png"
        svg_path.write_text(render(product), encoding="utf-8")
        subprocess.run(
            [converter, str(svg_path), "--width", "900", "--height", "640", "--format", "png", "--output", str(png_path)],
            check=True,
        )
        print(f"wrote {png_path.relative_to(APP_DIR)}")


if __name__ == "__main__":
    main()
