import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Proje kök dizinini yola ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_system import RAGSystem

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

if __name__ == '__main__':
    unittest.main()
