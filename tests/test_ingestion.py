import unittest
from marketbrief.ingestion import validate_url,extract_article

class IngestionTests(unittest.TestCase):
    def test_url_validation(self):
        self.assertTrue(validate_url("https://example.com/a"))
        self.assertFalse(validate_url("javascript:alert(1)"))
        self.assertFalse(validate_url("not a url"))
    def test_html_extraction(self):
        html="""<html><head><title>Market Update</title></head><body><nav>Navigation content that should disappear.</nav><article><h1>Heading</h1><p>The company reported quarterly revenue growth of twelve percent this period.</p><p>Analysts said operating margins improved compared with the prior quarter.</p></article></body></html>"""
        a=extract_article(html,"https://example.com")
        self.assertEqual(a.title,"Market Update")
        self.assertIn("quarterly revenue growth",a.text)
        self.assertNotIn("Navigation content",a.text)
if __name__=="__main__": unittest.main()
