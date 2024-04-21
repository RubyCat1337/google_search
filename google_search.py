import requests
from bs4 import BeautifulSoup

query = input("Введите запрос для поиска: ")

def google_search(query, num_results=5):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find_all("div", class_="tF2Cxc")
        for idx, result in enumerate(search_results[:num_results], start=1):
            title_tag = result.find("h3")
            title = title_tag.get_text() if title_tag else "Нет заголовка"
            snippet_tag = result.find("span", class_="aCOpRe")
            snippet = snippet_tag.get_text() if snippet_tag else "Нет сниппета"
            time_tag = result.find("span", class_="LEwnzc")
            time_info = time_tag.get_text() if time_tag else "Нет информации о времени"
            link = result.find("a")["href"]
            print(f"Результат {idx}:")
            print(f"Заголовок: {title}")
            print(f"Время: {time_info}")
            print(f"Сниппет: {snippet}")
            print(f"Ссылка: {link}")
            print("-" * 50)
        
    else:
        print("Ошибка при выполнении запроса")


google_search(query)
