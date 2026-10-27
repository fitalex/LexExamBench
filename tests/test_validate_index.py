"""Original synthetic metadata; never actual exam bodies or answer keys."""
import copy
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_index import validate_document, validate_public_tree, validate_sources, main

def synthetic_record():
    return dict(id='synthetic-2017-001', exam_system='national-judicial-exam', year=2017,
        paper='synthetic-paper', question_number='synthetic-1', question_type='single-choice',
        subject='synthetic-placeholder', source_id='synthetic-source', source_url='https://example.org/synthetic',
        answer_source_url=None, provenance_grade='synthetic', accessed_at='2026-10-27',
        business_category_mapping=['no-direct-mapping'],
        rights={k:dict(status='pending', evidence_url=None, basis='Original synthetic fixture; no grant asserted') for k in
            ('question_copy','answer_copy','storage','redistribution','external_model')},
        law_time_status='historical-review-pending', law_time_context='Synthetic historical date placeholder; not legal advice',
        current_law_review='pending', expert_review='pending', split='unassigned', public_holdout_candidate='unassigned',
        revision=1, provenance=dict(method='original-synthetic-fixture', locator='synthetic-1', revision='fixture-v1'))

def doc(q=None): return {'schema_version':'0.2.0','questions':[synthetic_record() if q is None else q]}

def source_fixture():
    q=synthetic_record()
    source=dict(id='synthetic-source',url=q['source_url'],publisher='Original synthetic fixture',
        exam_system=q['exam_system'],year=2017,question_type='synthetic',answer_source_url=None,
        provenance_grade='synthetic',accessed_at=q['accessed_at'],verification='unverified',
        access_result='No network request',revision='fixture-v1',rights=q['rights'],
        indexing=dict(status='pending',evidence_url=None,basis='Synthetic fixture only'))
    return dict(schema_version='0.2.0',sources=[source])

class IndexValidationTests(unittest.TestCase):
    def reject(self, field, value):
        q=synthetic_record(); q[field]=value
        self.assertTrue(validate_document(doc(q)))
    def test_synthetic_valid(self): self.assertEqual([],validate_document(doc()))
    def test_empty_rejected(self): self.assertTrue(validate_document({'schema_version':'0.2.0','questions':[]}))
    def test_explicit_empty_diagnostic(self): self.assertEqual([],validate_document({'schema_version':'0.2.0','questions':[]},allow_empty=True))
    def test_missing_source(self):
        q=synthetic_record(); del q['source_url']; self.assertTrue(validate_document(doc(q)))
    def test_missing_registry_source(self):
        q=synthetic_record(); q.update(provenance_grade='official',source_url='https://www.moj.gov.cn/example'); self.assertTrue(validate_document(doc(q),[]))
    def test_duplicate_id(self):
        d=doc(); d['questions'].append(copy.deepcopy(d['questions'][0])); self.assertTrue(validate_document(d))
    def test_duplicate_year_paper_number(self):
        d=doc(); q=copy.deepcopy(d['questions'][0]);q['id']='another-id';d['questions'].append(q);self.assertTrue(validate_document(d))
    def test_official_recalled_mislabeled(self): self.reject('provenance_grade','official')
    def test_official_url_recalled_label(self):
        q=synthetic_record();q.update(source_url='https://www.moj.gov.cn/example',provenance_grade='recalled');self.assertTrue(validate_document(doc(q)))
    def test_rights_forged_status(self):
        q=synthetic_record();q['rights']['storage']['status']='authorized';self.assertTrue(validate_document(doc(q)))
    def test_rights_url_is_not_a_grant(self):
        q=synthetic_record();q['rights']['external_model'].update(status='verified',evidence_url='https://example.org/license');self.assertTrue(validate_document(doc(q)))
    def test_model_rights_missing_evidence(self):
        q=synthetic_record();q['rights']['external_model']['status']='verified';self.assertTrue(validate_document(doc(q)))
    def test_missing_law_time(self):
        q=synthetic_record();del q['law_time_context'];self.assertTrue(validate_document(doc(q)))
    def test_body_rejected(self): self.reject('question_text','ORIGINAL SYNTHETIC INVALID FIELD')
    def test_nested_body_rejected(self):
        q=synthetic_record();q['provenance']['answer_text']='ORIGINAL SYNTHETIC INVALID FIELD';self.assertTrue(validate_document(doc(q)))
    def test_holdout_split(self): self.reject('split','holdout')
    def test_holdout_candidate(self): self.reject('public_holdout_candidate','holdout')
    def test_expert_signature_forged(self): self.reject('expert_review','approved')
    def test_current_law_forged(self): self.reject('current_law_review','approved')
    def test_exam_year_mismatch(self): self.reject('year',2026)
    def test_invalid_date(self): self.reject('accessed_at','2026-02-30')
    def test_unknown_category(self): self.reject('business_category_mapping',['invented-legal-category'])
    def test_illegal_json_cli_redacted(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'invalid.json';p.write_text('{ORIGINAL_SYNTHETIC_SECRET_MARKER')
            out=io.StringIO()
            with contextlib.redirect_stderr(out): self.assertEqual(1,main([str(p)]))
            self.assertNotIn('ORIGINAL_SYNTHETIC_SECRET_MARKER',out.getvalue())
    def test_empty_sources_rejected(self):
        self.assertTrue(validate_sources({'schema_version':'0.2.0','sources':[]}))
    def test_source_body_rejected(self):
        registry=source_fixture()
        registry['sources'][0]['question_text']='ORIGINAL SYNTHETIC INVALID FIELD'
        self.assertTrue(validate_sources(registry))
    def test_source_rights_forgery(self):
        registry=source_fixture()
        registry['sources'][0]['rights']['external_model']['status']='verified'
        self.assertTrue(validate_sources(registry))
    def test_source_synthetic_fixture_valid(self):
        self.assertEqual([],validate_sources(source_fixture()))
    def test_malformed_url_does_not_crash(self):
        self.reject('source_url','https://[invalid')
    def test_synthetic_not_counted_in_production(self):
        self.assertTrue(validate_document(doc(),[]))
    def test_public_holdout_path(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'holdout').mkdir();self.assertTrue(validate_public_tree(root))
    def test_public_pdf(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'exam.pdf').touch();self.assertTrue(validate_public_tree(root))
    def test_unregistered_public_data(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'data').mkdir();(root/'data/snapshot.json').write_text('{}');self.assertTrue(validate_public_tree(root))

if __name__=='__main__': unittest.main()
