from bs4 import BeautifulSoup

def get_method_data(html, method_name):
    soup = BeautifulSoup(html, 'html.parser')

    start = soup.find("a", attrs = {'name': lambda L: L and L.startswith(method_name)})

    div = start.findNext("div")

    #print(test)
    cleaned_div = " ".join(div.get_text().replace("\n", " ").split())
    dl = div.findNext("dl")
    cleaned_dl = " ".join(dl.get_text().replace("\n", " ").split())

    final = cleaned_div + " " + cleaned_dl

    print(final)

    return 1    