import asyncio
import os
import httpx
from dotenv import load_dotenv
import datetime

load_dotenv()
token = os.getenv("TOKEN_ORGANIZZE")
headers = {"Authorization": f"Basic {token}", "User-Agent": "rel_gastos_organizze/0.1"}

async def test():
    async with httpx.AsyncClient() as client:
        # Get credit cards
        res = await client.get("https://api.organizze.com.br/rest/v2/credit_cards", headers=headers)
        cards = res.json()
        for card in cards:
            print(f"\nCard: {card['name']} (ID: {card['id']})")
            
            # Find the current invoice (due date > today or just the ones from start_date to end_date)
            hoje = datetime.datetime.now()
            start = (hoje - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            end = (hoje + datetime.timedelta(days=60)).strftime('%Y-%m-%d')
            
            res_inv = await client.get(f"https://api.organizze.com.br/rest/v2/credit_cards/{card['id']}/invoices?start_date={start}&end_date={end}", headers=headers)
            invoices = res_inv.json()
            
            # Find invoice for July (month 7)
            fatura_atual = None
            for inv in invoices:
                dt = datetime.datetime.strptime(inv['date'], '%Y-%m-%d')
                if dt.month == 7 and dt.year == 2026: # July
                    fatura_atual = inv
                    break
            
            if not fatura_atual:
                print("No July invoice found")
                continue
                
            print(f"July Invoice ID: {fatura_atual['id']}, Due Date: {fatura_atual['date']}")
            
            # Fetch transactions for this invoice
            res_tx = await client.get(f"https://api.organizze.com.br/rest/v2/credit_cards/{card['id']}/invoices/{fatura_atual['id']}", headers=headers)
            inv_data = res_tx.json()
            txs = inv_data.get('transactions', [])
            
            print(f"Total transactions in invoice: {len(txs)}")
            for t in txs:
                if 'american' in t['description'].lower() or 'airlines' in t['description'].lower():
                    print(f"!!! FOUND AA TRANSACTION: {t['description']} | Date: {t['date']} | Amount: {t['amount_cents']}")

asyncio.run(test())
