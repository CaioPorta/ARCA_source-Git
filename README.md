---

# Original Project Description (by the author)

> The following text is the original content of this repository's README.md, preserved verbatim.

# ARCA
 Development of ARCA aplication
  
 Resume: 
  
I've made a windows APP using Python. The software was made to assist the treatment of my financial operations. In this software, I use many libraries, such as Selenium, SQLite3, PyQt5, MatplotLib, OS, yahoofinance, threading, xlsxwriter, pandas, tkinter, BeautifulSoup, json, requests, csv and so on. There are many things to do yet, but the APP base is already operational. Some of these things to improve are data treatment, data analysis and data presentation. 

Full description:

This aplication is meant to be an assistant to your financial life.
With this aplication you will be able to register all your transactions in a
offline way, check for tributations you owe (separed automatically by
Swing Trades and Day Trades) and get to know to which financial sector you are
more exposed.
Also, you can view in a simple way your returnings through time percentionally
and nominally.
To auxiliate in your decisions, we have implemented an algorithm to help you
catch some important market indicators and get some robot's recommendations.

Worried about your security, the app allows you to save your database file
in any folder you want. You can for exemple save it in a vault like
OneDrive's Vault or in a removable disk like DVD, Pendrive, external HD/SSD etc.
Also, you can generate a backup file and save wherever you want.

To don't loose your access to your database in case you forget your password,
we ask to inform your email, so if needed we can unlock your access by reaching
your confirmed email.

Have good trades ;)

---

# ARCA — Project Guide

ARCA is a Windows desktop application (Python) that acts as an **offline personal finance and trading assistant**. It focuses on the Brazilian market (B3 – stocks/FIIs) and cryptocurrencies, handling transaction registration, Brazilian tax computation (Day Trade vs. Swing Trade), portfolio performance, and live market quotes.

## Features

- **Offline transaction ledger** – register stock (Bolsa) and crypto (Cripto) trades, deposits, and withdrawals.
- **Brazilian tax engine** – automatically separates *Day Trades* and *Swing Trades* and computes owed taxes/loss carry-forward per B3 rules.
- **Performance tracking** – portfolio returns over time, both nominal and percentage.
- **Market analysis** – sector exposure breakdown and market indicators.
- **Live quotes** – prices for stocks, FIIs, and fiat/crypto fetched from Yahoo Finance / yahoo_fin and Binance.
- **Security & portability** – password-protected profiles, email-based recovery, and the ability to store the SQLite database anywhere (vault, external drive) plus manual backups.

## Architecture

The app follows a layered design: a PyQt5 GUI front-end, a data-access layer over SQLite, a market-data layer, and a background-threading model for non-blocking operations.

```
ARCA.py  ─────────────▶  HMI.graphical_thread()   (entry point / main window)
                              │
        ┌───────────────────┼─────────────────────────────────────────────┐
        ▼                  ▼                   ▼                          ▼
 DBManager.py       YahooFinance.py       Calcular.py          BackgroundProcesses.py
 (SQLite access)    (market data API)     (financial math)     (Thread / QThread pool)
        │                                                  │
        └──────────► HMI sub-modules (pages/UI) ◄───────────┘
                     HMI_Trades · HMI_Tributacao · HMI_ARCA ·
                     HMI_Desempenho · HMI_Mercado ·
                     HMI_Trades_Bolsa · HMI_Trades_Criptomoedas
```

### Key modules

| File | Responsibility |
|------|----------------|
| `ARCA.py` | Entry point. Spawns the GUI thread. |
| `HMI.py` | Main window (`IHMmain`) and page-navigation dispatcher; holds shared app state. Also defines `graphical_thread`. |
| `HMI_Trades.py` / `HMI_Trades_Bolsa.py` / `HMI_Trades_Criptomoedas.py` | Trade registration, broker management, operations (buy/sell), deposits/withdrawals for stocks and crypto. |
| `HMI_Tributacao.py` | Tax calculation UI (Day Trade / Swing Trade). |
| `HMI_ARCA.py` | Core portfolio pages by asset class (Ações, Real Estate, Caixa, Ativos Internacionais, Criptomoedas). |
| `HMI_Desempenho.py` | Performance/returns views. |
| `HMI_Mercado.py` | Market analysis views. |
| `DBManager.py` | SQLite data-access layer: profile/user management, schema creation, CRUD operations. |
| `YahooFinance.py` | Market-data fetching (yfinance, yahoo_fin, selenium+B3, Binance). |
| `Calcular.py` | Financial math: portfolio value (`Patrimonio`) and yield (`Rendimento`). |
| `BackgroundProcesses.py` | Threading helpers – `BackgroundProcess` (threading.Thread) and `WorkerThread` (QThread). |
| `VersionChecker.py` | Online version check / update. |
| `LoadingWindow.py`, `CalendarWindow.py`, `RelogioWindow.py`, `OperacaoRegistradaComSucesso.py` | Supporting UI windows. |

### Data model

Each user gets a dedicated SQLite database (`<UserPath>\<User>.db`) with tables for profiles, asset types/sectors, holdings (`Bolsa`), quotes (`Cotações`), tax records per month (`Tributação*`), brokers (`Corretoras`), banks (`Bancos`), and fiat/crypto currencies. A global `Users.db` (in the working directory) maps usernames to their database paths and recovery emails.

### Threading model

Long-running tasks (fetching tickers, updating quotes, computing taxes) run on background threads so the GUI stays responsive. Shared state is guarded by a `threading.Lock` (`ThreadLock`) in both `HMI.py` and `DBManager.py`.

## Getting Started

1. Install dependencies (see `Guia de Desenvolvimento/requirements.txt`):
   ```powershell
   pip install -r "Guia de Desenvolvimento/requirements.txt"
   ```
2. Run the application:
   ```powershell
   python ARCA.py
   ```
3. On first launch, create a profile (username, password, recovery email, and database storage location).

## Building an executable

The app is packaged into a single `.exe` with PyInstaller using `ARCA.spec`:
```powershell
pyinstaller ARCA.spec
```
This produces the distributable in `dist/`, bundled with `logoARCA.ico`.

## Development resources

The `Guia de Desenvolvimento/` folder contains developer notes, sequence diagrams (`Sequencial Diagram.drawio`), DB/HMI maps (PDFs), screenshot references, and the dependency list.

> Note: The original README is preserved verbatim in the section above this guide.
