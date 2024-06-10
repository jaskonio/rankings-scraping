import requests
from bs4 import BeautifulSoup
import pandas as pd

class CronoChipService():
    def getByDorsal(self, circuit_id:str, dorsal_id:str):
        url = "https://cronochip.com/inscripciones/clasificationsCircuits/findbydorsal"

        payload = f'data%5BDorsalFilter%5D%5Bdorsal%5D={dorsal_id}&data%5BDorsalFilter%5D%5Bcircuit_id%5D={circuit_id}&_method=POST'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        soup = BeautifulSoup(response.text, 'lxml')

        headers = []
        header_html = soup.find('thead')

        for th in header_html.find_all('th'):
            if 'class' in th.attrs and 'pruebas' in th['class']:
                pruebas_html = th.find_all('div', {'class': 'prueba'})
                for i in range(1, len(pruebas_html)+1):
                    headers.append(f'Prueba {i}')
            else:
                headers.append(th.get_text())

        rows = []
        tbody_html = soup.find('tbody')

        for tr in tbody_html.find_all('tr'):
            cells = tr.find_all(['td'])
            row = []
            for cell in cells:
                if 'class' in cell.attrs and 'pruebas' in cell['class']:
                    pruebas_html = cell.find_all('div', {'class': 'prueba'})
                    for prueba_html in pruebas_html:
                        row.append(prueba_html.get_text())
                else:
                    row.append(cell.get_text())
            rows.append(row)

        df = pd.DataFrame(rows, columns=headers)
        return df