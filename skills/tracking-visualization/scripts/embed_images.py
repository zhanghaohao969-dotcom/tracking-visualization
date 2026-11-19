#!/usr/bin/env python3
"""Embed local raster images without transcoding or executing JavaScript."""
import argparse
import base64
from pathlib import Path
from annotation_common import load_html, parse_config, replace_config, resolve_image, image_refs, IMAGE_MIMES


def embed(source, output=None):
    path, html = load_html(source)
    output = Path(output).resolve() if output else path.with_name(path.stem + '-standalone.html')
    if output.exists() or output == path:
        raise ValueError('Output exists; choose a new output filename')
    if not output.parent.is_dir():
        raise ValueError('Output directory does not exist')
    config, _ = parse_config(html)
    replacement = {}
    for ref in image_refs(html, config):
        local = resolve_image(ref, path.parent)
        if local is not None:
            raw = local.read_bytes()
            replacement[ref] = 'data:' + IMAGE_MIMES[local.suffix.lower()] + ';base64,' + base64.b64encode(raw).decode('ascii')
    for page in config.get('pages', []):
        page['img'] = replacement.get(page['img'], page['img'])
    html = replace_config(html, config)
    for ref, uri in replacement.items():
        html = html.replace('"' + ref + '"', '"' + uri + '"').replace("'" + ref + "'", "'" + uri + "'")
    final_config, _ = parse_config(html)
    for ref in image_refs(html, final_config):
        if resolve_image(ref, path.parent) is not None:
            raise ValueError('Unresolved local image: ' + ref)
    # Exclusive creation prevents accidental overwriting.
    with output.open('x', encoding='utf-8') as handle:
        handle.write(html)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    parser.add_argument('output', type=Path, nargs='?')
    args = parser.parse_args()
    try:
        output = embed(args.html, args.output)
    except (ValueError, OSError) as error:
        print('[FAIL]', error)
        return 1
    print('[PASS]', output, '- local images embedded; original bytes preserved')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
