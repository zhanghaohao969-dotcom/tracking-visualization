#!/usr/bin/env python3
"""Shared, non-executing CONFIG parser and bounded local-image handling."""
import base64
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

CONFIG_RE = re.compile(r'(<script\b[^>]*\bid=["\']annotation-config["\'][^>]*>)([\s\S]*?)(</script\s*>)', re.I)
IMAGE_MIMES = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp'}
MAX_IMAGE_BYTES = 12 * 1024 * 1024
MAX_HTML_BYTES = 50 * 1024 * 1024


def load_html(path):
    p = Path(path).resolve()
    if p.stat().st_size > MAX_HTML_BYTES:
        raise ValueError('HTML exceeds the 50 MiB validation limit')
    return p, p.read_text(encoding='utf-8')


def parse_config(html):
    matches = list(CONFIG_RE.finditer(html))
    if len(matches) != 1:
        raise ValueError('Expected exactly one script#annotation-config JSON block')
    match = matches[0]
    if not re.search(r'\btype=["\']application/json["\']', match.group(1), re.I):
        raise ValueError('annotation-config must use type="application/json"')
    config = json.loads(match.group(2))
    if not isinstance(config, dict):
        raise ValueError('CONFIG must be a JSON object')
    return config, match


def replace_config(html, config):
    _, match = parse_config(html)
    # Escape < so JSON text cannot terminate its script element.
    text = json.dumps(config, ensure_ascii=False, indent=2).replace('<', '\\u003c')
    return html[:match.start(2)] + '\n' + text + '\n' + html[match.end(2):]


def resolve_image(ref, base):
    if not isinstance(ref, str) or not ref.strip():
        raise ValueError('Image reference must be a non-empty string')
    if ref.startswith('data:'):
        if not re.match(r'^data:image/(png|jpeg|gif|webp);base64,[A-Za-z0-9+/=\s]+$', ref):
            raise ValueError('Only base64 PNG/JPEG/GIF/WebP data images are supported')
        raw = base64.b64decode(ref.split(',', 1)[1], validate=True)
        if len(raw) > MAX_IMAGE_BYTES:
            raise ValueError('Embedded image exceeds 12 MiB')
        return None
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError('Use local relative images or data images; remote URLs are not fetched')
    relative = Path(unquote(ref))
    if relative.is_absolute() or '\\' in ref:
        raise ValueError('Absolute image paths are not allowed')
    root = Path(base).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Image path escapes the HTML directory')
    if path.suffix.lower() not in IMAGE_MIMES:
        raise ValueError('Unsupported image extension')
    if not path.is_file():
        raise ValueError('Missing image: ' + ref)
    if path.stat().st_size > MAX_IMAGE_BYTES:
        raise ValueError('Image exceeds 12 MiB: ' + ref)
    return path


def image_refs(html, config):
    refs = []
    for match in re.finditer(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', html, re.I):
        ref = match.group(1)
        if '${' not in ref:
            refs.append(ref)
    for match in re.finditer(r'url\(\s*["\']?([^"\')\s]+)', html, re.I):
        ref = match.group(1)
        if not ref.startswith(('data:image/svg+xml', '#')):
            refs.append(ref)
    refs.extend(page.get('img') for page in config.get('pages', []) if isinstance(page, dict))
    return list(dict.fromkeys(refs))
