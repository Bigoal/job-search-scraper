import requests
from bs4 import BeautifulSoup


def fetch_jobs(url):
    """Fetch and parse job listings from a given URL."""
    print("Extracting Jobs...")
    try:
        page = requests.get(url, timeout=10) 
        page.raise_for_status()
        return BeautifulSoup(page.content, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return None 


def search_jobs(soup, keyword):
    """Search for jobs containing the keyword in their title."""
    if not soup:
        return []
    jobs_found = soup.find_all("h2", string=lambda text: text and keyword.lower() in text.lower()
    )
    
    # Get parent card elements for each found job title
    jobs_found_cards = [
        card.find_parent("div", class_="card") 
        for card in jobs_found
        if card.find_parent("div", class_="card")
    ]
    
    return jobs_found_cards


def display_job_details(jobs_found_cards, keyword):
    """Display details of found job cards."""
    if not jobs_found_cards:
        print(f"No jobs found with keyword: '{keyword}'\n")
        print("-" * 40)
        return
    
    print(f"\nFound {len(jobs_found_cards)} job(s) with keyword '{keyword}':\n")
    
    for i, card in enumerate(jobs_found_cards, 1):
        title = card.find(class_="title")
        company = card.find(class_="company")
        location = card.find(class_="location")
        Applying_link = card.find_all("a")[1]["href"]        
        print(f"Job #{i}:")
        print(f"  Title: {title.text.strip() if title else 'Not specified'}")
        print(f"  Company: {company.text.strip() if company else 'Not specified'}")
        print(f"  Location: {location.text.strip() if location else 'Not specified'}")
        print(f"  Applying link: {Applying_link}")
        print()
    
    print("-" * 40)


def main():
    """Main function to run the job search application."""
    URL = "https://realpython.github.io/fake-jobs/"
    
    soup = fetch_jobs(URL)
    if not soup:
        print("Failed to fetch job listings. Exiting...")
        return
    
    print("\n" + "=" * 50)
    print("JOB SEARCH PORTAL".center(50))
    print("=" * 50)
    
    while True:
        keyword = input("\nEnter the keyword you want to search with (or 'exit' to quit): ").strip().lower()
        
        if keyword == "exit":
            print("\nExiting... Thank you for using Job Search Portal!")
            break
        
        if not keyword:
            print("Please enter a keyword.")
            continue
        
        found_jobs = search_jobs(soup, keyword)
        display_job_details(found_jobs, keyword)


if __name__ == "__main__":
    main()