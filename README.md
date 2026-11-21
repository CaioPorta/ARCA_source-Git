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

Within the GUI layer, `src/app/ui/HMI.py` defines the entry point (`graphical_thread`) and composes the main window `IHMmain` from four small mixin modules (one file per concern). This keeps the public surface unchanged while making each UI concern easy to find and maintain — see "IHMmain composition" below.

```
ARCA.py  ──▶  ui/graphical_thread.py    (entry point / main window)
                          │
                          ▼
                 ui/HMI.py: IHMmain         (global variables)
                  ├── HMI_PageNavigation    (page navigation)
                  ├── HMI_PageBuilders      (page creation)
                  ├── HMI_Events            (button/slider/event handlers)
                  └── HMI_Presentation      (display & loading updates)
                  └── HMI_X_page            (the page X manager)
                          │
        ┌─────────────────┼───────────────────────────────┐───────────────────────┐
        ▼                 ▼                               ▼                       ▼
  core/DBManager.py   core/YahooFinance.py    core/Calcular.py    core/BackgroundProcesses.py
  (SQLite access)     (market data API)       (financial math)      (Thread + QThread pool)
```

### IHMmain composition

`IHMmain` is a single `QWidget` subclass whose behaviour is split across four mixin modules in `src/app/ui/home_and_parameters/`, re-composed in `HMI.py`. The public surface (`from ui.HMI import IHMmain`) is unchanged; only the file organization differs.

| Module | Responsibility |
|------|----------------|
| `home_and_parameters/HMI_PageNavigation.py` | `CreatePage` dispatcher + navigation decisions (page transitions, confirmations) |
| `home_and_parameters/HMI_Presentation.py` | Page rendering, layout helpers, header, quote tables |
| `home_and_parameters/HMI_PageBuilders.py` | Per-page widget builders (`CreatePage0` … `CreatePage17`) |
| `home_and_parameters/HMI_Events.py` | Button/key/event handlers (input validation, file import/export) |

Only the lifecycle/state methods (`__init__`, `initialize`, `InicializacaoUsuario`) live directly in `HMI.py`; everything else is inherited from the mixins above.

### Project layout

Code lives under `src/app/`, organized into two packages: `core/` (backend business logic) and `ui/` (PyQt5 front-end). Assets live under `src/assets/`. The repo root holds only the launcher, build config, and top-level files.

```
ARCA_source-Git/
├── ARCA.py                 # Launcher: fixes sys.path + chdir into assets, then starts GUI
├── ARCA.spec               # PyInstaller build config
├── requirements.txt        # Python dependencies
├── src/
│   ├── app/
│   │   ├── core/                         # backend business logic (package)
│   │   │   ├── DBManager.py              # SQLite data-access layer
│   │   │   ├── YahooFinance.py           # market-data fetching
│   │   │   ├── Calcular.py               # financial math
│   │   │   ├── BackgroundProcesses.py    # threading model (Thread / QThread pool)
│   │   │   └── VersionChecker.py         # online version check
│   │   ├── ui/               # PyQt5 front-end (package)
│   │   │   ├── HMI.py                    # entry point + composed IHMmain window (see "IHMmain composition")
│   │   │   ├── pages.py                  # PAGE_BY_NAME / PAGE_BY_ID registry
│   │   │   ├── graphical_thread.py       # QApplication lifecycle / main-window runner
│   │   │   ├── home_and_parameters/      # IHMmain mixin modules (one file per concern)
│   │   │   │   ├── HMI_PageNavigation.py # CreatePage dispatcher + navigation decisions
│   │   │   │   ├── HMI_Presentation.py   # page rendering, layout, header, quote tables
│   │   │   │   ├── HMI_PageBuilders.py   # per-page widget builders (CreatePage0..17)
│   │   │   │   └── HMI_Events.py         # button/key/event handlers
│   │   │   ├── arca/                     # core portfolio pages by asset class
│   │   │   │   └── HMI_ARCA_page.py
│   │   │   ├── desempenho/               # performance/returns views
│   │   │   │   └── HMI_Desempenho_page.py
│   │   │   ├── mercado/                  # market analysis views
│   │   │   │   └── HMI_Mercado_page.py
│   │   │   ├── tributacao/               # tax calculation UI (Day Trade / Swing Trade)
│   │   │   │   └── HMI_Tributacao_page.py
│   │   │   ├── trades/                   # trade registration
│   │   │   │   ├── HMI_Trades_page.py
│   │   │   │   ├── trades_bolsa/         # stocks (Bolsa) trades
│   │   │   │   │   └── HMI_Trades_Bolsa_page.py
│   │   │   │   └── trades_criptomoedas/  # crypto trades
│   │   │   │       └── HMI_Trades_Criptomoedas_page.py
│   │   │   └── popup/                    # modal popups (loading, calendar, clock, success)
│   │   │       ├── __init__.py
│   │   │       ├── CalendarWindow.py
│   │   │       ├── LoadingWindow.py
│   │   │       ├── RelogioWindow.py
│   │   │       └── OperacaoRegistradaComSucesso.py
│   │   └── assets/                       # images, sounds, chromedriver.exe
└── docs/
    ├─── Bonus                            # Legacy: How I used to do before this app
    └─── Guia de Desenvolvimento          # The project HMI arquichecture, some instructions about compiling
```

### Key modules

All modules below live in `src/app/core/` (backend) or `src/app/ui/` (frontend). `ARCA.py` at the root is a thin launcher.

