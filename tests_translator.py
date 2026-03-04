"""
Unit Tests for El País Scraper
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from translator import ArticleTranslator


class TestArticleTranslator:
    """Test cases for ArticleTranslator"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.translator = ArticleTranslator(use_free_api=True)
        self.sample_titles = [
            "El futuro de la política española",
            "Cómo cambia la economía mundial",
            "La importancia de la educación",
            "Los retos de la tecnología",
            "España en la encrucijada política"
        ]
    
    def test_translator_initialization(self):
        """Test translator initialization"""
        assert self.translator is not None
        assert self.translator.use_free_api is True
    
    def test_analyze_repeated_words_basic(self):
        """Test word analysis functionality"""
        translated_titles = [
            {'original': 'Test 1', 'translated': 'The future of politics and government'},
            {'original': 'Test 2', 'translated': 'Politics and technology in modern government'},
            {'original': 'Test 3', 'translated': 'Government future with politics'},
        ]
        
        repeated = ArticleTranslator.analyze_repeated_words(
            translated_titles,
            min_occurrences=2
        )
        
        assert 'politics' in repeated or 'government' in repeated
    
    def test_analyze_repeated_words_min_occurrences(self):
        """Test minimum occurrence filter"""
        translated_titles = [
            {'original': 'Test 1', 'translated': 'apple banana apple'},
            {'original': 'Test 2', 'translated': 'apple cherry apple apple'},
        ]
        
        # Words with min 3 occurrences
        repeated = ArticleTranslator.analyze_repeated_words(
            translated_titles,
            min_occurrences=3
        )
        
        assert 'apple' in repeated
        assert repeated['apple'] >= 3
    
    def test_analyze_repeated_words_empty_input(self):
        """Test with empty input"""
        repeated = ArticleTranslator.analyze_repeated_words([], min_occurrences=2)
        assert repeated == {}
    
    def test_analyze_repeated_words_no_repeats(self):
        """Test when no words repeat"""
        translated_titles = [
            {'original': 'Test 1', 'translated': 'unique words only here'},
            {'original': 'Test 2', 'translated': 'different content completely'},
        ]
        
        repeated = ArticleTranslator.analyze_repeated_words(
            translated_titles,
            min_occurrences=2
        )
        
        # Should be mostly empty (except for common words filtered)
        assert len(repeated) < 5
    
    @patch('translator.ArticleTranslator._translate_with_free_api')
    def test_translate_with_fallback(self, mock_api):
        """Test translation with fallback"""
        mock_api.return_value = "Translated text"
        
        result = self.translator.translate_titles(["Test title"])
        
        assert len(result) == 1
        assert result[0]['original'] == "Test title"
        assert result[0]['translated'] is not None


class TestWordAnalysis:
    """Test word analysis functionality"""
    
    def test_stop_words_removal(self):
        """Test that common stop words are properly filtered"""
        translated_titles = [
            {'original': 'T1', 'translated': 'the quick brown fox'},
            {'original': 'T2', 'translated': 'the quick brown dog'},
        ]
        
        repeated = ArticleTranslator.analyze_repeated_words(
            translated_titles,
            min_occurrences=1
        )
        
        # 'the' and 'quick' should be filtered or not appear as common
        assert 'the' not in repeated
    
    def test_case_insensitivity(self):
        """Test that analysis is case-insensitive"""
        translated_titles = [
            {'original': 'T1', 'translated': 'Apple and apple pie'},
            {'original': 'T2', 'translated': 'APPLE sauce'},
        ]
        
        repeated = ArticleTranslator.analyze_repeated_words(
            translated_titles,
            min_occurrences=2
        )
        
        assert 'apple' in repeated
        assert repeated['apple'] >= 3
    
    def test_punctuation_handling(self):
        """Test that punctuation is properly handled"""
        translated_titles = [
            {'original': 'T1', 'translated': 'Hello, world! Hello world.'},
            {'original': 'T2', 'translated': 'Hello-world and hello'},
        ]
        
        repeated = ArticleTranslator.analyze_repeated_words(
            translated_titles,
            min_occurrences=2
        )
        
        assert 'hello' in repeated


class TestTranslationIntegration:
    """Integration tests for translation"""
    
    @pytest.mark.slow
    def test_free_api_translation(self):
        """Test free translation API (slow test)"""
        translator = ArticleTranslator(use_free_api=True)
        
        try:
            result = translator._translate_with_free_api("Hola mundo")
            assert result is not None
            assert len(result) > 0
        except Exception as e:
            pytest.skip(f"Free API unavailable: {e}")
    
    def test_translation_result_format(self):
        """Test that translation results have correct format"""
        translator = ArticleTranslator(use_free_api=True)
        
        with patch.object(translator, '_translate_with_free_api') as mock:
            mock.return_value = "Translated"
            
            results = translator.translate_titles(["Title 1", "Title 2"])
            
            assert len(results) == 2
            for result in results:
                assert 'original' in result
                assert 'translated' in result
                assert isinstance(result['original'], str)
                assert isinstance(result['translated'], str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
