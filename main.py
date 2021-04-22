"""
BAŞTAN YAZILACAK.
"""

from __future__ import print_function

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from GUI import Ui_AnaPencere

from time import localtime, strftime
from fonksiyonlar import *
import requests

# VALIDATOR KÜTÜPHANELERİ
import functools
import logging
import time
"""
from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver

from Desfire.DESFire import *
from Desfire.util import byte_array_to_human_readable_hex
from Desfire.pcsc import PCSCDevice
"""
IGNORE_EXCEPTIONS = (KeyboardInterrupt, MemoryError,)

global ekran
ekran=0
global kartVar
kartVar = False
global strAlias
strAlias = ""
global strY_Bakiye
strY_Bakiye = ""
global strE_Bakiye
strE_Bakiye = ""
global strTip 
strTip=""
global strVize
strVize=""
global yukleme
yukleme=True
global eklenecekBakiye
eklenecekBakiye = 0
global miktarResetle
miktarResetle=False
global yukletme
yukletme=True

def sunucuyaBas(alias,tip,isletmeID,isletmeADI,posID,oncekiTutar,sonrakiBakiye,yuklenenTutar):
    url = "http://arge.local:8003/api/kartdolum" 
    data = {
        "kartAliasNo": alias, # aliasNo
        "kartTipi": tip, # Öğrenci
        "kartBakiye":float(sonrakiBakiye),
        "öncekiTutar": float(oncekiTutar), # 12
        "yüklenenTutar" : float(yuklenenTutar),
        "bakiyeDolumTarihi" : time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
        "isletmeId": isletmeID,
        "isletmeAdi":isletmeADI,
        "posId": posID
        }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r)
    return r

def catch_gracefully():
    """Function decorator to show any Python exceptions occured inside a function.
    Use when the underlying thread main loop does not provide satisfying exception output.
    """
    def _outer(func):

        @functools.wraps(func)
        def _inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if isinstance(e, IGNORE_EXCEPTIONS):
                    raise
                else:
                    logger.error("Catched exception %s when running %s", e, func)
                    logger.exception(e)

        return _inner

    return _outer
