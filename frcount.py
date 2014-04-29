#coding: utf8 
import webapp2

from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from datetime import datetime

page_html = '''
<!DOCTYPE html>
<html>
<head>
  <link type="text/css" rel="stylesheet" href="/static/main.css" />

  <title>Count of Classified Items on ebay.fr</title>
</head>

<body>
  <a href="http://www.ebay.fr" class="main-title">
    ebay.fr
  </a>

  <div id="content">

  <h2>Classifieds Count</h2>

    <table border="1" bordercolor="#000066" style="background-color:#FFFFFF" cellpadding="3" cellspacing="0">
	<tr>
		<td>Category</td>
		<td>URL</td>
		<td>Count</td>
	</tr>
	%(rows)s
    </table>

  </div>
</body>

</html>
'''
table_row = '''
<tr>
    <td>%(category)s</td>
    <td><a href='%(url)s'>%(url)s</a></td>
    <td align='right'>%(count)s</td>
</tr>
	
'''

fr_cats = [
   [173030,"www.ebay.fr/sch/173030/i.html?LH_CAds=1"," Animaux"],
   [353,"www.ebay.fr/sch/353/i.html?LH_CAds=1","Art, antiquités"],
   [9800,"www.ebay.fr/sch/9800/i.html?LH_CAds=1","Auto, moto"],
   [135232,"www.ebay.fr/sch/135232/i.html?LH_CAds=1","Auto: pièces, accessoires"],
   [1293,"www.ebay.fr/sch/1293/i.html?LH_CAds=1","Bateaux, voile, nautisme"],
   [35112,"www.ebay.fr/sch/35112/i.html?LH_CAds=1","Beauté, bien-être, parfums"],
   [2984,"www.ebay.fr/sch/2984/i.html?LH_CAds=1","Bébé, puériculture"],
   [281,"www.ebay.fr/sch/281/i.html?LH_CAds=1","Bijoux, montres"],
   [7487,"www.ebay.fr/sch/7487/i.html?LH_CAds=1","Céramiques, verres"],
   [1,"www.ebay.fr/sch/1/i.html?LH_CAds=1","Collections"],
   [11232,"www.ebay.fr/sch/11232/i.html?LH_CAds=1","DVD, cinéma"],
   [293,"www.ebay.fr/sch/293/i.html?LH_CAds=1","Image, son"],
   [147425,"www.ebay.fr/sch/147425/i.html?LH_CAds=1","Immobilier"],
   [58058,"www.ebay.fr/sch/58058/i.html?LH_CAds=1","Informatique, Réseaux"],
   [14982,"www.ebay.fr/sch/14982/i.html?LH_CAds=1","Instruments de musique"],
   [220,"www.ebay.fr/sch/220/i.html?LH_CAds=1","Jeux, jouets, figurines"],
   [1249,"www.ebay.fr/sch/1249/i.html?LH_CAds=1","Jeux vidéo, consoles"],
   [267,"www.ebay.fr/sch/267/i.html?LH_CAds=1","Livres, BD, revues"],
   [14339,"www.ebay.fr/sch/14339/i.html?LH_CAds=1","Loisirs créatifs"],
   [11700,"www.ebay.fr/sch/11700/i.html?LH_CAds=1","Maison, jardin, bricolage"],
   [11116,"www.ebay.fr/sch/11116/i.html?LH_CAds=1","Monnaies"],
   [14780,"www.ebay.fr/sch/14780/i.html?LH_CAds=1","Moto: pièces, accessoires"],
   [11233,"www.ebay.fr/sch/11233/i.html?LH_CAds=1","Musique, CD, vinyles"],
   [32653,"www.ebay.fr/sch/32653/i.html?LH_CAds=1","Photo, caméscopes"],
   [12576,"www.ebay.fr/sch/12576/i.html?LH_CAds=1","PME, artisans, agriculteurs"],
   [888,"www.ebay.fr/sch/888/i.html?LH_CAds=1","Sports, vacances"],
   [14675,"www.ebay.fr/sch/14675/i.html?LH_CAds=1","Téléphonie, mobilité"],
   [260,"www.ebay.fr/sch/260/i.html?LH_CAds=1","Timbres"],
   [11450,"www.ebay.fr/sch/11450/i.html?LH_CAds=1","Vêtements, accessoires"],
   [62682,"www.ebay.fr/sch/62682/i.html?LH_CAds=1","Vins, Gastronomie"]]

class FRCategory(db.Model):
    ''' Models an individual Category country entry'''
    cat_id = db.IntegerProperty(required = True)
    name = db.StringProperty(required = True)
    url = db.StringProperty(required = True)
    count = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)



class FRCountHandler(webapp2.RequestHandler):
    def get(self):
        rows = ""
        total = 0
        for val in fr_cats:
            cat_id = val[0]
            url = "http://" + val[1]
            category = val[2]

            cat_row = memcache.get(str(cat_id))
            count = 0
            time_now = datetime.now()
            last_mod = datetime.now()

            # bug fix for NoneType error
            if cat_row:
                last_mod = cat_row.last_modified

            if cat_row and ((time_now - last_mod).seconds/60 < 5):
                count = cat_row.count
                total = total + count
            else:
                page = urlfetch.fetch(url,deadline=120).content
                str_to_find = "<span class='countClass autClass-resCount'>"
                start_index = page.find(str_to_find)

                count = '0'
                if start_index > 0:
                    end_index = page.find("</span>", start_index)
                    count = page[start_index + len(str_to_find):end_index]
                    c = ''.join(count.split())
                    c = c.replace("\xc2\xa0", "")
                    count = int(c)
                    total = total + count

                        
                    cat_row = FRCategory(cat_id = cat_id, name = category, url = url, count = int(c))

                    memcache.set(str(cat_id), cat_row)
                
            rows = rows + table_row % {'category':category, 'url':url, 'count':count}            
            
        rows = rows + table_row % {'category':"<b>Total</b>", 'url':"", 'count':"<b>" + str(total) + "</b>"}        
        self.response.out.write(page_html % {"rows": rows})





