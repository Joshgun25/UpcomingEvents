# -*- coding: utf-8 -*-
import math
import os
import time
from datetime import datetime

import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
				   request, send_from_directory, session, url_for)
from werkzeug.utils import secure_filename

from forms import (EditCompetitionForm, EditMemberForm, EditTeamForm, SQLForm,
				   UploadCVForm, UploadImageForm)
from member_profile import Member
from queries import run, select, update

admin = Blueprint(name='admin', import_name=__name__)


@admin.route("/admin/")
@admin.route("/admin")
def admin_page():
	if (session.get('member_id') == 'admin'):
		return render_template('admin_page.html')
	else:
		return redirect(url_for('home.home_page'))


@admin.route("/admin/sql/", methods=['GET', 'POST'])
@admin.route("/admin/sql", methods=['GET', 'POST'])
def sql_page():
	form = SQLForm()
	if form.validate_on_submit():
		query = form.query.data
		result = run(query)
		return render_template('sql_page.html', form=form, queryResult=result, resultLen=len(result))
	return render_template('sql_page.html', form=form, queryResult=None, resultLen=0)


@admin.route("/admin/events/edit/<id>", methods=['GET', 'POST'])
def admin_edit_event_page(id):
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
		},
		{   
			"id" : "5",
			"name":"13 Aralık Konseri   CSO",
			"url":"https://biletinial.com/muzik/13-aralik19-cso",
			"location":"Cumhurbaşkanlığı Senfoni Orkestrası Salonu",
			"city":"Ankara",
			"image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/13-aralik-konseri-cso-20191126165219.jpg",
			"date":"Aralık- 13",
			"type_":"Senfoni",
			"description":"   : Antonio Pirolli  : Perihan Artan Nayır, soprano Asude Karayavuz, mezzo-soprano Emre Akkuş, tenor Şafak Güç, bas Ankara Devlet Opera ve Balesi Korosu Koro Şefi: Giampaolo Vessella  Giuseppe Verdi ………………………………”Requiem”"
		},
		{   
			"id" : "6",
			"name":"Requiem - ÇDSO",
			"url":"https://biletinial.com/muzik/requiem-cdso",
			"location":"Adana B.Belediyesi Konser Salonu",
			"city":"Adana",
			"image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/requiem-cdso-20191161155.jpg",
			"date":"Aralık- 13",
			"type_":"Sinema",
			"description":"  10+ ”Requıem” Şef: Rengim Gökmen Solistler: Can Çakmur “Piyano” Nurdan Küçükekmekçi “Soprano” Arda Aktar “Tenor” Koro: Ankara Devlet Çoksesli Korosu Koro şefi : Burak Onur Erdem Program: F. Mendelssohn / Piyano Konçertosu No.2 G. Fauré / Requıem (Adana'da ilk Seslendiriliş) "
		},
		{ 
			"id" : "7",
			"name":"Çeşm-i Ahu  Diyarbakır Devlet Klasik Türk Müziği Korosu",
			"url":"https://biletinial.com/muzik/cesmi-ahu-ddktmk",
			"location":"Cahit Sıtkı Tarancı KSM KoroSalonu",
			"city":"Diyarbakır",
			"image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/cesm-i-ahu-diyarbakir-devlet-klasik-turk-muzigi-korosu-20191122103917.jpg",
			"date":"Aralık- 12",
			"type_":"Tiyatro",
			"description":"  M.Tanju Demirkol Çeşm-İ Ahu ( Periyodik Konseri)  Hicaz Eserler Hisarbuselik  Nurdan Ünal, Deniz Değirmenci, Ebru Özbay, Bedriye İleri "
		},
		{ 
			"id" : "8",
			"name":"19 Aralık Konseri  CSO",
			"url":"https://biletinial.com/muzik/19-aralik19-cso",
			"location":"Cumhurbaşkanlığı Senfoni Orkestrası Salonu",
			"city":"Ankara",
			"image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/19-aralik-konseri-cso-20191126165743.jpg",
			"date":"Aralık- 19",
			"type_":"Senfoni",
			"description":"  : Rengim Gökmen  Ayşegül Sarıca, piyano  Wolfgang Amadeus Mozart ………“Figaro’nun Düğünü” Operası Uvertürü, Kv.492 Wolfgang Amadeus Mozart ……… Piyano Konçertosu Nr. 20, re minör, Kv.466 Wolfgang Amadeus Mozart ……… 41.Senfoni, do majör, Kv.551"
		},
		{ 
			"id" : "9",
			"name":"19 Aralık Konseri Bursa Bölge Devlet Senfoni Orkestrası",
			"url":"https://biletinial.com/muzik/19-aralik-konseri-bbdso",
			"location":"Merinos AKKM Osmangazi Salonu",
			"city":"Bursa",
			"image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/19-aralik-konseri-bursa-bolge-devlet-senfoni-orkestrasi-2019125132455.jpg",
			"date":"Aralık- 19",
			"type_":"Konser",
			"description":"  Ayyub Guliyev Alihan Samedov “Balaban” P.Bülbüloğlu “Aşk Ve Ölüm Balesinden Seçmeler” “Balaban Konçertosu” “Senfoni No.9”"
		},
		{ 
			"id" : "10",
			"name":"11 Aralık Konseri İstanbul Devlet Türk Müziği Araştırma ve Uygulama Topluluğu",
			"url":"https://biletinial.com/muzik/11-aralik-ist-ar-uyg-toplulugu",
			"location":"Altunizade Kültür ve Sanat Merkezi",
			"city":"İstanbul",
			"image":"https://d2yj4fhf636aio.cloudfront.net/Uploads/Films/11-aralik-konseri-istanbul-arastirma-ve-uygulama-toplulugu-20191125162215.png",
			"date":"Aralık- 11",
			"type_":"Türk Müziği",
			"description":"  1.Bölüm: Hicâzbûselik Makâmında Klâsik Takım 2.Bölüm: Mâhur Makâmında Fasıl Konuk Şef Önay Akın yönetmenliğinde, Hicâzbûselik Makâmının büyük formda bestelenmiş eserlerinden oluşan Klâsik Takım ve Mâhur Makâmının seçilmiş eserlerinden oluşan bir Fasıl icrâ edilecektir."
		}
	]


	form = EditCompetitionForm()
	imageForm = UploadImageForm()
	imageFolderPath = os.path.join(os.getcwd(), 'static/images/competitions')

	if (request.method == 'POST' and form.submit_competition.data or form.validate()):
		print("Not")
		name = form.name.data.encode('utf-8')
		date = form.date.data
		country = form.country.data.encode('utf-8')
		description = form.description.data.encode('utf-8')
		reward = form.reward.data.encode('utf-8')
		image = imageForm.image.data
		if(image and '.jpg' in image.filename or '.jpeg' in image.filename):
			current_date = time.gmtime()
			filename = secure_filename(
				"{}_{}.jpg".format(id, current_date[0:6]))
			filePath = os.path.join(imageFolderPath, filename)
			images = os.listdir(imageFolderPath)
			digits = int(math.log(int(id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(id)):
					os.remove(os.path.join(imageFolderPath, im))
			image.save(filePath)
		elif(image):
			flash('Please upload a file in JPG format', "danger")
		print("Before update: ", date)
		update("competition", "name='{}', date=DATE('{}'), country='{}', description='{}', reward='{}'".format(
			name, date, country, description, reward), "id={}".format(id))
		return redirect(url_for('admin.admin_edit_event_page', id=id))
	else:
		if(session.get('member_id') != 'admin'):
			flash('No admin privileges...', 'danger')
			return redirect(url_for('home.home_page'))

		for event in event_data:
			if(event['id'] == id):
				result = event

		img_name = None
		for img in os.listdir(imageFolderPath):
			if(id in img[0:len(id)] and (img[len(id)] == '_' or img[len(id)] == '.')):
				img_name = img
		form.description.data = result['description']
		return render_template('admin_edit_event_page.html', form=form, result=result, imgName=img_name, uploadImg=imageForm)
	return render_template('admin_edit_event_page.html', form=form, result=result, imgName=img_name, uploadImg=imageForm)


@admin.route("/admin/teams/edit/<id>", methods=['GET', 'POST'])
def admin_edit_team_page(id):
	form = EditTeamForm()
	imageForm = UploadImageForm()
	imageFolderPath = os.path.join(os.getcwd(), 'static/images/team')
	if (request.method == 'POST' and form.submit_team.data or form.validate()):
		name = form.name.data.encode('utf-8')
		members = form.memberCtr.data
		year = form.year.data
		print("Year", year)
		email = form.email.data.encode('utf-8')
		address = form.address.data.encode('utf-8')
		competition = form.competition.data
		image = imageForm.image.data
		if(image and '.jpg' in image.filename or '.jpeg' in image.filename):
			date = time.gmtime()
			filename = secure_filename("{}_{}.jpg".format(id, date[0:6]))
			filePath = os.path.join(imageFolderPath, filename)
			images = os.listdir(imageFolderPath)
			digits = int(math.log(int(id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(id)):
					os.remove(os.path.join(imageFolderPath, im))
			image.save(filePath)
		elif(image):
			flash("Please upload a file in JPG format", 'danger')
		update("team", "name='{}', num_members={}, found_year='{}', email='{}', adress='{}', competition_id={}, logo='{}'".format(
			name, members, year, email, address, competition, id), where="id={}".format(id))
		return redirect(url_for('admin.admin_edit_team_page', id=id))
	else:
		if(session.get('member_id') != 'admin'):
			flash('No admin privileges...', 'danger')
			return redirect(url_for('home.home_page'))
		result = select(columns="team.name,team.num_members,team.found_year,team.email,team.adress,competition.name",
						table="team join competition on team.COMPETITION_ID=competition.id",
						where="team.id={}".format(id))
		img_name = None
		for img in os.listdir(imageFolderPath):
			if(id in img[0:len(id)] and (img[len(id)] == '_' or img[len(id)] == '.')):
				img_name = img
		return render_template('admin_edit_team_page.html', form=form, result=result, uploadImg=imageForm, imgName=img_name)
	return render_template('admin_edit_team_page.html', form=form, result=result, uploadImg=imageForm, imgName=img_name)


@admin.route("/admin/members/")
@admin.route("/admin/members")
def admin_members_page():
	if(session.get('member_id') != 'admin'):
		flash('No admin privileges...', 'danger')
		return redirect(url_for('home.home_page'))
	else:
		result = select(columns="person.name,person.email,auth_type.name,team.name,person.id",
						table="person join team on person.team_id=team.id \
							join auth_type on person.auth_type=auth_type.id \
							order by team.name asc, auth_type.name desc")
		return render_template('admin_members_page.html', members=result)


@admin.route("/admin/members/edit/<person_id>", methods=['GET', 'POST'])
def admin_edit_member_page(person_id):
	# TODO:: Alter table to include social accounts links in person database.
	form = EditMemberForm()
	cvForm = UploadCVForm()
	cvFolderPath = os.path.join(os.getcwd(), 'static/cv')
	imageForm = UploadImageForm()
	imageFolderPath = os.path.join(os.getcwd(), 'static/images/person')
	cvPath = None
	if form.validate_on_submit():
		team = form.team.data
		subteam = form.subteam.data
		role = form.role.data.encode('utf-8')
		auth_type = form.auth_type.data
		email = form.email.data.encode('utf-8')
		name = form.name.data.encode('utf-8')
		address = form.address.data.encode('utf-8')
		active = form.active.data
		age = form.age.data
		phone = form.phone.data
		clas = form.clas.data
		major = form.major.data
		cv = cvForm.cv.data

		if(cv and '.pdf' in cv.filename):
			date = time.gmtime()
			filename = secure_filename(
				"{}_{}.pdf".format(person_id, date[0:6]))
			filePath = os.path.join(cvFolderPath, filename)
			cvs = os.listdir(cvFolderPath)
			digits = int(math.log(int(person_id), 10))+1
			for c in cvs:
				if(c[digits] == '_' and c[0:digits] == str(person_id)):
					os.remove(os.path.join(cvFolderPath, c))
			cv.save(filePath)
		elif(cv):
			flash("Please insert a pdf file.", 'danger')
		print(cv)
		image = imageForm.image.data
		if(image and '.jpg' in image.filename or '.jpeg' in image.filename):
			date = time.gmtime()
			filename = secure_filename(
				"{}_{}.jpg".format(person_id, date[0:6]))
			filePath = os.path.join(imageFolderPath, filename)
			images = os.listdir(imageFolderPath)
			digits = int(math.log(int(person_id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(person_id)):
					os.remove(os.path.join(imageFolderPath, im))
			image.save(filePath)
		elif(image):
			flash("Please upload a file in JPG format", 'danger')

		teamID = select(columns="id", table="team",
						where="name='{}'".format(team))
		subteamID = select(columns="id", table="subteam",
						   where="name='{}'".format(subteam))
		majorID = select(columns="id", table="major",
						 where="code='{}'".format(major))
		memberID = select(columns="member.id",
						  table="member join person on member.person_id=person.id",
						  where="person.id={}".format(person_id))

		teamID, subteamID, majorID, memberID = teamID[0], subteamID[0], majorID[0], memberID[0]

		update("member", "role='{}', active={}, address='{}'".format(
			role, active, address), where="id={}".format(memberID))

		update("person", "name='{}', age='{}', phone='{}', cv={}, email='{}', \
					class={}, auth_type={}, team_id={}, subteam_id={}, major_id={}".format(
			name, age, phone, person_id, email, clas, auth_type, teamID, subteamID, majorID), where="id={}".format(person_id))

		return redirect(url_for('admin.admin_edit_member_page', person_id=person_id, cvPath=person_id))
	else:
		if(session.get('member_id') != 'admin'):
			flash('No admin privileges...', 'danger')
			return redirect(url_for('home.home_page'))
		else:
			columns = """person.name,person.email,team.name,subteam.name,\
					member.role,member.active,member.entrydate,auth_type.name, \
					member.address,person.phone,major.name,person.class,person.age,member.id,person.cv"""

			table = """member join person on member.person_id=person.id \
					join major on person.major_id=major.id \
					join team on person.team_id=team.id \
					join subteam on person.subteam_id=subteam.id \
					join auth_type on person.auth_type=auth_type.id"""

			where = "person.id={}".format(person_id)
			result = select(columns, table, where)
			cvPath = None
			for c in os.listdir(cvFolderPath):
				if(person_id in c[0:len(person_id)] and (c[len(person_id)] == '_' or c[len(person_id)] == '.')):
					cvPath = c

			img_name = None
			for img in os.listdir(imageFolderPath):
				if(person_id in img[0:len(person_id)] and (img[len(person_id)] == '_' or img[len(person_id)] == '.')):
					img_name = img
			return render_template('admin_edit_member_page.html', form=form, uploadImg=imageForm, uploadCV=cvForm, result=result, cvPath=cvPath, imgName=img_name)

	return render_template('admin_edit_member_page.html', form=form, uploadImg=imageForm, uploadCV=cvForm, cvPath=cvPath, imgName=img_name)


@admin.route("/download/<filename>", methods=['GET', 'POST'])
def download(filename):
	cvFolder = os.path.join(admin.root_path, "static/cv")
	return send_from_directory(directory=cvFolder, filename=filename, as_attachment=True, cache_timeout=0)


@admin.route("/admin/profile", methods=['GET', 'POST'])
def admin_profile_page():
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		result = None
		return render_template('admin_profile_page.html', result=result)


@admin.route("/admin/review/events", methods=['GET', 'POST'])
def admin_review_events_page():
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		result = None
		return render_template('admin_review_events_page.html', result=result)


@admin.route("/admin/review/organizers", methods=['GET', 'POST'])
def admin_review_organizers_page():
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		result = None
		return render_template('admin_review_organizers_page.html', result=result)