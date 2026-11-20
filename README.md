# IndiaMART Product Scraper & Analysis

A Python learning project that uses Scrapy to extract product listings and pandas, Matplotlib, and seaborn to explore the exported data.

## What is implemented

- Product name, price, company, location, address, and product-link extraction.
- Pagination across up to five search pages.
- JSON or CSV export through Scrapy feeds.
- Price cleaning, summary statistics, and three analysis plots.

The spider currently uses a fixed search query (`industry machinery`) and city (`bengaluru`). MongoDB connection scaffolding exists, but the insert statement is commented out; database persistence is not enabled.

## Repository structure

```text
scrapy.cfg
tutorial/
    items.py
    settings.py
    pipelines.py
    spiders/
        indamart_data_fetch.py
eda.py
requirements.txt
code_execution_instruction
```

There is no separate ETL directory or notebook in the current repository. Data cleaning is performed by [eda.py](eda.py).

## Getting started

```bash
git clone https://github.com/dionclive-04/data_engineering_challenge.git
cd data_engineering_challenge
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.\.venv\Scripts\Activate.ps1`.
- macOS/Linux: `source .venv/bin/activate`.

Then, from the repository root containing `scrapy.cfg`:

```bash
pip install -r requirements.txt
scrapy list
```

The spider name is `indiamart_api`.

## Collect and analyze data

The spider's existing MongoDB client initialization reads `MONGODB_URI` from the environment. Configure it locally before crawling; never commit credentials. Inserts remain disabled.

Only crawl a site you are authorized to access. The command below enables robots.txt handling for this run.

```bash
scrapy crawl indiamart_api -s ROBOTSTXT_OBEY=True -O output1.json
python eda.py
```

Keep both commands in the repository root so the analysis can find `output1.json`. The `-O` flag replaces that local output file on subsequent runs.

The analysis prints summary statistics and writes:

- `price_distribution.png`
- `top_products_frequency.png`
- `avg_price.png`

To export CSV instead, use `-O products.csv`. The existing analysis script requires the JSON export.

## Limitations and next steps

- Selectors depend on the site's current HTML and may need maintenance.
- The analysis expects non-empty data with the fields emitted by the spider.
- Price cleaning strips non-digit characters; prices with decimals, ranges, or differing units need more careful normalization.
- Search parameters are defined inside the spider rather than exposed as command-line arguments.
- Add saved HTML fixtures and extraction tests before extending the scraper.
- If enabling MongoDB writes, add connection cleanup, error handling, and duplicate prevention.

## Credential maintenance

Any database credential previously committed to Git must be revoked or rotated in MongoDB Atlas. Replacing the current source does not remove credentials from earlier commits.

## Author

[Dion Clive Saldanha](https://github.com/dionclive-04)
