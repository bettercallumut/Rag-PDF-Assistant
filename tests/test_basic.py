import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Proje kök dizinini yola ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_system import RAGSystem
from updater import UpdateChecker

class TestRAGSystem(unittest.TestCase):
    def setUp(self):
        # Mock embeddings to avoid loading heavy models during tests
        with patch('rag_system.HuggingFaceEmbeddings') as mock_embeddings:
            self.rag_system = RAGSystem()
            self.rag_system.embeddings = MagicMock()

    def test_initialization(self):
        self.assertIsNotNone(self.rag_system)
        self.assertIsNone(self.rag_system.vectorstore)

    @patch('rag_system.PyPDF2.PdfReader')
    def test_process_pdf_error(self, mock_reader):
        # Test file not found error handling
        with self.assertRaises(Exception):
            self.rag_system.process_pdf("non_existent_file.pdf")

class TestUpdater(unittest.TestCase):
    def test_version_compare_newer(self):
        checker = UpdateChecker("test/repo")
        self.assertTrue(checker.is_newer("1.1.0", "1.0.0"))
        self.assertTrue(checker.is_newer("2.0.0", "1.9.9"))
        self.assertTrue(checker.is_newer("1.0.1", "1.0.0"))

    def test_version_compare_older(self):
        checker = UpdateChecker("test/repo")
        self.assertFalse(checker.is_newer("0.9.9", "1.0.0"))
        self.assertFalse(checker.is_newer("1.0.0", "1.0.0"))
        self.assertFalse(checker.is_newer("1.0.0", "1.1.0"))

if __name__ == '__main__':
    unittest.main()