"""
class MyObserver(CardObserver):
    \"\"\"Observe when a card is inserted. Then try to run DESFire application listing against it.\"\"\"

    # We need to have our own exception handling for this as the
    # # main loop of pyscard doesn't seem to do any exception output by default
    #matris= [[7e, 12,4a,a8,82,11,2c,0f,5d,7c,12,95,9a,ae,c1,44], [7e,12,4a,a8,82,11,2c,0f,5d,7c,12,95,9a,ae,c1,44]];
    matris = [[69 ,89 ,236 ,204 ,38 ,136 ,123 ,20 ,112 ,117 ,215 ,251 ,17 ,144 ,25 ,66] , [15 ,134 ,34 ,233 ,76 ,199 ,236 ,152 ,39 ,17 ,105 ,66 ,4 ,188 ,246 ,253] , [212 ,11 ,82 ,42 ,220 ,186 ,112 ,65 ,188 ,36 ,63 ,21 ,14 ,113 ,208 ,84] , [31 ,236 ,15 ,121 ,137 ,57 ,87 ,146 ,23 ,138 ,89 ,46 ,135 ,80 ,46 ,48] , [136 ,194 ,249 ,247 ,161 ,79 ,4 ,123 ,54 ,231 ,73 ,117 ,61 ,101 ,21 ,11] , [110 ,199 ,81 ,168 ,248 ,3 ,154 ,133 ,158 ,36 ,183 ,229 ,122 ,2 ,1 ,200] , [133 ,98 ,63 ,250 ,9 ,223 ,183 ,175 ,163 ,248 ,247 ,6 ,204 ,180 ,2 ,161] , [190 ,76 ,58 ,100 ,249 ,49 ,74 ,130 ,152 ,66 ,188 ,15 ,175 ,176 ,146 ,26] , [38 ,207 ,202 ,202 ,157 ,149 ,98 ,93 ,101 ,121 ,8 ,60 ,61 ,94 ,146 ,80] , [149 ,238 ,27 ,22 ,196 ,203 ,147 ,16 ,217 ,123 ,58 ,199 ,123 ,56 ,18 ,20] , [163 ,157 ,176 ,49 ,32 ,19 ,180 ,106 ,70 ,190 ,219 ,154 ,21 ,102 ,84 ,216] , [93 ,88 ,2 ,51 ,48 ,149 ,200 ,213 ,184 ,107 ,206 ,30 ,55 ,221 ,28 ,74] , [137 ,82 ,123 ,82 ,115 ,24 ,97 ,126 ,6 ,86 ,68 ,154 ,178 ,246 ,27 ,191] , [123 ,61 ,59 ,3 ,151 ,103 ,167 ,58 ,224 ,191 ,96 ,188 ,151 ,211 ,120 ,49] , [96 ,178 ,145 ,222 ,155 ,114 ,235 ,74 ,4 ,58 ,250 ,201 ,54 ,171 ,54 ,226] , [66 ,180 ,68 ,33 ,56 ,24 ,199 ,56 ,198 ,159 ,247 ,82 ,137 ,16 ,69 ,123]]

    @catch_gracefully()
    def update(self, observable, actions):
        global kartVar, yukleme, eklenecekBakiye,ekran,strAlias,strTip,strVize,strE_Bakiye,strY_Bakiye
        global miktarResetle
        global yukletme

        (addedcards, removedcards) = actions
        
        print("GELEN : ",addedcards)
        print("GİDEN : ",removedcards)

        if(len(removedcards)>0):
            yukletme=True
            kartVar = False
            strAlias = ""
            strY_Bakiye = ""
            strE_Bakiye = ""
            strTip=""
            strVize=""
            miktarResetle=True
            if(ekran==2):
                ekran=0

        if(len(addedcards)>0):
            kartVar = True
            if(yukleme):
                card=addedcards[0]
                connection = card.createConnection()
                connection.connect()

                # This will log raw card traffic to console
                connection.addObserver(ConsoleCardConnectionObserver())

                # connection object itself is CardConnectionDecorator wrapper
                # and we need to address the underlying connection object
                desfire = DESFire(PCSCDevice(connection.component))
                key_setting=desfire.getKeySetting()
                info=desfire.getCardVersion()

                desfire.authenticate(0,key_setting)
                print(info)
                input("KART FORMATLANDI, BAŞKA?")
                
                crypto_key_3=desfire.createKeySetting(FMKwithU(info.UID,3),0,DESFireKeyType.DF_KEY_AES,[])
                crypto_key_4=desfire.createKeySetting(FMKwithU(info.UID,4),0,DESFireKeyType.DF_KEY_AES,[])

                # KRIPTO APP SEÇİLİYOR
                desfire.selectApplication('00 00 01')

                # crypto_key_4'den izin alınıyor, bu key okuma yapmaya yarar
                desfire.authenticate(4,crypto_key_4)
                read=desfire.readFileData(0,0,65)

                # okunan hex değerlerin arasındaki boşluklar temizlendi
                gelen = ""
                for eleman in (byte_array_to_human_readable_hex(read).lower()).split(" "):
                    gelen += eleman         
                # kendi verimiz çözüldü
                vize = gelen[128:]
                vize = "01"
                kart_veri = specialdecrypt(gelen[:-2])
                print(kart_veri)
                strAlias = kart_veri[0:7]
                kart_bakiye = kart_veri[7:13]
                bakiyem = int(kart_bakiye)/100
                strE_Bakiye = str(bakiyem)
                kart_tip = kart_veri[13:15]
                if(kart_tip=="01"):
                    strTip="STANDART"
                elif(kart_tip=="02"):
                    strTip="ÖĞRENCİ"
                elif(kart_tip=="03"):
                    strTip="PERSONEL"
                            
                son_vize_tarih = kart_veri[15:21]
                son_basis_tarih = kart_veri[21:31]
                strVize = son_vize_tarih[4:6]+"."+son_vize_tarih[2:4]+".20"+son_vize_tarih[0:2]

                bakiyem = bakiyem + eklenecekBakiye
                strY_Bakiye = str(bakiyem)  
                yeni_bakiye = sifirEkle(str(int(bakiyem*100)),6)
                
                paket = strAlias+yeni_bakiye+kart_tip+son_vize_tarih+son_basis_tarih
                
                print(paket)

                sifrelenmis = specialencrypt(paket)
                print(sifrelenmis)
                desfire.authenticate(3,crypto_key_3)
                desfire.writeFileData(0,0,65,sifrelenmis+vize)

                if(int(eklenecekBakiye)!=0):
                    print(strAlias,strTip,strE_Bakiye,strY_Bakiye,eklenecekBakiye)
                    sunucuyaBas(strAlias,strTip,1,"KOOPERATIF",1,strE_Bakiye,strY_Bakiye,eklenecekBakiye)
                
"""
class Pencere(QMainWindow):

    def __init__(self):
        global ekran
        super().__init__()

        self.ui = Ui_AnaPencere()
        self.ui.setupUi(self)

        # TIMERLAR
        self.zaman = QTimer() 
        self.zaman.timeout.connect(self.zamanCek)
        self.zaman.start(1)    

        global logger
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        ekran = 0
        """
        available_reader = readers()
        if not available_reader:
            self.ui.lblDurum.setText("KART OKUYUCUYU TAKIN")
            self.ekran=-1
            available_reader = readers()
        else:
            cardmonitor = CardMonitor()
            cardobserver = MyObserver()
            cardmonitor.addObserver(cardobserver)
        """
    def bakiyeYukle(self):
        global yukleme, eklenecekBakiye, ekran
        yukleme = True
        eklenecekBakiye = self.ui.doubleSpinBox.value()
        ekran = 1
        self.ekran=1

    def closeEvent(self, event):
        try:
            """
            cardmonitor.deleteObserver(cardobserver)
            """
            pass
        except:
            pass

    def zamanCek(self):
        global ekran,kartVar,strAlias,strTip,strVize,strE_Bakiye,strY_Bakiye,miktarResetle,eklenecekBakiye

        eklenecekBakiye = self.ui.doubleSpinBox.value()

        self.ui.lblAlias.setText(strAlias)
        self.ui.lblTip.setText(strTip)
        self.ui.lblVize.setText(strVize)
        self.ui.lblEskiBakiye.setText(strE_Bakiye)
        self.ui.lblGuncelBakiye.setText(strY_Bakiye)

        if(miktarResetle):
            self.ui.doubleSpinBox.setValue(0.0)
            eklenecekBakiye=0.0
            miktarResetle=False
    
        if(kartVar):
            self.ui.kartDurum.setStyleSheet("background:green;")
        else:
            self.ui.kartDurum.setStyleSheet("background:yellow;")

        self.ekran = ekran

        # EKRAN DEĞİŞKENİ
        if(self.ekran==0):
            self.ui.lblDurum.setText("YÜKLENECEK MİKTARI GİRİN")
        elif(self.ekran==1):
            self.ui.lblDurum.setText("KARTI YERLEŞTİRİN")
        elif(self.ekran==2):
            self.ui.lblDurum.setText("IŞLEM BAŞARILI")
            miktarResetle=True
            kartVar = False
            strAlias = ""
            strY_Bakiye = ""
            strE_Bakiye = ""
            strTip=""
            strVize=""
        elif(self.ekran==3):
            self.ui.lblDurum.setText("ZAMAN AŞIMI")
            kartVar = False
            strAlias = ""
            strY_Bakiye = ""
            strE_Bakiye = ""
            strTip=""
            strVize=""
            miktarResetle=True

        

if __name__ == '__main__':
    app = QApplication([])
    pencere = Pencere()
    pencere.show()
    app.exec_()