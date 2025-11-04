import csv
from src.search import get_company_website, get_linkedin_url
from src.scraper import find_career_page, get_top_jobs

INPUT_FILE = "data/raw_companies.csv"
OUTPUT_FILE = "data/final_output.csv"

def enrich_company(company_name, description):
    print(f"\nProcessing: {company_name}")
    website = get_company_website(company_name, description)
    linkedin = get_linkedin_url(company_name)
    career_page = find_career_page(website)
    top_jobs = get_top_jobs(career_page)

    result = {
        "Company Name": company_name,
        "Company Description": description,
        "Website URL": website or "",
        "Linkedin URL": linkedin or "",
        "Careers Page URL": career_page or "",
        "Job listings page URL": career_page or "",
    }

    for i, job in enumerate(top_jobs[:3], start=1):
        result[f"job post{i} URL"] = job.get("url", "")
        result[f"job post{i} title"] = job.get("title", "")

    for i in range(len(top_jobs) + 1, 4):
        result[f"job post{i} URL"] = ""
        result[f"job post{i} title"] = ""

    return result


def main():
    results = []
    with open(INPUT_FILE, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            company_name = row.get("Company Name") or row.get("company_name")
            description = row.get("Company Description") or row.get("description")
            if company_name and description:
                results.append(enrich_company(company_name.strip(), description.strip()))

    fieldnames = [
        "Company Name",
        "Company Description",
        "Website URL",
        "Linkedin URL",
        "Careers Page URL",
        "Job listings page URL",
        "job post1 URL",
        "job post1 title",
        "job post2 URL",
        "job post2 title",
        "job post3 URL",
        "job post3 title",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone! Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

# # xlxs
# import csv
# import pandas as pd
# from src.search import get_company_website, get_linkedin_url
# from src.scraper import find_career_page, get_top_jobs

# INPUT_FILE = "data/raw_companies.csv"
# OUTPUT_FILE = "data/final_output.xlsx"  # Save as Excel file

# def enrich_company(company_name, description):
#     print(f"\nProcessing: {company_name}")
#     website = get_company_website(company_name)
#     linkedin = get_linkedin_url(company_name)
#     career_page = find_career_page(website)
#     top_jobs = get_top_jobs(career_page)

#     result = {
#         "Company Name": company_name,
#         "Company Description": description,
#         "Website URL": website or "",
#         "Linkedin URL": linkedin or "",
#         "Careers Page URL": career_page or "",
#         "Job listings page URL": career_page or "",
#     }

#     for i, job in enumerate(top_jobs[:3], start=1):
#         result[f"job post{i} URL"] = job.get("url", "")
#         result[f"job post{i} title"] = job.get("title", "")

#     # Fill empty slots if fewer than 3 jobs
#     for i in range(len(top_jobs) + 1, 4):
#         result[f"job post{i} URL"] = ""
#         result[f"job post{i} title"] = ""

#     return result


# def main():
#     results = []
#     with open(INPUT_FILE, "r", encoding="utf-8-sig", errors="ignore") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             company_name = row.get("Company Name") or row.get("company_name")
#             description = row.get("Company Description") or row.get("description")
#             if company_name and description:
#                 results.append(enrich_company(company_name.strip(), description.strip()))

#     # Convert results list to DataFrame
#     df = pd.DataFrame(results)

#     # Save to Excel
#     df.to_excel(OUTPUT_FILE, index=False, engine="openpyxl")

#     print(f"\n✅ Done! Results saved to {OUTPUT_FILE}")


# if __name__ == "__main__":
#     main()
