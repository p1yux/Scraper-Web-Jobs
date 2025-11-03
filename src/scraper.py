import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_career_page(website):
    """Find a likely career page (including subdomains or nested paths)."""
    if not website:
        return None
    try:
        resp = requests.get(website, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            if any(keyword in href for keyword in ["career","about-us/careers", "about/careers", "careers", "jobs", "join-us", "work-with-us"]):
                return urljoin(website, href)
    except Exception as e:
        print(f"[WARN] Could not find career page for {website}: {e}")
    return None


def get_top_jobs(career_page):
    """Extract up to 3 job postings from common job platforms."""
    if not career_page:
        return []
    try:
        resp = requests.get(career_page, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        jobs = []

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if any(platform in href for platform in ["personio.com", "greenhouse.io", "lever.co", "teamtailor.com"]):
                return detect_jobs_from_platform(href)

            if any(word in text.lower() for word in ["engineer", "manager", "developer", "intern", "designer"]):
                job_url = urljoin(career_page, href)
                jobs.append({"title": text, "url": job_url})
                if len(jobs) >= 3:
                    break
        return jobs
    except Exception as e:
        print(f"[WARN] Error while fetching jobs: {e}")
        return []


def detect_jobs_from_platform(job_page_url):
    """Special handler for Personio/Lever/Greenhouse job boards."""
    try:
        resp = requests.get(job_page_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        jobs = []
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            if text and any(word in text.lower() for word in ["manager", "developer", "engineer", "intern", "specialist"]):
                job_url = a["href"]
                if not job_url.startswith("http"):
                    job_url = urljoin(job_page_url, job_url)
                jobs.append({"title": text, "url": job_url})
            if len(jobs) >= 3:
                break
        return jobs
    except:
        return []
