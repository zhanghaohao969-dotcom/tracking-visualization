#!/usr/bin/env python3
"""Validate annotation JSON, local assets and JS syntax without executing page code."""
import argparse
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from annotation_common import load_html, parse_config, resolve_image, image_refs

COLORS = {'blue', 'green', 'red'}
STATUS = {'ok', 'empty', 'unverified', 'p0', 'p1', 'p2'}


def validate(html_path):
    path, html = load_html(html_path)
    c, _ = parse_config(html)
    errors = []
    warnings = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    def text(v):
        return isinstance(v, str) and bool(v.strip())
    def integer(v):
        return type(v) is int and v > 0
    for key in ('title', 'meta'):
        require(text(c.get(key)), key + ' must be non-empty text')
    require(c.get('lang', 'en') in ('en', 'zh-CN'), 'lang must be en or zh-CN')
    require(type(c.get('showPriority', False)) is bool, 'showPriority must be boolean')
    legends = c.get('legend', [])
    require(isinstance(legends, list) and bool(legends), 'legend must be a non-empty array')
    legend_colors = []
    for item in legends if isinstance(legends, list) else []:
        require(isinstance(item, dict), 'legend entry must be an object')
        if not isinstance(item, dict):
            continue
        require(item.get('color') in COLORS, 'Invalid legend color')
        require(text(item.get('label')), 'legend label is required')
        legend_colors.append(item.get('color'))
    require(len(legend_colors) == len(set(legend_colors)), 'Duplicate legend colors')
    rows = c.get('table', [])
    require(isinstance(rows, list) and bool(rows), 'table must be a non-empty array')
    mapping = {}
    row_ids = set()
    for row in rows if isinstance(rows, list) else []:
        require(isinstance(row, dict), 'table entry must be an object')
        if not isinstance(row, dict):
            continue
        rid = row.get('id')
        require(integer(rid) and rid not in row_ids, 'table ids must be unique positive integers')
        row_ids.add(rid if isinstance(rid, (int, str)) else str(rid))
        for key in ('action', 'loc', 'params'):
            require(text(row.get(key)), f'table {rid}: {key} is required')
        require(row.get('status') in STATUS, f'table {rid}: invalid status')
        require(row.get('color') in COLORS, f'table {rid}: explicit color is required')
        gap = row.get('status') in {'p0', 'p1', 'p2'}
        require((row.get('color') == 'red') == gap, f'table {rid}: red is reserved for gaps')
        if gap:
            require(row.get('count') is None and row.get('users') is None, f'table {rid}: gaps have no observed counts')
            for key in ('timing', 'desc', 'suggestion'):
                require(text(row.get(key)), f'table {rid}: gap requires {key}')
        if row.get('status') == 'empty':
            require(row.get('count') == 0 and row.get('users') == 0, f'table {rid}: empty requires verified zero counts')
        if row.get('status') == 'unverified':
            require(row.get('count') is None and row.get('users') is None, f'table {rid}: unknown counts must remain absent')
        for key in ('count', 'users'):
            value = row.get(key)
            require(value is None or (type(value) is int and value >= 0), f'table {rid}: {key} must be a non-negative integer')
        require(not re.search(r'\bP[012]\b', str(row.get('action', '')), re.I), f'table {rid}: action must not include priority labels')
        for loc in str(row.get('pinLoc', '')).split(' / '):
            if not loc:
                continue
            require(bool(re.fullmatch(r'S[1-9]\d*-[1-9]\d*', loc)), f'table {rid}: invalid pinLoc {loc}')
            require(loc not in mapping, 'pinLoc maps to multiple rows: ' + loc)
            mapping[loc] = row
    require(('pins' in c) != ('pages' in c), 'Choose either pins or pages')
    pages = c.get('pages', [{'pins': c.get('pins', [])}])
    require(isinstance(pages, list) and bool(pages), 'pages must be a non-empty array')
    found = set()
    for index, page in enumerate(pages if isinstance(pages, list) else [], 1):
        require(isinstance(page, dict), f'page {index} must be an object')
        if not isinstance(page, dict):
            continue
        if 'pages' in c:
            require(text(page.get('name')) and text(page.get('img')), f'page {index}: name and img required')
            badge = page.get('badge', {})
            require(isinstance(badge, dict) and text(badge.get('text')) and bool(re.fullmatch(r'#[0-9a-fA-F]{6}', str(badge.get('bg', '')))), f'page {index}: invalid badge')
        pins = page.get('pins', [])
        require(isinstance(pins, list) and bool(pins), f'page {index}: pins must be non-empty')
        ids = set()
        for pin in pins if isinstance(pins, list) else []:
            require(isinstance(pin, dict), f'page {index}: pin must be an object')
            if not isinstance(pin, dict):
                continue
            pid = pin.get('id')
            require(integer(pid) and pid not in ids, f'page {index}: duplicate or invalid pin id')
            ids.add(pid if isinstance(pid, (str, int)) else str(pid))
            loc = f'S{index}-{pid}'
            found.add(loc)
            require(pin.get('color') in COLORS and pin.get('color') in legend_colors, loc + ': invalid or unlisted color')
            pos = pin.get('pos', {})
            for axis in ('x', 'y'):
                v = pos.get(axis) if isinstance(pos, dict) else None
                require(type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 100, loc + ': invalid position')
            for key in ('action', 'title', 'desc', 'params', 'data'):
                require(text(pin.get(key)), loc + ': ' + key + ' required')
            require(not re.search(r'\bP[012]\b', str(pin.get('action', '')), re.I), loc + ': priority label in action')
            require(loc in mapping, loc + ': not mapped by table.pinLoc')
            row = mapping.get(loc, {})
            require(row.get('action') == pin.get('action'), loc + ': pin/table action mismatch')
            require(row.get('color') == pin.get('color'), loc + ': pin/table color mismatch')
            for field in ('empty', 'unverified', 'suggest'):
                require(type(pin.get(field, False)) is bool, loc + ': ' + field + ' must be boolean')
            require((pin.get('empty') is True) == (row.get('status') == 'empty'), loc + ': zero-data flag mismatch')
            require((pin.get('unverified') is True) == (row.get('status') == 'unverified'), loc + ': unverified flag mismatch')
            require(pin.get('mark') in (None, 'error'), loc + ': invalid mark')
            if pin.get('color') == 'red':
                require(pin.get('suggest') is True, loc + ': gap requires suggest:true')
                require(row.get('status') in {'p0', 'p1', 'p2'}, loc + ': gap status mismatch')
                require(pin.get('tier', row.get('status')) == row.get('status'), loc + ': tier mismatch')
                require(pin.get('desc') == row.get('desc'), loc + ': gap descriptions must agree')
                normalize = lambda s: re.sub(r'[\s:：]+', '', str(s)).lower()
                a, b = normalize(pin.get('desc')), normalize(pin.get('data'))
                require(a != b and not (len(a) > 20 and a in b), loc + ': desc and data duplicate')
            else:
                require(not pin.get('suggest', False), loc + ': existing pin must not suggest a gap')
    require(set(mapping) <= found, 'table.pinLoc refers to a missing pin')
    for ref in image_refs(html, c):
        try:
            resolve_image(ref, path.parent)
        except (ValueError, OSError) as error:
            errors.append(str(error))
    node = shutil.which('node')
    if not node:
        errors.append('Node.js is required for complete JavaScript syntax checks')
    else:
        blocks = re.findall(r'<script\b([^>]*)>([\s\S]*?)</script\s*>', html, re.I)
        for attrs, script in blocks:
            if 'application/json' in attrs:
                continue
            with tempfile.TemporaryDirectory() as directory:
                js = Path(directory) / 'check.js'
                js.write_text(script, encoding='utf-8')
                result = subprocess.run([node, '--check', str(js)], capture_output=True, text=True, timeout=15)
                require(result.returncode == 0, 'JavaScript syntax: ' + result.stderr.strip())
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    args = parser.parse_args()
    try:
        errors, warnings = validate(args.html)
    except (ValueError, OSError, TypeError, subprocess.TimeoutExpired) as error:
        print('[FAIL]', error)
        return 2
    for warning in warnings:
        print('[WARN]', warning)
    for error in errors:
        print('[FAIL]', error)
    if not errors:
        print('[PASS] JSON semantics, local image paths and JavaScript syntax; page code was not executed')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
