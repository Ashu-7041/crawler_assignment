# E-commerce Product Crawler

This service crawls e-commerce websites to extract all product page URLs using multi-threaded operations and Selenium WebDriver.

## Features

- Multi-threaded web crawling for efficient data collection
- Detection of product URLs based on common URL patterns
- MongoDB storage of crawled data
- Celery-based task distribution for scalability
- Configurable for multiple e-commerce websites

## Setup

### Prerequisites

- Python 3.10+
- MongoDB
- Redis (for Celery message broker)
- Chrome browser (for Selenium WebDriver)

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/crawler_assignment.git
cd crawler_assignment
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set up environment variables in a `.env` file:
```
MONGODB_USER=your_mongodb_user
MONGODB_PASSWORD=your_mongodb_password
MONGODB_HOST=your_mongodb_host
MONGODB_PORT=your_mongodb_port
MONGODB_AUTH_DB=your_auth_db
```

## Usage

### Starting the Celery Worker

Start the Celery worker to process crawling tasks:

```
celery -A celery_config worker -l info -Q crawler_service
```

### Triggering the Crawler

Run the crawler with the included sample websites or modify `run.py` to include your target e-commerce sites:

```
python run.py
```

The default configuration includes:
- https://www.virgio.com/
- https://www.westside.com/

## Customization

### Adding More Websites

Edit `run.py` to include additional e-commerce websites:

```python
ecommerce_sites = [
    "https://www.virgio.com/",
    "https://www.westside.com/",
    "https://your-additional-site.com/"
]
```

### Additional URL Patterns

To recognize different product URL patterns, modify the `PRODUCT_PATTERNS` list in `services/crawler_service/crawler.py`.

## Code Formatting

This project uses Black and isort for code formatting:

```
make format  # Format code with Black
make sort    # Sort imports with isort
make lint    # Run flake8 for linting
```

## Docker Support

A Dockerfile is included to containerize the application:

```
docker build -t ecommerce-crawler .
docker run ecommerce-crawler
```

## License

[MIT License](LICENSE)
