from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


def get_page_count(keyword):
    browser_url = (
        "https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword="
    )
    browser = webdriver.Chrome()
    browser.get(f"{browser_url}{keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("div", class_="pasination")
    if pagination == None:
        return 1
    pages = pagination.find_all("div", recursive=False)
    count = len(pages)
    if count >= 10:
        return 10
    else:
        return count


def extract_saramin_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        browser_url = "https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword="
        final_url = f"{browser_url}{keyword}&recruitPage={page + 1}"
        print("Requesting", final_url)
        browser = webdriver.Chrome()
        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")

        job_list = soup.find("div", class_="content")
        jobs = job_list.find_all("div", recursive=False)
        for job in jobs:
            zone = job.find("div", class_="recruit_info_list")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor["title"]
                link = anchor["href"]
                company = job.find("strong", class_="corp_name")
                location = job.select_one("div.job_condition > span")

                job_data = {
                    "link": f"https://www.saramin.co.kr{link}",
                    "company": company.a.get_text(strip=True) if company else "N/A",
                    "location": location.get_text(strip=True) if location else "N/A",
                    "position": title.replace(",", " "),
                }

                results.append(job_data)

    return results
