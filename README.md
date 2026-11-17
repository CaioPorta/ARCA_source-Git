# ARCA - Your Financial Operations Assistant
  
## Overview
  
This is a Windows application built with Python to help manage personal finances. It uses many libraries, such as Selenium, SQLite3, PyQt5, Matplotlib, OS, yfinance, threading, xlsxwriter, pandas, tkinter, BeautifulSoup, json, requests, and csv. There is still a lot to do, but the core of the app is already operational. Some planned improvements include data processing, analysis, and presentation. 

## Getting Started

1. Install dependencies (see `requirements.txt` at the repo root):
   ```powershell
   pip install -r "requirements.txt"
   ```
2. Install chromedriver, available at src\chromedriver.exe
3. Install Chrome, available at src\ChromeSetup.exe
4. Run the application from the repo root:
   ```powershell
   python ARCA.py
   ```
   The launcher sets up the module path and working directory, so all asset paths (`./images`, `./sounds`) resolve correctly.
5. On first launch, create a profile (username, password, recovery email, and database storage location).

# Project Guide

ARCA is a Windows desktop application (Python) that acts as an **offline personal finance and trading assistant**. It focuses on the Brazilian market (B3 – stocks/FIIs) and cryptocurrencies, handling transaction registration, Brazilian tax computation (Day Trade vs. Swing Trade), portfolio performance, and live market quotes.

## Main functional description

This application is designed to be an assistant for your finances.
With it, you can register all your transactions offline, check the taxes you
owe (automatically separated into Swing Trades and Day Trades), and find out
which financial sector you're most exposed to.
You can also view your returns over time in a simple way, both in percentage
and nominal terms.
To assist you with your decisions, we implemented an algorithm that tracks key
market indicators and provides automated recommendations.

For added security, the app allows you to save your database file
in any folder you want. You can for example save it in a vault like
OneDrive's Vault or on removable storage such as a DVD, flash drive,
or external HDD/SSD.
Also, you can generate a backup file and save wherever you want.

To avoid losing access to your database in case you forget your password,
we ask that you inform your email, so if needed we can unlock your access by reaching
your confirmed email.

Have good trades ;)

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
        ┌─────────────────────┼──────────────────┐──────────────────────────┐
        ▼                     ▼                  ▼                          ▼
 DBManager.py       YahooFinance.py       Calcular.py          BackgroundProcesses.py
 (SQLite access)    (market data API)     (financial math)     (Thread / QThread pool)
        │                                                   │
        └──────────► HMI sub-modules (pages/UI) ◄───────────┘
                     HMI_Trades · HMI_Tributacao · HMI_ARCA ·
                     HMI_Desempenho · HMI_Mercado ·
                     HMI_Trades_Bolsa · HMI_Trades_Criptomoedas
