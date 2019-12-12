# -*- coding: utf-8 -*-
import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, session, url_for)

from forms import *
from queries import select
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

home = Blueprint(name='home', import_name=__name__,
                    template_folder='templates')

# TODO:: IMPLEMENT SMALL LOGO OF EACH ROUTE'S ELEMENTS


@home.route("/")
def home_page():
    event_data = [ 
        { 
            "id" : "1",
            "name":"13 Aralık Maali-Yi Sema   İstanbul Devlet Türk Müziği Araştırma Ve Uygulama Topluluğu",
            "url":"https://biletinial.com/muzik/maaliyi-sema-idtmaut",
            "location":"İrfa–İrfan Medeniyeti Araştırma Ve K.M.",
            "city":"Konya",
            "image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/maali-yi-sema-istanbul-devlet-turk-muzigi-arastirma-ve-uygulama-toplulugu-2019122155527.png",
            "date":"Aralık- 13",
            "type_":"Konser",
            "description":"   M. Fatih Çıtlak / Beste-İ Kadim Hüseynî Mevlevî Âyin-İ Şerîf-İ Anlatımlı Olarak İzleyiciler İle Buluşacak "
        },
        { 
            "id" : "2",
            "name":"12 Aralık Konseri - Bursa Bölge Devlet Senfoni Orkestrası",
            "url":"https://biletinial.com/muzik/12-aralik-konseri-bursa-bolge-devlet-senfoni-orkestrasi",
            "location":"Merinos AKKM Osmangazi Salonu",
            "city":"Bursa",
            "image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/12-aralik-konseri-bursa-bolge-devlet-senfoni-orkestrasi-2019125231546.jpg",
            "date":"Aralık- 12",
            "type_":"Konser",
            "description":"  7+ Adrian Prabava  Tatiana Samouil “Keman”  M.Glinka “Ruslan And Lyudmila Uvertürü A.Arensky  “Keman Konçertosu”Op.54 D.Şostakoviç “ Senfoni No.9 KASIM AYINDA İZLEYİCİ REKORU KIRAN BBDSO, MOLDOVALI KEMAN SANATÇISI TATIANA SAMOUIL İLE ARENSKY KEMAN KONÇERTOSUNU İLK KEZ BURSALI SANATSEVERLERLE BULUŞTURACAK! BBDSO, 12 Aralık 2019 akşamı gerçekleşecek konserinde, Mikhail GLINKA’nın “Ruslan&Ludmila” uvertürü, Anton ARENSKY’nin Keman konçertosu ve Dimitri ŞOSTAKOVİÇ’in 9 Senfonisi seslendirilecek. Dünyaca ünlü orkestra şefi Adrian Prabava’nın yöneteceği konserin solisti 2002 yılında yapılan ve “Klasik Müziğin Olimpiyatı” olarak nitelenen “Çaykovski” yarışmasında ödül alan Moldovalı Keman sanatçısı Tatiana Samouil. Endonezya’da dünyaya gelmiş olan dünyaca ünlü orkestra şefi Adrian Prabava, Detmold Müzik Yüksek Okulu’nda keman eğitimi görmüş ve ardından Hannover Müzik, Tiyatro ve Medya Yüksek Okulu’nda Eiji Oue’dan orkestra şefliği dersleri almıştır. Ayrıca Kurt Masur ve Bernard Haitink’in yanısıra aynı zamanda mentörü olan Jorma Panula’nın master derslerine katılmıştır. Sanatçı, halen dünyanın en ünlü orkestralarından davet alıp konserlerine devam etmektedir. Ünlü müzisyenler yetiştirmiş bir ailenin çocuğu olarak dünyaya gelen Tatiana Samouil, 3 yaşında piyano, 5 yaşında ise keman eğitimi almaya başladı. 9 yaşındayken babası şef Alexandru Samoila yönetimindeki Moldova Ulusal Orkestrası ile ilk kez sahneye çıktı ve bu konserden sonra kendini kemana adamaya karar verdi.. Zaman içinde sadece üç yıl içinde müzik camiasının en prestijli yarışmaları olarak kabul edilen yedi yarışmaya katıldı ve bunların tamamında ödül kazandı. Bu yarışmalar arasında Moskova Çaykovski UluslararasıYarışması (2002), Brüksel’de Kraliçe Elisabeth Yarışması (2001), Yeni Zelanda'da Michael Hill Uluslararası Yarışması (2001) ve Helsinki Uluslararası Jean Sibelius Keman Yarışması(2000) sayılabilir. Konserin ilk yarısında seslendirilecek olan Glinka’nın “Ruslan&Ludmila” operası uvertürü 5 perdeden oluşan operanın giriş müziğidir ve 9 Yüzyılda Rusya’da geçer. Eser, Rimsky-Korsakov, Borodin ve Mussorgsky’e esin kaynağı olmuştur. Konserin ikinci yarısında seslendirilecek olan Şostakoviç’in 9 Senfonisi ise devrim niteliğini taşıyan bir zafer kutlamasıdır. Bursa Bölge Devlet Senfoni Orkestrası Konseri, Bursa Büyükşehir Belediyesi, Bursa Filarmoni Derneği ve Uludağ Premium’un katkılarıyla 12 Aralık 2019 Perşembe  akşamı saat 20:00’de Atatürk Kongre ve Kültür Merkezi’nde gerçekleşecektir. "
        },
        { 
            "id" : "3",
            "name":"Bir Deste Beste  Şanlıurfa Devlet Türk Halk Müziği Korosu",
            "url":"https://biletinial.com/muzik/bir-deste-beste-sdthmk",
            "location":"ŞanlIurfa B.B. Şair Nabi Kültür Merkezi",
            "city":"Şanlıurfa",
            "image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/bir-deste-beste-sanliurfa-devlet-turk-halk-muzigi-korosu-201912415282.jpg",
            "date":"Aralık- 20",
            "type_":"Konser",
            "description":"  M. Bakır Karadağlı"
        },
        { 
            "id" : "4",
            "name":"13  Aralık Konseri   İstanbul Devlet Senfoni Orkestrası",
            "url":"https://biletinial.com/muzik/13-aralik-idso",
            "location":"Grand Pera  Emek Sahnesi",
            "city":"İstanbul",
            "image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/13-aralik-konseri-istanbul-devlet-senfoni-orkestrasi-2019129122243.jpg",
            "date":"Aralık- 13",
            "type_":"Klasik,Senfoni,Konser",
            "description":"  Şef :Ender Sakpınar Solist: Emılıo Aversano (Piano)"
        }
    ]
    
    return render_template("home_page.html", events=event_data)