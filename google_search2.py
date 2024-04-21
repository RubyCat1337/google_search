import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

def google_search(query, num_results=5):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all("div", class_="tF2Cxc")
    
    def extract_info(result):
        title = result.find("h3").get_text() if result.find("h3") else "Нет заголовка"
        snippet = result.find("span", class_="aCOpRe").get_text() if result.find("span", class_="aCOpRe") else "Нет сниппета"
        time_info = result.find("span", class_="LEwnzc").get_text() if result.find("span", class_="LEwnzc") else "Нет информации о времени"
        link = result.find("a")["href"]
        return title, snippet, time_info, link

    results = []
    with ThreadPoolExecutor() as executor:
        for idx, result in enumerate(search_results[:num_results], start=1):
            title, snippet, time_info, link = executor.submit(extract_info, result).result()
            results.append((idx, title, snippet, time_info, link))

    for idx, title, snippet, time_info, link in results:
        print(f"Результат {idx}:")
        print(f"Заголовок: {title}")
        print(f"Время: {time_info}")
        print(f"Сниппет: {snippet}")
        print(f"Ссылка: {link}")
        print("-" * 50)

query = input("Введите запрос для поиска: ")
google_search(query)