```

### Project layout (To be updated)

Code lives under `src/app/` (flat). Assets live under `src/assets/`. The repo root holds only the launcher, build config, and top-level files.

```
ARCA_source-Git/
├── ARCA.py                 # Launcher: fixes sys.path + chdir into assets, then starts GUI
├── ARCA.spec               # PyInstaller build config
├── requirements.txt        # Python dependencies
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── app/                # all application modules (flat)
│   │   ├── __init__.py
│   │   ├── HMI.py          # main window + page dispatcher
│   │   ├── DBManager.py    # SQLite data layer
│   │   ├── YahooFinance.py # market data
│   │   ├── Calcular.py     # financial math
│   │   ├── BackgroundProcesses.py  # threading model
│   │   ├── VersionChecker.py
│   │   ├── LoadingWindow.py
│   │   ├── CalendarWindow.py
│   │   ├── RelogioWindow.py
│   │   ├── OperacaoRegistradaComSucesso.py
│   │   ├── HMI_Trades.py
│   │   ├── HMI_Tributacao.py
│   │   ├── HMI_ARCA.py
│   │   ├── HMI_Desempenho.py
│   │   ├── HMI_Mercado.py
│   │   ├── HMI_Trades_Bolsa.py
│   │   └── HMI_Trades_Criptomoedas.py
│   └── assets/             # images, sounds, Bonus/, chromedriver.exe
└── docs/  # TODO
```

### Key modules

All modules below live in `src/app/`. `ARCA.py` at the root is a thin launcher.

| File | Responsibility |
|------|----------------|
| `ARCA.py` | Backend - Launcher: adds `src/app` to `sys.path`, chdir into assets, spawns the GUI thread |
| `HMI.py` | Frontend - Main window (`IHMmain`) and page-navigation dispatcher; holds shared app state. Also defines `graphical_thread` |
| `HMI_Trades.py` / `HMI_Trades_Bolsa.py` / `HMI_Trades_Criptomoedas.py` | Frontend - Trade registration, broker management, operations (buy/sell), deposits/withdrawals for stocks and crypto |
| `HMI_Tributacao.py` | Frontend - Tax calculation UI (Day Trade / Swing Trade) |
| `HMI_ARCA.py` | Frontend - Core portfolio pages by asset class (Ações, Real Estate, Caixa, Ativos Internacionais, Criptomoedas) |
| `HMI_Desempenho.py` | Frontend - Performance/returns views |
| `HMI_Mercado.py` | Frontend - Market analysis views |
| `LoadingWindow.py`, `CalendarWindow.py`, `RelogioWindow.py`, `OperacaoRegistradaComSucesso.py` | Frontend - Auxiliary UI |
| `DBManager.py` | Backend - SQLite data-access layer: profile/user management, schema creation, CRUD operations |
| `YahooFinance.py` | Backend - Market-data fetching (yfinance, yahoo_fin, selenium+B3, Binance) |
| `Calcular.py` | Backend - Financial math: portfolio value (`Patrimonio`) and yield (`Rendimento`) |
| `BackgroundProcesses.py` | Backend - Threading helpers – `BackgroundProcess` (threading.Thread) and `WorkerThread` (QThread) |
| `VersionChecker.py` | Backend - Online version check / update |

### Data model

Each user gets a dedicated SQLite database (`<UserPath>\<User>.db`) with tables for profiles, asset types/sectors, holdings (`Bolsa`), quotes (`Cotações`), tax records per month (`Tributação*`), brokers (`Corretoras`), banks (`Bancos`), and fiat/crypto currencies. An internal app database maps usernames to their database paths and recovery emails.

### Threading model

Long-running tasks (fetching tickers, updating quotes, computing taxes) run on background threads so the GUI stays responsive. Shared state is guarded by a `threading.Lock` (`ThreadLock`) in both `HMI.py` and `DBManager.py`.

## Building an executable

The app is packaged into a single `.exe` with PyInstaller using `ARCA.spec`:
```powershell
pyinstaller --onefile --noconsole -i .\core\logoARCA.ico core\ARCA.py
```
This produces the distributable in `dist/`, bundled with `logoARCA.ico`.

## Development resources

The `Guia de Desenvolvimento` folder contains developer notes, sequence diagrams (`Sequencial Diagram.drawio`), DB/HMI maps (PDFs), and screenshot references. 

## TODOs
- Remove unused imports
(Architecture is the most important thing to modify today, so to be easier to give maintenance to the project)
- Mon graphical_thread crée la QApplication et lance la boucle d’événements (exec_()) dans run(). Du coup, je ne peux pas instancier la fenêtre dans un test sans bloquer. De plus, Qt exige que la QApplication et les widgets vivent dans le thread principal : lancer l’UI dans un thread secondaire est fragile.
Je dois séparer la fenêtre du lancement
- Create Functional Tests for the UI
- Create Functional Tests for the APP
- Create Unit Tests
- Unrelate DBManager from HMI
- Modularize HMI.py
- Make DBManager.ThreadLock to be private only
- Cybersecurity, even if the app will run offline
