import requests
import argparse
from datetime import datetime, timedelta

ETHERSCAN_API_KEY = 'YOUR_ETHERSCAN_API_KEY'  # Вставьте сюда ваш ключ

def get_transactions(address):
    url = (
        f'https://api.etherscan.io/api?module=account&action=txlist&'
        f'address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}'
    )
    response = requests.get(url)
    data = response.json()
    if data['status'] != '1':
        print(f"[!] Ошибка: {data['message']}")
        return []
    return data['result']

def is_wallet_frozen(transactions, days_threshold):
    if not transactions:
        return True
    last_tx = transactions[-1]
    last_time = datetime.fromtimestamp(int(last_tx['timeStamp']))
    return datetime.utcnow() - last_time > timedelta(days=days_threshold)

def main():
    parser = argparse.ArgumentParser(description="Определение 'замороженных' ETH-кошельков")
    parser.add_argument('addresses', metavar='A', type=str, nargs='+', help='ETH-адреса для анализа')
    parser.add_argument('--days', type=int, default=365, help='Порог неактивности в днях (по умолчанию: 365)')
    args = parser.parse_args()

    print(f"[i] Анализ адресов на предмет неактивности более {args.days} дней...\n")

    for addr in args.addresses:
        print(f"➤ Проверка {addr}...")
        txs = get_transactions(addr)
        frozen = is_wallet_frozen(txs, args.days)
        print(f"  🔒 Заморожен: {'Да' if frozen else 'Нет'}")
        if txs:
            print(f"  Последняя активность: {datetime.fromtimestamp(int(txs[-1]['timeStamp']))}")
        else:
            print("  ⚠️ Нет транзакций (возможно новый или пустой кошелёк)")
        print()

if __name__ == "__main__":
    main()
