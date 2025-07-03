import argparse
import logging
from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler
from concurrent.futures import ThreadPoolExecutor

def crawl_images(url_list, save_dir, engine='google', num_images=10, filters=None):
    if filters is None:
        filters = {}

    if engine.lower() == 'google':
        crawler = GoogleImageCrawler(storage={'root_dir': save_dir})
    elif engine.lower() == 'bing':
        crawler = BingImageCrawler(storage={'root_dir': save_dir})
    elif engine.lower() == 'baidu':
        crawler = BaiduImageCrawler(storage={'root_dir': save_dir})
    else:
        raise ValueError("Invalid engine specified. Choose 'google', 'bing', or 'baidu'.")

    for url in url_list:
        try:
            logging.info(f"Starting crawl for keyword: {url}")
            crawler.crawl(keyword=url, max_num=num_images, filters=filters)
            logging.info(f"Successfully finished crawling for: {url}")
        except Exception as e:
            logging.error(f"Error while crawling for keyword {url}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Image crawler using Google, Bing, or Baidu.")
    parser.add_argument(
        "-u", "--urls", 
        nargs="+", 
        required=True, 
        help="List of search terms or keywords for crawling images."
    )
    parser.add_argument(
        "-d", "--directory", 
        required=True, 
        help="Directory to save the downloaded images."
    )
    parser.add_argument(
        "-e", "--engine", 
        choices=["google", "bing", "baidu"], 
        default="google", 
        help="Search engine to use for crawling images."
    )
    parser.add_argument(
        "-n", "--num", 
        type=int, 
        default=10, 
        help="Number of images to download per search term."
    )
    parser.add_argument(
        "-f", "--filters", 
        type=str, 
        default=None, 
        help="Optional filters for Bing (JSON string: e.g., '{\"size\": \"large\", \"color\": \"blue\"}')."
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable verbose logging."
    )
    parser.add_argument(
        "-t", "--threads", 
        type=int, 
        default=1, 
        help="Number of threads for concurrent crawling."
    )

    args = parser.parse_args()

    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    # Parse filters if provided
    filters = eval(args.filters) if args.filters else {}

    if args.threads > 1:
        # Use a thread pool for concurrent crawling
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            executor.map(
                lambda keyword: crawl_images(
                    [keyword], args.directory, engine=args.engine, num_images=args.num, filters=filters
                ),
                args.urls
            )
    else:
        # Sequential crawling
        crawl_images(args.urls, args.directory, engine=args.engine, num_images=args.num, filters=filters)

if __name__ == "__main__":
    main()
