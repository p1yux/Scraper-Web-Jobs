from ddgs import DDGS

def get_company_website(company_name, description):
    """Search for the company's official website with description, ignoring Wikipedia, Crunchbase, etc."""
    query = f"{company_name} official site {description}"
    blocked_domains = ["wikipedia.org", "linkedin.com", "crunchbase.com", "glassdoor.com", "indeed.com"]

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    for r in results:
        url = r.get("href", "")
        if not any(b in url for b in blocked_domains):
            return url
    return None

def get_linkedin_url(company_name):
    """Search for the company's LinkedIn page."""
    query = f"{company_name} site:linkedin.com/company"
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=1))
    if results:
        return results[0].get("href")
    return None
