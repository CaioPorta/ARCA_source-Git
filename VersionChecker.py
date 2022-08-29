from BackgroundProcesses import WorkerThread

import os
import re
from pathlib import Path

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class VersionChecker(object):
    def __init__(self, HMI):
        super().__init__()
        self.HMI = HMI
        self.Progress = 0
        self.Title = "Baixando atualização...\nPor favor aguarde...\n"
        self.InProgress = False
        self.StartThread_CheckVersion()

    def StartThread_CheckVersion(self):
        try:
            self.Thread_CheckVersion = WorkerThread('Thread_CheckVersion', self.HMI)
            self.Thread_CheckVersion.start()
        except: pass

    def CheckVersion(self): # Thread_CheckVersion
        try:
            CurrentVersion = self.GetCurrentVersion()
            OnlineVersion = self.GetOnlineVersion()
            if self.HigherVersion(CurrentVersion, OnlineVersion):
                self.HMI.VersionUpdate = True
        except: pass

    def GetOnlineVersion(self):
        Version = ""
        url = "https://github.com/CaioPorta/ARCA/blob/main/HMI.py"
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
            options.add_argument('--window-size=1280,1024')
            browser = webdriver.Chrome(chrome_options=options, executable_path=os.getcwd() + '\\chromedriver.exe')
            browser.set_window_size(1280, 1024)
            DownloadsPath = str(Path.home() / "Downloads")
            browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': DownloadsPath}}
            browser.execute("send_command", params)
            browser.get(url)
            Version = browser.find_element("xpath", '//*[@id="LC52"]/span[4]').get_attribute('innerText')
            browser.close()
            self.HMI.OnlineVersion = Version

        except Exception as error:
            print("Ocorreu um erro inesperado.\nTente novamente mais tarde.\n", error) # Debug
            Version = self.HMI.APPVersion
        finally:
            return Version

    def GetCurrentVersion(self):
        return self.HMI.APPVersion

    def HigherVersion(self, CurrentVersion, OnlineVersion):
        CurrentVersion = re.findall(r'\d+', CurrentVersion)
        OnlineVersion = re.findall(r'\d+', OnlineVersion)
        for i in list(range(6)):
            if OnlineVersion[i] > CurrentVersion[i]: return True
        return False

    def StartThread_UpdateVersion(self):
        try:
            self.InProgress = True
            self.Thread_UpdateVersion = WorkerThread('Thread_UpdateVersion', self.HMI)
            self.Thread_UpdateVersion.start()
        except: pass

    def UpdateVersion(self):
        try:
            self.Title = "Baixando atualização (1/3)\nPor favor aguarde...\n"
            self.Progress = 0
            passo = int(100 / 18)
            self.HMI.LW.show()
            download = ""
            self.Progress += passo
            # url = "https://github.com/CaioPorta/ARCA/archive/refs/heads/main.zip"
            url = "https://1drv.ms/u/s!AnVbpyqr6k2ijJFb8WbILnlp2Mbwew?e=Y2ITSc"
            self.Progress += passo
            currdir = os.getcwd()
            self.Progress += passo
            downloads_path = str(Path.home() / "Downloads")
            self.Progress += passo
            # new_ARCA_path = downloads_path + "/ARCA-main/dist"
            new_ARCA_path = downloads_path + "/dist"
            self.Progress += passo
            # new_ARCAzip_path = downloads_path + "/ARCA-main.zip"
            new_ARCAzip_path = downloads_path + "/dist.zip"
            self.Progress += passo
            options = Options()
            self.Progress += passo
            options.add_argument('--headless')
            self.Progress += passo
            options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
            self.Progress += passo
            options.add_argument('--window-size=1920,1080')
            options.add_argument("--incognito")
            self.Progress += passo
            browser = webdriver.Chrome(chrome_options=options,
                                       executable_path=currdir + '\\chromedriver.exe')
            self.Progress += passo
            browser.set_window_size(1920,1080)
            self.Progress += passo
            DownloadsPath = str(Path.home() / "Downloads")
            self.Progress += passo
            browser.command_executor._commands["send_command"] = (
                "POST", '/session/$sessionId/chromium/send_command')
            self.Progress += passo
            params = {'cmd': 'Page.setDownloadBehavior',
                      'params': {'behavior': 'allow', 'downloadPath': DownloadsPath}}
            self.Progress += passo
            browser.execute("send_command", params)
            self.Progress += passo
            browser.get(url)
            self.Progress += passo
            browser.find_element("xpath",'//*[@id="id__136-menu"]/div/ul/li/button/div/i').click()
            self.Progress = 99

            self.Title = "Baixando atualização (2/3)\nPor favor aguarde...\n"
            self.Progress = 0
            passo = 2

            downloading = True
            #self.abort = False

            while downloading:# and not self.abort: # Wait the download
                if self.Progress < 97: self.Progress += passo
                else: self.Progress = 0
                try:
                    with zipfile.ZipFile(new_ARCAzip_path, 'r') as zip_ref:
                        zip_ref.extractall(downloads_path)
                        os.remove(new_ARCAzip_path)
                        download = "success"
                    downloading = False
                except:
                    time.sleep(0.5)
            self.Progress = 100
            browser.close()
            self.Title = "Baixando atualização (3/3)\nPor favor aguarde...\n"
            self.Progress = 0
            passo = int(100 / 10)
            if download == "success":
                destination = currdir
                print('destination ', destination)
                source = new_ARCA_path + "/ChromeSetup.exe"
                print('source ChromeSetup ', source)
                shutil.copyfile(source, destination)
                self.Progress += passo
                os.startfile(destination + "/ChromeSetup.exe")
                print('startfile ChromeSetup')
                source = new_ARCA_path + "/chromedriver.exe"
                print('source chromedriver ', source)
                shutil.copyfile(source, destination)
                self.Progress += passo
                os.startfile(destination + "/chromedriver.exe")
                print('startfile chromedriver')
                source = new_ARCA_path + "/sounds"
                print('source ', source)
                shutil.copy(source, destination)
                self.Progress += passo
                source = new_ARCA_path + "/images"
                print('source ', source)
                shutil.copy(source, destination)
                self.Progress += passo
                source = new_ARCA_path + "/Bonus"
                print('source ', source)
                shutil.copy(source, destination)
                self.Progress += passo
                source = new_ARCA_path + "/ARCA.exe"
                print('source ', source)
                shutil.copyfile(source, destination)
                self.Progress += passo

                try:
                    print("Tentando remover ARCA.exe do desktop pelo caminho: ", desktop + '/ARCA.exe')
                    os.remove(desktop + '/ARCA.exe')
                    print("Remoção feita COM sucesso")
                except: print("Remoção feita SEM sucesso")
                self.Progress += passo

                print("Criando atalho de ARCA.exe")
                desktop = winshell.desktop()
                path = os.path.join(desktop, 'ARCA.lnk')
                target = destination + "/ARCA.exe"
                icon = destination + "/ARCA.exe"
                print('path: ', path)
                print('target: ', target)
                print('icon: ', icon)
                self.Progress += passo

                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.IconLocation = icon
                shortcut.save()
                self.Progress += passo
                print("Renomeando atalho")
                os.rename(desktop + '/ARCA.exe - Atalho', desktop + '/ARCA.exe')

                print("Removendo pasta: ", downloads_path + "/dist")
                os.remove(downloads_path + "/dist")
                self.Progress = 100

        except Exception as error:
            print("Ocorreu um erro inesperado.\nTente novamente mais tarde.\n", error)  # Debug