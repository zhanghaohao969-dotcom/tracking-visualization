"""Regression tests using only fictional template data and temporary directories."""
import copy
import importlib.util
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/tracking-visualization'
sys.path.insert(0, str(SKILL / 'scripts'))
from annotation_common import parse_config, replace_config
from validate_annotation import validate
from embed_images import embed


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        for name in ('placeholder.png', 'texture.jpg'):
            shutil.copyfile(SKILL / 'assets' / name, self.base / name)
        self.original = (SKILL / 'assets/template-single.html').read_text()
        self.config, _ = parse_config(self.original)

    def write(self, config=None, text=None):
        path = self.base / 'report.html'
        path.write_text(text if text is not None else replace_config(self.original, config or self.config))
        return path

    def test_both_templates(self):
        for name in ('template-single.html', 'template-multi.html'):
            errors, _ = validate(SKILL / 'assets' / name)
            self.assertEqual(errors, [], name)

    def test_invalid_position(self):
        c = copy.deepcopy(self.config)
        c['pins'][0]['pos']['x'] = 101
        self.assertTrue(validate(self.write(c))[0])

    def test_mapping_mismatch(self):
        c = copy.deepcopy(self.config)
        c['table'][0]['action'] = 'different_event'
        self.assertTrue(validate(self.write(c))[0])

    def test_duplicate_mapping(self):
        c = copy.deepcopy(self.config)
        c['table'][1]['pinLoc'] = 'S1-1'
        self.assertTrue(validate(self.write(c))[0])

    def test_missing_suggest(self):
        c = copy.deepcopy(self.config)
        c['pins'][1]['suggest'] = False
        self.assertTrue(validate(self.write(c))[0])

    def test_priority_in_action(self):
        c = copy.deepcopy(self.config)
        c['pins'][1]['action'] = 'missing P0'
        c['table'][1]['action'] = 'missing P0'
        self.assertTrue(validate(self.write(c))[0])

    def test_unknown_not_zero(self):
        c = copy.deepcopy(self.config)
        c['pins'][0]['unverified'] = True
        c['table'][0]['status'] = 'unverified'
        c['table'][0].pop('count')
        c['table'][0].pop('users')
        self.assertEqual(validate(self.write(c))[0], [])
        c['table'][0]['count'] = 0
        self.assertTrue(validate(self.write(c))[0])

    def test_missing_image(self):
        text = self.original.replace('src="placeholder.png"', 'src="missing.png"')
        self.assertTrue(validate(self.write(text=text))[0])

    def test_embed_preserves_image_bytes(self):
        import base64
        path = self.write()
        output = embed(path)
        text = output.read_text()
        match = re.search(r'src="data:image/png;base64,([^"]+)"', text)
        self.assertIsNotNone(match)
        self.assertEqual(base64.b64decode(match.group(1)), (self.base / 'placeholder.png').read_bytes())
        self.assertEqual(validate(output)[0], [])
        self.assertTrue(path.exists())

    def test_refuse_overwrite(self):
        path = self.write()
        output = embed(path)
        with self.assertRaises(ValueError):
            embed(path, output)

    def test_refuse_path_escape(self):
        path = self.write(text=self.original.replace('src="placeholder.png"', 'src="../private.png"'))
        with self.assertRaises(ValueError):
            embed(path)

    def test_refuse_remote_image(self):
        path = self.write(text=self.original.replace('src="placeholder.png"', 'src="https://example.com/image.png"'))
        with self.assertRaises(ValueError):
            embed(path)

    def test_no_page_execution(self):
        sentinel = self.base / 'should-not-exist.txt'
        payload = '<script>require("fs").writeFileSync(' + json.dumps(str(sentinel)) + ',"unsafe")</script>'
        path = self.write(text=self.original.replace('</body>', payload + '</body>'))
        self.assertEqual(validate(path)[0], [])
        self.assertFalse(sentinel.exists())

    def test_text_safe_renderer(self):
        for name in ('template-single.html', 'template-multi.html'):
            text = (SKILL / 'assets' / name).read_text()
            self.assertNotIn('innerHTML', text)
            self.assertNotIn('insertAdjacentHTML', text)
            self.assertNotIn('eval(', text)
            self.assertIn('textContent', text)

    def test_default_priority_hidden_and_bilingual(self):
        self.assertIs(self.config['showPriority'], False)
        self.assertIn("'zh-CN'", self.original)
        self.assertIn("en:", self.original)


if __name__ == '__main__':
    unittest.main()
