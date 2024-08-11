import requests
import datetime as dt


class CryptoApi:
    def __init__(self, account_id):
        self.account_id = account_id

    def find_transactions(self, transaction_id):
        url = f"https://api.trongrid.io/v1/accounts/{self.account_id}/transactions/trc20"
        response = requests.get(url, params={"only_confirmed": True, "limit": 10}, headers={"accept": "application/json"})

        for transaction in response.json()['data']:
            if transaction['to'] == self.account_id and transaction['transaction_id'] == transaction_id:
                return transaction

        return False

    def get_transactions(self):
        url = f"https://api.trongrid.io/v1/accounts/{self.account_id}/transactions/trc20"
        response = requests.get(url, params={"only_confirmed": True, "limit": 10}, headers={"accept": "application/json"})
        ids = []
        for transaction in response.json()['data']:
            transaction_id = transaction['transaction_id']
            ids.append(transaction_id)
            time = dt.datetime.fromtimestamp(float(transaction['block_timestamp']) / 1000)
            # print(time.strftime("%Y-%m-%d"), dt.datetime.now().strftime("%Y-%m-%d"))
            # if time.strftime("%Y-%m-%d") != dt.datetime.now().strftime("%Y-%m-%d"):
            #     break
            value = float(transaction['value'][:-6]+'.'+transaction['value'][-6:])
            # if transaction['to'] == self.account_id:
            #     print(time , transaction_id, value)
        return ids

if __name__ == '__main__':
    account_id = 'TUpjgCrB1np6vE93dPMRKNcCc35TstEfU7'
    api = CryptoApi(account_id)

    api.get_transactions()