| File | Responsibility |
|------|----------------|
| `ARCA.py` | Backend - Launcher: adds `src/app` to `sys.path`, chdir into assets, spawns the GUI thread |
| `ui/HMI.py` | Frontend - Entry point (`graphical_thread`) and composed main window (`IHMmain`). Holds only lifecycle/state; see "IHMmain composition" for the four mixins it inherits from |
| `ui/home_and_parameters/HMI_PageNavigation.py` | Frontend - mixin: `CreatePage` dispatcher + navigation decisions |
| `ui/home_and_parameters/HMI_Presentation.py` | Frontend - mixin: page rendering, layout helpers, header, quote tables |
| `ui/home_and_parameters/HMI_PageBuilders.py` | Frontend - mixin: per-page widget builders (`CreatePage0` … `CreatePage17`) |
| `ui/home_and_parameters/HMI_Events.py` | Frontend - mixin: button/key/event handlers (input validation, file import/export) |
| `ui/trades/HMI_Trades_page.py` / `ui/trades/trades_bolsa/HMI_Trades_Bolsa_page.py` / `ui/trades/trades_criptomoedas/HMI_Trades_Criptomoedas_page.py` | Frontend - Trade registration, broker management, operations (buy/sell), deposits/withdrawals for stocks and crypto |
| `ui/tributacao/HMI_Tributacao_page.py` | Frontend - Tax calculation UI (Day Trade / Swing Trade) |
| `ui/arca/HMI_ARCA_page.py` | Frontend - Core portfolio pages by asset class (Ações, Real Estate, Caixa, Ativos Internacionais, Criptomoedas) |
| `ui.desempenho/HMI_Desempenho_page.py` | Frontend - Performance/returns views |
| `ui/mercado/HMI_Mercado_page.py` | Frontend - Market analysis views |
| `ui/popup/*` (`LoadingWindow`, `CalendarWindow`, `RelogioWindow`, `OperacaoRegistradaComSucesso`) | Frontend - Auxiliary UI / modal popups |
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
(Architecture is the most important thing to modify today, so to be easier to give maintenance to the project)
01 - Create Functional Tests for the UI
02 - Create Functional Tests for the APP
03 - Create Unit Tests
04 - Make DBManager to be independent from HMI thread
05 - Modularize HMI.py -> DONE: `IHMmain` behaviour is now split in `src\app\ui\home_and_parameters` across `HMI_PageNavigation`, `HMI_Presentation`, `HMI_PageBuilders`, `HMI_Events`
06 - Modularize HMI_ARCA_page.py -> `HMI_ARCA` behaviour needs to split in `src\app\ui\arca` across `PageNavigation`, `Presentation`, `PageBuilders`, `Events`
07 - Modularize HMI_Desempenho_page.py -> `HMI_Desempenho` behaviour needs to split in `src\app\ui\desempenho` across `PageNavigation`, `Presentation`, `PageBuilders`, `Events`
08 - Modularize HMI_Mercado_page.py -> `HMI_Mercado` behaviour needs to split in `src\app\ui\mercado` across `PageNavigation`, `Presentation`, `PageBuilders`, `Events`
09 - Modularize HMI_Tributacao_page.py -> `HMI_Tributacao` behaviour needs to split in `src\app\ui\tributacao` across `PageNavigation`, `Presentation`, `PageBuilders`, `Events`
10 - Modularize HMI_Trades_page.py -> `HMI_Trades` behaviour needs to split in `src\app\ui\trades` across `PageNavigation`, `Presentation`, `PageBuilders`, `Events`
11 - Modularize HMI_Trades_Bolsa_page.py -> `HMI_Trades_Bolsa` behaviour needs to split in `src\app\ui\trades_bolsa` across `PageNavigation`, `Presentation`, `PageBuilders`, `Events`
12 - Modularize HMI_Trades_Criptomoedas_page.py -> `HMI_Trades_Criptomoedas` behaviour needs to split in `src\app\ui\trades_criptomoedas` across `PageNavigation`, `Presentation`, `PageBuilders`, `Events`
13 - Make DBManager.ThreadLock to be private only
14 - Cybersecurity, even if the app will run offline

Crashes:
DEFECT 1 - self.HMI.Movie_AlterarOPBolsa.setScaledSize(QSize().scaled(self.HMI.frameGeometry().width()*12/20/2,self.HMI.frameGeometry().height()*7/10*.95-30, Qt.KeepAspectRatio))
DEFECT 2 - GetAllTickers 
   HTTP Error 403: Forbidden
DEFECT 3 - WebDriver.__init__() got an unexpected keyword argument 'chrome_options'
DEFECT 4 - When sending a verification email, when creating a new account: QObject::startTimer: Timers cannot be started from another thread
DEFECT 5 - When trying to go to page Desempenho:
   Traceback (most recent call last):
   File "f:\Projetos_pessoais_offline\ARCA_source-Git\src\app\ui\home_and_parameters\HMI_PageBuilders.py", line 257, in <lambda>
      self.Button_DesempenhoInvisivel.pressed.connect(lambda: self.CreatePage(PAGE_BY_NAME['Desempenho'].page_id))
                                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   File "f:\Projetos_pessoais_offline\ARCA_source-Git\src\app\ui\home_and_parameters\HMI_PageNavigation.py", line 631, in CreatePage
      self.HMI_Desempenho.CreatePage12()
   File "f:\Projetos_pessoais_offline\ARCA_source-Git\src\app\ui\desempenho\HMI_Desempenho_page.py", line 71, in CreatePage12
      self.HMI.Movie_Grafico1.setScaledSize(QSize().scaled(self.HMI.frameGeometry().width(),self.HMI.frameGeometry().height()/5*.95, Qt.KeepAspectRatio))
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   TypeError: arguments did not match any overloaded call:
   scaled(self, s: QSize, mode: Qt.AspectRatioMode): argument 1 has unexpected type 'int'
   scaled(self, w: int, h: int, mode: Qt.AspectRatioMode): argument 2 has unexpected type 'float'
