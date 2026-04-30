import logging
import requests
from PIL import Image
from io import BytesIO
from main import validate_url, extract_text_from_url, analyze_source_credibility, extract_metadata_from_url

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_url_analysis():
    # Test cases
    test_cases = {
        'valid_news': [
            'https://www.reuters.com/world/middle-east/israel-hamas-war-latest-2023-11-03/',
            'https://www.bbc.com/news/world-middle-east-67169358'
        ],
        'invalid_urls': [
            'https://nonexistent.news.com/article',
            'invalid-url',
            'ftp://invalid.com'
        ],
        'image_urls': [
            'https://www.reuters.com/resizer/12345/reuterslogo.png',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/800px-Google_2015_logo.svg.png'
        ]
    }

    # Test 1: Valid News URLs
    logger.info("\n=== Testing Valid News URLs ===")
    for url in test_cases['valid_news']:
        logger.info(f"\nTesting URL: {url}")
        
        # Test URL validation
        is_valid, message = validate_url(url)
        logger.info(f"URL Validation: {is_valid} - {message}")
        
        if is_valid:
            # Test text extraction
            text = extract_text_from_url(url)
            logger.info(f"Text Extraction Length: {len(text) if not isinstance(text, str) or not text.startswith('Error') else 0}")
            logger.info(f"Text Preview: {text[:200]}...")
            
            # Test metadata extraction
            metadata = extract_metadata_from_url(url)
            logger.info("\nMetadata Extraction:")
            for key, value in metadata.items():
                logger.info(f"{key}: {value}")
            
            # Test credibility analysis
            credibility = analyze_source_credibility(metadata)
            logger.info("\nCredibility Analysis:")
            logger.info(f"Score: {credibility['credibility_score']}")
            logger.info(f"Level: {credibility['credibility_level']}")
            if credibility['warnings']:
                logger.info("Warnings:")
                for warning in credibility['warnings']:
                    logger.info(f"- {warning}")
            if credibility['insights']:
                logger.info("Insights:")
                for insight in credibility['insights']:
                    logger.info(f"- {insight}")

    # Test 2: Invalid URLs
    logger.info("\n=== Testing Invalid URLs ===")
    for url in test_cases['invalid_urls']:
        logger.info(f"\nTesting Invalid URL: {url}")
        is_valid, message = validate_url(url)
        logger.info(f"URL Validation: {is_valid} - {message}")

    # Test 3: Image URLs
    logger.info("\n=== Testing Image URLs ===")
    for url in test_cases['image_urls']:
        logger.info(f"\nTesting Image URL: {url}")
        
        # Test URL validation
        is_valid, message = validate_url(url)
        logger.info(f"URL Validation: {is_valid} - {message}")
        
        if is_valid:
            # Test OCR text extraction
            text = extract_text_from_url(url)
            logger.info(f"OCR Text Extraction: {text}")

    logger.info("\n=== Testing Retry Mechanism ===")
    test_url = "https://httpstat.us/503"
    logger.info(f"Testing URL with 503 status: {test_url}")
    is_valid, message = validate_url(test_url)
    logger.info(f"Retry Result: {message}")

if __name__ == "__main__":
    test_url_analysis()
