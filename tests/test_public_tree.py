"""Filesystem regression fixtures are empty files, never examination material."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_index import validate_public_tree


class PublicTreeRegressionTests(unittest.TestCase):
    def check_rejected(self, relative_path, expected):
        for checkout in ('repo', 'work/repo', 'home/runner/work/LexExamBench/LexExamBench'):
            with self.subTest(checkout=checkout), tempfile.TemporaryDirectory() as td:
                root = Path(td) / checkout
                target = root / relative_path
                target.parent.mkdir(parents=True)
                target.touch()
                self.assertIn(expected, validate_public_tree(root))

    def test_holdout_under_actions_checkout(self):
        self.check_rejected('holdout/fixture.txt', 'forbidden private/holdout path')

    def test_pdf_under_actions_checkout(self):
        self.check_rejected('exam.pdf', 'unapproved content file')

    def test_unregistered_data_under_actions_checkout(self):
        self.check_rejected('data/fixture.json', 'unregistered public data file')

    def test_clean_roots_pass(self):
        for checkout in ('repo', 'work/repo', 'home/runner/work/LexExamBench/LexExamBench'):
            with self.subTest(checkout=checkout), tempfile.TemporaryDirectory() as td:
                root = Path(td) / checkout
                (root / 'docs').mkdir(parents=True)
                (root / 'docs/readme.md').touch()
                self.assertEqual([], validate_public_tree(root))

    def test_work_and_cache_do_not_hide_forbidden_files(self):
        for folder in ('work', '__pycache__'):
            with self.subTest(folder=folder):
                self.check_rejected(f'{folder}/private/fixture.txt', 'forbidden private/holdout path')
                self.check_rejected(f'{folder}/exam.pdf', 'unapproved content file')
                self.check_rejected(f'{folder}/data/fixture.json', 'unregistered public data file')

    def test_force_added_ignored_files_checked_even_if_removed_from_worktree(self):
        fixtures = {
            'work/holdout/fixture.txt': 'forbidden private/holdout path',
            'private/fixture.txt': 'forbidden private/holdout path',
            'work/exam.pdf': 'unapproved content file',
            'work/data/fixture.json': 'unregistered public data file',
        }
        for filename, expected in fixtures.items():
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as td:
                root = Path(td) / 'work/repo'
                root.mkdir(parents=True)
                def git(*args):
                    return subprocess.run(['git', '-C', str(root), *args], check=True,
                                          capture_output=True)
                git('init', '-q')
                (root / '.gitignore').write_text('work/\nprivate/\n')
                target = root / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.touch()
                git('add', '-f', '--', filename)
                self.assertIn(expected, validate_public_tree(root))
                target.unlink()  # Still staged: disk-only scanning is insufficient.
                self.assertIn(expected, validate_public_tree(root))

    def test_git_index_read_failure_rejects(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / '.git').mkdir()
            with patch('validate_index.subprocess.run', side_effect=OSError):
                self.assertIn('cannot inspect Git index paths', validate_public_tree(root))

    def test_git_metadata_is_excluded(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'work/repo'
            root.mkdir(parents=True)
            subprocess.run(['git', '-C', str(root), 'init', '-q'], check=True,
                           capture_output=True)
            (root / '.git/internal.pdf').touch()
            self.assertEqual([], validate_public_tree(root))


if __name__ == '__main__':
    unittest.main()
