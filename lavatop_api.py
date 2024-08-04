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


