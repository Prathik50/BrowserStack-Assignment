"""
Translation Module - Translates Spanish article titles to English
Uses Google Translate API with fallback to free API
"""

import logging
import os
from typing import List, Dict
from collections import Counter
import re

logger = logging.getLogger(__name__)


class ArticleTranslator:
    """Translates article titles using various translation services"""
    
    def __init__(self, api_key: str = None, use_free_api: bool = True):
        """Initialize translator
        
        Args:
            api_key: Google Cloud Translation API key
            use_free_api: Use free translation API if Google API fails
        """
        self.api_key = api_key or os.getenv('GOOGLE_TRANSLATE_API_KEY')
        self.use_free_api = use_free_api
        self.translated_titles = []
    
    def translate_titles(self, titles: List[str]) -> List[Dict]:
        """Translate article titles from Spanish to English
        
        Args:
            titles: List of Spanish titles
            
        Returns:
            List of dictionaries with original and translated titles
        """
        results = []
        
        for title in titles:
            try:
                translated = self._translate_text(title)
                results.append({
                    'original': title,
                    'translated': translated
                })
                logger.info(f"Translated: {title} -> {translated}")
                
            except Exception as e:
                logger.error(f"Failed to translate '{title}': {e}")
                results.append({
                    'original': title,
                    'translated': title  # Fallback to original
                })
        
        self.translated_titles = results
        return results
    
    def _translate_text(self, text: str) -> str:
        """Translate text using available API
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        # Try Google Translate API first
        if self.api_key:
            try:
                return self._translate_with_google(text)
            except Exception as e:
                logger.warning(f"Google API failed: {e}. Trying fallback...")
        
        # Fallback to free translation API
        if self.use_free_api:
            return self._translate_with_free_api(text)
        
        return text
    
    def _translate_with_google(self, text: str) -> str:
        """Translate using Google Cloud Translation API"""
        try:
            from google.cloud import translate_v2
            
            client = translate_v2.Client(credentials=self.api_key)
            result = client.translate_text(text, target_language='en', source_language='es')
            return result['translatedText']
            
        except ImportError:
            logger.warning("google-cloud-translate not installed, using free API")
            return self._translate_with_free_api(text)
    
    def _translate_with_free_api(self, text: str) -> str:
        """Translate using free MyMemory API (no authentication needed)"""
        import requests
        
        try:
            url = "https://api.mymemory.translated.net/get"
            params = {
                'q': text,
                'langpair': 'es|en'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data['responseStatus'] == 200:
                translated = data['responseData']['translatedText']
                return translated
            else:
                raise Exception(f"API error: {data.get('responseDetails', 'Unknown error')}")
                
        except Exception as e:
            logger.warning(f"MyMemory API failed: {e}")
            # Fallback to simple translation attempt
            return text
    
    def print_translated_titles(self):
        """Print translated titles in a formatted way"""
        print("\n" + "="*100)
        print("TRADUCCIÓN DE TÍTULOS AL INGLÉS")
        print("="*100 + "\n")
        
        for idx, result in enumerate(self.translated_titles, 1):
            print(f"Artículo {idx}:")
            print(f"  Original (ES): {result['original']}")
            print(f"  Traducido (EN): {result['translated']}")
            print()
    
    @staticmethod
    def analyze_repeated_words(translated_titles: List[Dict], min_occurrences: int = 3) -> Dict[str, int]:
        """Analyze translated headers to find repeated words
        
        Args:
            translated_titles: List of translation results
            min_occurrences: Minimum occurrences to include in results
            
        Returns:
            Dictionary of word: count for repeated words
        """
        # Collect all words from translated titles
        all_words = []
        
        for result in translated_titles:
            translated_text = result['translated'].lower()
            # Clean and split text
            words = re.findall(r'\b[a-z]+\b', translated_text)
            all_words.extend(words)
        
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'are', 'was', 'were', 'be', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can', 'may',
            'might', 'must', 'shall', 'by', 'from', 'as', 'that', 'this', 'which',
            'who', 'what', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
            'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'not'
        }
        
        # Remove stop words
        filtered_words = [w for w in all_words if w not in stop_words and len(w) > 2]
        
        # Count occurrences
        word_counts = Counter(filtered_words)
        
        # Filter by minimum occurrences
        repeated_words = {
            word: count for word, count in word_counts.items()
            if count >= min_occurrences
        }
        
        return dict(sorted(repeated_words.items(), key=lambda x: x[1], reverse=True))
    
    def print_word_analysis(self, min_occurrences: int = 3):
        """Print analysis of repeated words in translated titles
        
        Args:
            min_occurrences: Minimum occurrences to display
        """
        repeated_words = self.analyze_repeated_words(self.translated_titles, min_occurrences)
        
        print("\n" + "="*80)
        print(f"ANÁLISIS DE PALABRAS REPETIDAS (mínimo {min_occurrences} veces)")
        print("="*80 + "\n")
        
        if repeated_words:
            for word, count in repeated_words.items():
                print(f"  '{word}': {count} veces")
        else:
            print(f"No hay palabras repetidas más de {min_occurrences} veces en los títulos traducidos.")
        
        print()


if __name__ == "__main__":
    # Example usage
    sample_titles = [
        "El futuro de la política española",
        "Cómo cambia la economía mundial",
        "La importancia de la educación",
        "Los retos de la tecnología",
        "España en la encrucijada política"
    ]
    
    translator = ArticleTranslator(use_free_api=True)
    results = translator.translate_titles(sample_titles)
    translator.print_translated_titles()
    translator.print_word_analysis(min_occurrences=2)
