import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN_ORGANIZZE")
headers = {"Authorization": f"Basic {token}", "User-Agent": "rel_gastos_organizze/0.1"}

async def test():
    async with httpx.AsyncClient() as client:
        url = "https://api.organizze.com.br/rest/v2/transactions?start_date=2026-05-11&end_date=2026-07-10"
        res1 = await client.get(url, headers=headers)
        txs = res1.json()
        dates = [t['date'] for t in txs]
        cc_txs = [t for t in txs if t.get('credit_card_id')]
        print(f"Total: {len(txs)}")
        print(f"CC Txs: {len(cc_txs)}")
        if dates:
            print(f"Min date: {min(dates)}, Max date: {max(dates)}")

asyncio.run(test())
