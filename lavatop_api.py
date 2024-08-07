import requests


class LavaTopAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'accept': 'application/json',
            'X-Api-Key': self.token
        }

    def get_products(self):
        response = requests.get('https://gate.lava.top/api/v2/products', headers=self.headers)
        return response

    def create_link(self, offer_id, currency='EUR', email='test@gmail.com'):
        # NOT item id
        # you need like this products_list.json()['items']['offers'][0]['id']
        json = {
                "email": email,
                "offerId": offer_id,
                "currency": currency,
                "buyerLanguage": "EN"
        }
        headers = self.headers | {"Content-Type": "application/json"}
        response = requests.post('https://gate.lava.top/api/v2/invoice', headers=headers, json=json)
        return response

    def get_paymant_by_id(self, id):
        response = requests.get(f'https://gate.lava.top/api/v1/invoice/', headers=self.headers, params={'id': id})
        return response



if __name__ == '__main__':
    token = '5qrdAsdvjyj9yvXCWj7uEhQBP9rpEqkM2JXPVaVEWijM0Fgmt7CXKmG6NVDCMAzy'
    api = LavaTopAPI(token)
    # resp = api.create_link('4ccc40c5-dabd-44aa-b4fb-27ae1cdfb987', 'RUB')
    # print(resp.json())
    # link = api.get_paymant_by_id('ae2e4773-ab9e-4855-ab04-20941361a6e1')
    # print(link.json())

    # products_list = api.get_products()
    # if products_list:
    #     print(products_list.json()['items'][0]['offers'][0]['id'])
    #     link_response = api.create_link(products_list.json()['items'][0]['offers'][0]['id'], currency='USD')
    #     if link_response:
    #         id = link_response.json()['id']
    #         link = link_response.json()['paymentUrl']
    #         print(id, link)
    # payment = api.get_paymant_by_id('e5851539-6d63-4798-85cf-f7453be99049')
    # print(payment.json())


'''{'id': 'ae2e4773-ab9e-4855-ab04-20941361a6e1', 'status': 'in-progress', 'amountTotal': {'currency': 'RUB', 'amount': 50.0}, 'paymentUrl': 'https://app.lava.top/products/6870bed1-be74-4b69-977c-8471ad3c7ee4/4ccc40c5-dabd-44aa-b4fb-27ae1cdfb987?paymentParams=CiAgICAgICAgewogICAgICAgICAgImludm9pY2VJZCI6ICJhZTJlNDc3My1hYjllLTQ4NTUtYWIwNC0yMDk0MTM2MWE2ZTEiLAogICAgICAgICAgInBheW1lbnRTZXR0aW5ncyI6IHsiaWQiOiJhZTJlNDc3My1hYjllLTQ4NTUtYWIwNC0yMDk0MTM2MWE2ZTEiLCJ0eXBlIjoiaW52b2ljZSIsInN0YXR1cyI6ImluLXByb2dyZXNzIiwiYW1vdW50X3RvdGFsIjp7ImN1cnJlbmN5IjoiUlVCIiwiYW1vdW50Ijo1MC4wfSwicHJvdmlkZXIiOnsibmFtZSI6ImJhbmsxMzEiLCJwYXJhbWV0ZXJzIjp7InB1YmxpY190b2tlbiI6IjU0ZDFjODYxOWE4ZmIzZmY0YWQxZGEyZDU4MjdhYWE5YTkyMDQyZDExZDMxZTJiY2YzZTk4NDEzNjExMGRmMmEiLCJzdHlsZXNoZWV0IjoiaHR0cHM6Ly93aWRnZXQuYmFuazEzMS5ydS9wYXltZW50LWZvcm0uY3NzIiwic2NyaXB0IjoiaHR0cHM6Ly93aWRnZXQuYmFuazEzMS5ydS9wYXltZW50LWZvcm0uanMifX19CiAgICAgICAgfQogICAgICA'}'''
'''{'id': 'ae2e4773-ab9e-4855-ab04-20941361a6e1', 'status': 'in-progress', 'amountTotal': {'currency': 'RUB', 'amount': 50.0}}'''