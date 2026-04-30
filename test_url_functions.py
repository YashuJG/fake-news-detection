from main import validate_url, extract_text_from_url, analyze_source_credibility, extract_metadata_from_url
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_url_functions():
    # Test URLs
    test_urls = [
        'https://www.reuters.com/world/us/biden-hosts-south-koreas-yoon-japan-pm-kishida-historic-camp-david-summit-2023-08-18/',
        'https://breakingnews123.xyz/fake-article',
        'https://www.bbc.com/news',
        'https://invalid.url.com/article',
        'https://medium.com/@user/article'
    ]

    for url in test_urls:
        logger.info(f"\n{'='*50}\nTesting URL: {url}\n{'='*50}")

        # Test 1: validate_url()
        logger.info("\n1. Testing URL validation:")
        is_valid, message = validate_url(url)
        logger.info(f"Valid: {is_valid}")
        logger.info(f"Message: {message}")

        if is_valid:
            # Test 2: extract_text_from_url()
            logger.info("\n2. Testing text extraction:")
            text = extract_text_from_url(url)
            logger.info(f"Extracted text length: {len(text) if not text.startswith('Error') else 0}")
            logger.info(f"Text preview: {text[:200]}...")

            # Test 3: extract_metadata_from_url()
            logger.info("\n3. Testing metadata extraction:")
            metadata = extract_metadata_from_url(url)
            if 'error' not in metadata:
                logger.info("Metadata extracted successfully:")
                for key, value in metadata.items():
                    logger.info(f"{key}: {value}")
            else:
                logger.error(f"Metadata extraction failed: {metadata['error']}")

            # Test 4: analyze_source_credibility()
            logger.info("\n4. Testing source credibility analysis:")
            credibility = analyze_source_credibility(metadata)
            logger.info(f"Credibility score: {credibility['credibility_score']}")
            logger.info(f"Credibility level: {credibility['credibility_level']}")
            if credibility['warnings']:
                logger.info("Warnings:")
                for warning in credibility['warnings']:
                    logger.info(f"- {warning}")
            if credibility['insights']:
                logger.info("Insights:")
                for insight in credibility['insights']:
                    logger.info(f"- {insight}")

        logger.info("\n")

if __name__ == "__main__":
    test_url_functions()
