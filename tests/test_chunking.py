import unittest
from types import SimpleNamespace
from marketbrief.indexing import articles_to_chunks

class ChunkingTests(unittest.TestCase):
    def test_metadata_survives_chunking(self):
        a=SimpleNamespace(url="https://example.com/a",title="Example",text="Market news content. "*200)
        chunks=articles_to_chunks([a],chunk_size=200,chunk_overlap=20)
        self.assertGreater(len(chunks),1)
        self.assertTrue(all(c.metadata["source"]==a.url for c in chunks))
        self.assertTrue(all(c.metadata["title"]==a.title for c in chunks))
if __name__=="__main__": unittest.main()
