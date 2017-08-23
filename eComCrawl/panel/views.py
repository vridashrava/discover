# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from crawlers.views import viewform, tasksOutput,viewdata,clearSessionData
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
import json,logging,os,urllib
from datetime import datetime,timedelta
from crawlers.db import DB
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from django.views import View

# Create your views here.
class Dashboard(TemplateView):
  template_name = 'dashboard/dashboard.html'

  def get(self, request, *args, **kwargs):
    return self.render_to_response({
      "page": "dashboard"
    })

class AddWebsite(TemplateView):
  template_name = 'dashboard/websites/add_website.html'
  subpage = "1"
  secondary_page = "add_website"
  data = ""
  def get(self, request, *args, **kwargs):
    categories_data = {}
    default_data = None
    if self.subpage == "1":
      if "page_1_data" in request.session:
        default_data = request.session["page_1_data"]


    if self.subpage == "2":
      # print(request.session["page_1_data"])
      self.template_name = 'dashboard/websites/add_website_page_2.html'

      # categories_data = {'ajio': {'MEN-SALE': ['https://www.ajio.com/c/men', 'https://www.ajio.com/', 'https://www.ajio.com/', 'https://www.ajio.com/s/mens-flat-50-80-off', 'https://www.ajio.com/s/jack-jones-western-wear', 'https://www.ajio.com/s/nike-men-brand', 'https://www.ajio.com/s/men-vans-footwear', 'https://www.ajio.com/s/jack-jones-western-wear', 'https://www.ajio.com/s/nike-men-brand', 'https://www.ajio.com/capsule/newin/men', 'https://www.ajio.com/s/men-newin-clothing', 'https://www.ajio.com/s/fresh-arrivals-accessories-and-footwear', 'https://www.ajio.com/s/international-brands-men', 'https://www.ajio.com/c/830216', 'https://www.ajio.com/c/830216010', 'https://www.ajio.com/c/830216001', 'https://www.ajio.com/c/830216013', 'https://www.ajio.com/c/830216002', 'https://www.ajio.com/c/830216015', 'https://www.ajio.com/c/830216011', 'https://www.ajio.com/c/830216003', 'https://www.ajio.com/c/830216004', 'https://www.ajio.com/c/830216014', 'https://www.ajio.com/c/830207', 'https://www.ajio.com/c/830207006', 'https://www.ajio.com/c/830207001', 'https://www.ajio.com/c/830207007', 'https://www.ajio.com/c/830207010', 'https://www.ajio.com/c/830207008?q=%3Arelevance', 'https://www.ajio.com/s/men-accessories-brands', 'https://www.ajio.com/c/830201001', 'https://www.ajio.com/c/830201', 'https://www.ajio.com/c/830201007', 'https://www.ajio.com/c/830202001', 'https://www.ajio.com/c/830205', 'https://www.ajio.com/c/830202002', 'https://www.ajio.com/c/830204003', 'https://www.ajio.com/c/men-capsule-collection', 'https://www.ajio.com/c/830212', 'https://www.ajio.com/c/830211', 'https://www.ajio.com/c/830211002', 'https://www.ajio.com/s/men-trunks-boxers', 'https://www.ajio.com/c/830211006', 'https://www.ajio.com/', 'https://www.ajio.com/s/eoss-men-impulse-steal-bags', 'https://www.ajio.com/s/mens-footwear-under-1499', 'https://www.ajio.com/s/jeans-under-1199', 'https://www.ajio.com/s/shorts-three-fourths-under-699', 'https://www.ajio.com/s/tees-clearance-sale', 'https://www.ajio.com/', 'https://www.ajio.com/', 'https://www.ajio.com/s/backpacks-and-utility-bags', 'https://www.ajio.com/c/men-brogues', 'https://www.ajio.com/s/cargos-chinos', 'https://www.ajio.com/s/men-shoe', 'https://www.ajio.com/c/men-denim-shirts-collection', 'https://www.ajio.com/c/graphic-shirts', 'https://www.ajio.com/c/830216003', 'https://www.ajio.com/c/Doubt-Is-Out', 'https://www.ajio.com/s/men-ajio-own-brand', 'https://www.ajio.com/s/international-brands-men', 'https://www.ajio.com/b/alcott', 'https://www.ajio.com/b/kaporal', 'https://www.ajio.com/b/native-youth', 'https://www.ajio.com/s/men-point-zero', 'https://www.ajio.com/b/tom-tailor', 'https://www.ajio.com/s/men-exclusive-brands', 'https://www.ajio.com/b/acuto', 'https://www.ajio.com/b/antiferro', 'https://www.ajio.com/s/men-dnmx-brand', 'https://www.ajio.com/b/funk', 'https://www.ajio.com/b/garcon', 'https://www.ajio.com/s/hats-off-accessories', 'https://www.ajio.com/b/netplay', 'https://www.ajio.com/b/piaffe', 'https://www.ajio.com/s/men-teamspirit-brand', 'https://www.ajio.com/c/830216', 'https://www.ajio.com/b/celio', 'https://www.ajio.com/s/duke-men', 'https://www.ajio.com/b/flying-machine', 'https://www.ajio.com/b/gas', 'https://www.ajio.com/b/indian-terrain', 'https://www.ajio.com/s/jack-jones-western-wear', 'https://www.ajio.com/b/john-players', 'https://www.ajio.com/s/men-killer-western-wear', 'https://www.ajio.com/s/men-lee', 'https://www.ajio.com/s/men-levis-western-wear', 'https://www.ajio.com/s/men-mark-spencer', 'https://www.ajio.com/s/pepe-jeans-men', 'https://www.ajio.com/b/spykar', 'https://www.ajio.com/s/united-colours-benetton', 'https://www.ajio.com/b/us-polo', 'https://www.ajio.com/s/men-wills-lifestyle', 'https://www.ajio.com/s/men-wrangler-western-wear', 'https://www.ajio.com/c/830211', 'https://www.ajio.com/s/hanes-innerwear-men', 'https://www.ajio.com/s/men-levis-innerwear', 'https://www.ajio.com/s/playboy-men', 'https://www.ajio.com/s/undercolors-of-benetton-innerwear', 'https://www.ajio.com/s/us-polo-innerwear', 'https://www.ajio.com/s/men-accessories-brands', 'https://www.ajio.com/s/men-eristonaman-accessories', 'https://www.ajio.com/s/flying-machine', 'https://www.ajio.com/b/mtv', 'https://www.ajio.com/s/puma-men-accessories', 'https://www.ajio.com/b/skybags', 'https://www.ajio.com/s/men-teakwood-leathers-accessories', 'https://www.ajio.com/s/tommy-hilfiger', 'https://www.ajio.com/s/men-us-polo-brand', 'https://www.ajio.com/s/men-wildcraft-accessories', 'https://www.ajio.com/s/men-wrangler-accessories', 'https://www.ajio.com/c/830207', 'https://www.ajio.com/s/men-carlton-london-footwear', 'https://www.ajio.com/s/crocs', 'https://www.ajio.com/s/famozi-footwear', 'https://www.ajio.com/b/knotty-derby', 'https://www.ajio.com/b/lee-cooper', 'https://www.ajio.com/b/modello-domani', 'https://www.ajio.com/b/muddman', 'https://www.ajio.com/s/men-puma-footwear-brand', 'https://www.ajio.com/b/red-tape', 'https://www.ajio.com/s/men-skechers-collection', 'https://www.ajio.com/b/sole-threads', 'https://www.ajio.com/s/men-ucb-footwear', 'https://www.ajio.com/s/men-vans-footwear', 'https://www.ajio.com/help/BrandListing']}}

    if self.subpage == "3":
      # print(request.session["page_2_data"])

      self.template_name = 'dashboard/websites/add_website_page_3.html'
      # default_data = request.session["page_3_data"]
      if "page_3_data" in request.session:
        default_data = request.session["page_3_data"]

    if self.subpage == "4":
      self.template_name = 'dashboard/websites/add_website_page_4.html'
      self.data = [{'product_name': ['Khaki Solid Slim Fit Chinos'], 'description': ['\n'], 'url': 'http://www.jabong.com/blackberrys-Khaki-Solid-Slim-Fit-Chinos-300077005.html?pos=1&cid=BL114MA03YFRINDFAS', 'product_brand': ['Blackberrys'], 'product_title': ['Blackberrys '], 'images': ['http://static2.jassets.com/p/Blackberrys-Khaki-Solid-Slim-Fit-Chinos-8761-500770003-1-pdp_slider_m.jpg', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['2195'], 'price': ['1756'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fit</span><span>Slim</span></li><li><span class="product-info-left">Color</span><span>Khaki</span></li><li><span class="product-info-left">Wash Care</span><span>Machine Wash, Do Not Bleach, Do Not Tumble Dry, Cool Iron, Dry Clean</span></li><li><span class="product-info-left">Style</span><span>Solid</span></li><li><span class="product-info-left">SKU</span><span>BL114MA03YFRINDFAS</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>Blackberrys authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['1756'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/trousers/"><span itemprop="name">Trousers</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/trousers/casual-trousers/"><span itemprop="name">Casual Trousers</span></a></li></ol>\'', 'discount': ['(-20%)'], 'id': '5949635e52ab721620f392ff'},
                 {'product_name': ['Black Solid Slim Fit Formal Trouser'], 'description': ['\n'], 'url': 'http://www.jabong.com/John_Player-Black-Solid-Slim-Fit-Formal-Trouser-300076981.html?pos=2&cid=JO423MA95BKVINDFAS', 'product_brand': ['John Players'], 'product_title': ['John Players '], 'images': ['http://static2.jassets.com/p/John-Players-Black-Solid-Slim-Fit-Formal-Trouser-2961-189670003-1-pdp_slider_m.webp', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['1999'], 'price': ['1000'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fabric</span><span>Blended</span></li><li><span class="product-info-left">Fit</span><span>Slim</span></li><li><span class="product-info-left">Color</span><span>Black</span></li><li><span class="product-info-left">Wash Care</span><span>Machine Wash, Do Not Bleach, Do Not Tumble Dry, Cool Iron, Dry Clean</span></li><li><span class="product-info-left">Style</span><span>Solid</span></li><li><span class="product-info-left">SKU</span><span>JO423MA95BKVINDFAS</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>John Players authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['1000'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/trousers/"><span itemprop="name">Trousers</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/trousers/formal-trousers/"><span itemprop="name">Formal Trousers</span></a></li></ol>\'', 'discount': ['(-50%)'], 'id': '5949638252ab721620f39300'},
                 {'product_name': ['Orange Checked Regular Fit Casual Shirt'], 'description': [], 'url': 'http://www.jabong.com/Tommy_Hilfiger-Orange-Checked-Regular-Fit-Casual-Shirt-300074043.html?pos=3&cid=TO348MA16JACINDFAS', 'product_brand': ['Tommy Hilfiger'], 'product_title': ['Tommy Hilfiger '], 'images': ['http://static2.jassets.com/p/Tommy-Hilfiger-Orange-Checked-Regular-Fit-Casual-Shirt-1959-340470003-1-pdp_slider_m.webp', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['4299'], 'price': ['3226'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fit</span><span>Regular</span></li><li><span class="product-info-left">Color</span><span>Orange</span></li><li><span class="product-info-left">Sleeves</span><span>Full Sleeves</span></li><li><span class="product-info-left">Wash Care</span><span>Machine Wash, Do Not Bleach, Do Not Tumble Dry, Cool Iron, Dry Clean</span></li><li><span class="product-info-left">Fabric</span><span>Cotton</span></li><li><span class="product-info-left">Style</span><span>Checked</span></li><li><span class="product-info-left">SKU</span><span>TO348MA16JACINDFAS</span></li><li><span class="product-info-left">Model Stats</span><span>Model is wearing size M and his height is 6\\\'0", chest 37" and waist 32".</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>Tommy Hilfiger authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['3226'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shirts/"><span itemprop="name">Shirts</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shirts/casual-shirts/"><span itemprop="name">Casual Shirts</span></a></li></ol>\'', 'discount': ['(-25%)'], 'id': '594963a452ab721620f39301'},
                 {'product_name': ['Pink Solid Slim Fit Casual Shirt'], 'description': ['\n'], 'url': 'http://www.jabong.com/John_Player-Pink-Solid-Slim-Fit-Casual-Shirt-300082745.html?pos=4&cid=JO423MA16QDSINDFAS', 'product_brand': ['John Players'], 'product_title': ['John Players '], 'images': ['http://static2.jassets.com/p/John-Players-Pink-Solid-Slim-Fit-Casual-Shirt-9288-547280003-1-pdp_slider_m.webp', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['1799'], 'price': ['900'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fit</span><span>Slim</span></li><li><span class="product-info-left">Color</span><span>Pink</span></li><li><span class="product-info-left">Sleeves</span><span>Full Sleeves</span></li><li><span class="product-info-left">Wash Care</span><span>Machine Wash, Do Not Bleach, Do Not Tumble Dry, Cool Iron, Dry Clean</span></li><li><span class="product-info-left">Fabric</span><span>Cotton</span></li><li><span class="product-info-left">Style</span><span>Solid</span></li><li><span class="product-info-left">SKU</span><span>JO423MA16QDSINDFAS</span></li><li><span class="product-info-left">Model Stats</span><span>Model is wearing size 40 and his height is 6\\\'1", chest 36" and waist 32".</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>John Players authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['900'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shirts/"><span itemprop="name">Shirts</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shirts/casual-shirts/"><span itemprop="name">Casual Shirts</span></a></li></ol>\'', 'discount': ['(-50%)'], 'id': '594963b852ab721620f39302'},
                 {'product_name': ['Club Black Training Shorts'], 'description': [], 'url': 'http://www.jabong.com/Adidas-Club-Black-Training-Shorts-300074465.html?pos=5&cid=AD004MA47YDRINDFAS', 'product_brand': ['Adidas'], 'product_title': ['Adidas '], 'images': ['http://static2.jassets.com/p/Adidas-Club-Black-Training-Shorts-7710-564470003-1-pdp_slider_m.webp', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['1899'], 'price': ['1299'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fabric</span><span>Polyester</span></li><li><span class="product-info-left">Fit</span><span>Regular</span></li><li><span class="product-info-left">Color</span><span>Black</span></li><li><span class="product-info-left">Style</span><span>Solid</span></li><li><span class="product-info-left">SKU</span><span>AD004MA47YDRINDFAS</span></li><li><span class="product-info-left">Model Stats</span><span>Model is wearing size M and his height is 6\\\'1", chest 40" and waist 32".</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>Adidas authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['1299'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shorts-34ths/"><span itemprop="name">Shorts &amp; 3/4ths</span></a></li></ol>\'', 'discount': ['(-32%)'], '_id': '594963c052ab721620f39303'}]

    return self.render_to_response({
      "page": "websites",
      "secondary_page": self.secondary_page,
      "data": self.data,
      "default_data": default_data,
      "categories_data": categories_data
    })

  def post(self,request,*args, **kwargs):
    db =DB()
    website_data_list = []
    categories_data = {}
    error = False
    default_data = None
    # print(self.subpage == "1")
    if self.subpage == "1":
      r = request.POST.dict()
      r["categories"] = request.POST.getlist("cat")
      if "cat" in r:
        del r["cat"]
      request.session["page_1_data"] = r
      # print ("r",r)
      categories_data = viewform(request.POST)
      if bool(categories_data[request.POST.get("urlname")]) == False:
        error = True
        if "page_1_data" in request.session:
          default_data = request.session["page_1_data"]

      else:
        self.template_name = "dashboard/websites/add_website_page_2.html"

      # print ("viewform",categories_data)

    if self.subpage == "2":
      r = request.POST.dict()
      for cat in request.session["page_1_data"]["categories"]:
        r[cat] = request.POST.getlist(cat)
      request.session["page_2_data"] = r
      self.template_name = "dashboard/websites/add_website_page_3.html"


    if self.subpage == "3":
      r = request.POST.dict()
      request.session["page_3_data"] = r

      # print(request.session["page_3_data"])
      # return HttpResponse("asdf")

      page_1_data = request.session['page_1_data'] 
      page_2_data = request.session['page_2_data'] 
      page_3_data = request.session['page_3_data'] 
      items = {'approach':"click"}
      listing_dict = {}
      product_dict = {}

      listing_dict['product_title'] = {"xpath":page_3_data.get('xpath_product_title',''),"xpath_type":page_3_data.get('','')}
      listing_dict['url'] = {"xpath":page_3_data.get('xpath_url',''),"xpath_type":page_3_data.get('type_url','')}
      listing_dict['image'] = {"xpath":page_3_data.get('xpath_image',''),"xpath_type":page_3_data.get('type_image','')}
      product_dict['product_name'] = {"xpath":page_3_data.get('xpath_product_name',''),"xpath_type":page_3_data.get('type_product_name','')}
      product_dict['product_id'] = {"xpath":page_3_data.get('xpath_product_id',''),"xpath_type":page_3_data.get('type_product_id','')}
      product_dict['rating'] = {"xpath":page_3_data.get('xpath_rating',''),"xpath_type":page_3_data.get('type_rating','')}
      product_dict['review_url'] = {"xpath":page_3_data.get('xpath_review_url',''),"xpath_type":page_3_data.get('type_review_url','')}
      product_dict['mrp'] = {"xpath":page_3_data.get('xpath_mrp',''),"xpath_type":page_3_data.get('type_mrp','')}
      product_dict['discount'] = {"xpath":page_3_data.get('xpath_discount',''),"xpath_type":page_3_data.get('type_discount','')}
      product_dict['selling_price'] = {"xpath":page_3_data.get('xpath_selling_price',''),"xpath_type":page_3_data.get('type_selling_price','')}
      product_dict['images'] = {"xpath":page_3_data.get('xpath_images',''),"xpath_type":page_3_data.get('type_images','')}
      product_dict['shipping_charge'] = {"xpath":page_3_data.get('xpath_shipping_charge',''),"xpath_type":page_3_data.get('type_shipping_charge','')}
      product_dict['delivery_time'] = {"xpath":page_3_data.get('xpath_delivery_time',''),"xpath_type":page_3_data.get('type_delivery_time','')}
      product_dict['material'] = {"xpath":page_3_data.get('xpath_material',''),"xpath_type":page_3_data.get('type_material','')}
      product_dict['color'] = {"xpath":page_3_data.get('xpath_color',''),"xpath_type":page_3_data.get('type_color','')}
      product_dict['description'] = {"xpath":page_3_data.get('xpath_description',''),"xpath_type":page_3_data.get('type_description','')}
      product_dict['specifications'] = {"xpath":page_3_data.get('xpath_specifications',''),"xpath_type":page_3_data.get('type_specifications','')}
      product_dict['thumbnail'] = {"xpath":page_3_data.get('xpath_thumbnail',''),"xpath_type":page_3_data.get('type_thumbnail','')}
      product_dict['breadcrumb'] = {"xpath":page_3_data.get('xpath_breadcrumb',''),"xpath_type":page_3_data.get('type_breadcrumb','')}
      product_dict['sizes'] = {"xpath":page_3_data.get('xpath_sizes',''),"xpath_type":page_3_data.get('type_sizes','')}
      paginate_parameters = {}
      pagination_type = page_3_data.get("paginationType","")
      if pagination_type:
        paginate_parameters['scroll_time_wait'] = int(page_3_data.get("pagination_pause_time",5))
        paginate_parameters['page_listing'] = int(page_3_data.get("pagination_items_per_page",20))
        paginate_parameters["products_path_count"] = page_3_data.get("xpath_product_count")
        paginate_parameters['load_more_xpath'] = page_3_data.get("xpath_next_button","")
        page_1_data['pagination'] = {"type":pagination_type,"paginate_parameters":paginate_parameters}

      # product_dict[''] = {"xpath":page_3_data.get('xpath_',''),"xpath_type":page_3_data.get('type_','')}
      items['fields'] = {'listing':listing_dict,'product':product_dict}
      items['xpath'] = page_3_data.get("items_xpath_1","")
      items['xpath_2'] = page_3_data.get("items_xpath_2","")
      categoryType = page_1_data.get("categoryType","")
      if "clickhover" in categoryType or "hover" in categoryType:
        items['hover'] = True
      else:
        items['hover'] = False
      items['approach'] = "click"
      page_1_data['items'] = items
      try:
        del page_1_data['csrfmiddlewaretoken']
        del page_2_data['csrfmiddlewaretoken']
      except:
        items['approach'] = "click"

      category_dict = {}
      for category,category_list in page_2_data.items():
          category_dict[category]= []
          for category_url in category_list:
            category_dict[category].append([category_url,False,0,0,0,"N/A"])
      category_dict = {page_1_data['urlname']:category_dict}
      website_name = page_1_data['urlname']
      db_handle =db.get_cursor(website_name+"_categories")
      logging.info("Categorical URLs Gathered for "+ website_name)
      logging.info("Categorical URLs Updated for "+website_name)
      print (json.dumps(page_1_data,indent=4))
      print (json.dumps(page_2_data,indent=4))
      homepage = page_1_data['url']
      # print (page_1_data['url'])
      for category in page_2_data.keys():
        category_url = page_2_data[category][4]
        website_data = viewdata(category_url,website_name,test=True,website_settings =page_1_data)
        # print (website_data)
        if website_data:
          website_data_list+=website_data
      request.session['page_4_data'] = page_1_data

      if len(website_data_list) > 0:
        self.template_name = "dashboard/websites/add_website_page_4.html"
        db.replace_cateogrical_data(db_handle,website_name,category_dict)

      else:
        self.template_name = "dashboard/websites/add_website_page_3.html"
        if "page_3_data" in request.session:
          default_data = request.session["page_3_data"]


      # TODO: IF EVERYTHING IS SUCCESSFUL CLEAR SESSION

    return self.render_to_response({
      "page":"websites",
      "secondary_page": self.secondary_page,
      "categories_data" : categories_data,
      "data":website_data_list,
      "error": error,
      "default_data": default_data
    })


def resetNewWebste(request):
  clearSessionData(request)
  
  return HttpResponseRedirect(reverse("add_website"))


class Websites(TemplateView):
  template_name = 'dashboard/websites/websites.html'
  secondary_page = "all_websites"
  def get(self, request, *args, **kwargs):
    db = DB()
    website_list = []
    collection_names = db.db_handle.collection_names()
    # print (collection_names)
    for collection_name in collection_names:
      website_dict = {}
      if collection_name.endswith("_categories"):
        website_name = collection_name.replace("_categories","")
        db_cursor = db.get_cursor(collection_name)
        category_dict = db.read_data(db_cursor,{website_name:{'$exists':True}})[0]
        del category_dict["_id"]
        categories_list = category_dict[website_name].keys()
        categories_list = [each for each in categories_list if each != ""]
        website_list.append({"name":website_name,"categories":categories_list})
    # website_list = [{"name": "jabong", "categories": ["MEN", "WOMEN"]}, {"name": "tatacliq", "categories": ["MEN", "WOMEN"]}] 
    return self.render_to_response({
      "page": "websites",
      "secondary_page": self.secondary_page,
      "websites": website_list
    })

class EditWebsite(TemplateView):

  template_name = 'dashboard/websites/edit_website_page_3.html'
  
  def get(self, request, website, *args, **kwargs):
    print(website)
    with open('eComCrawl/jsons/' + website + ".json") as data_file:    
      data = json.load(data_file)
      clearSessionData(request)

      #{'submit': '', 'categoryType': 'clickhover', 'type': 'type test', 'urlname': 'jabong', 'xpath': 'test', 'url': 'http://www.gadgetsnow.com/', 'categories': ['cat1', 'cat2'], 'csrfmiddlewaretoken': 'rNUiOvzap3IPxQqVpn3YI5CE3yE94sMJpynJJnjfZDPvvVx0xgbuZazL5ajbdWl6'}
      # request.session["page_1_data"] = {
      #   'urlname': data["urlname"],
      #   'url': data["url"],
      #   'categories': data['cat'],
      #   'xpath': data['xpath'],
      #   'categoryType': data['categoryType'],
      #   'type': data['type']
      # }


      # TODO: GET PAGE 2 DATA FROM DATASASE HERE 
      print(data["items"])
      default_data = {
        "items_xpath_1": data["items"]["xpath"],
        "xpath_product_title_1": data["items"]["fields"]["listing"]["product_title"]["xpath"],
        "type_product_title_1": data["items"]["fields"]["listing"]["product_title"]["xpath_type"],
        "xpath_url_1": data["items"]["fields"]["listing"]["url"]["xpath"],
        "type_url_1": data["items"]["fields"]["listing"]["url"]["xpath_type"],
        "paginationType": data["pagination"]["type"],
        "pagination_pause_time": data["pagination"]["paginate_parameters"].get("scroll_time_wait", ""),
        "pagination_items_per_page": data["pagination"]["paginate_parameters"].get("page_listing", ""),
        "xpath_product_count": data["pagination"]["paginate_parameters"].get("products_path_count", ""),
        "xpath_next_button": data["pagination"]["paginate_parameters"].get("load_more_xpath", ""),
        
        
        "xpath_product_name": data["items"]["fields"]["product"]["product_name"]["xpath"],
        "type_product_name": data["items"]["fields"]["product"]["product_name"]["xpath_type"],

        "xpath_product_id": data["items"]["fields"]["product"]["product_id"]["xpath"],
        "type_product_id": data["items"]["fields"]["product"]["product_id"]["xpath_type"],

        "xpath_rating": data["items"]["fields"]["product"]["rating"]["xpath"],
        "type_rating": data["items"]["fields"]["product"]["rating"]["xpath_type"],

        "xpath_review_url": data["items"]["fields"]["product"]["review_url"]["xpath"],
        "type_review_url": data["items"]["fields"]["product"]["review_url"]["xpath_type"],

        "xpath_mrp": data["items"]["fields"]["product"]["mrp"]["xpath"],
        "type_mrp": data["items"]["fields"]["product"]["mrp"]["xpath_type"],

        "xpath_discount": data["items"]["fields"]["product"]["discount"]["xpath"],
        "type_discount": data["items"]["fields"]["product"]["discount"]["xpath_type"],

        "xpath_selling_price": data["items"]["fields"]["product"]["selling_price"]["xpath"],
        "type_selling_price": data["items"]["fields"]["product"]["selling_price"]["xpath_type"],

        "xpath_images": data["items"]["fields"]["product"]["images"]["xpath"],
        "type_images": data["items"]["fields"]["product"]["images"]["xpath_type"],

        "xpath_shipping_charge": data["items"]["fields"]["product"]["shipping_charge"]["xpath"],
        "type_shipping_charge": data["items"]["fields"]["product"]["shipping_charge"]["xpath_type"],

        "xpath_delivery_time": data["items"]["fields"]["product"]["delivery_time"]["xpath"],
        "type_delivery_time": data["items"]["fields"]["product"]["delivery_time"]["xpath_type"],

        "xpath_material": data["items"]["fields"]["product"]["material"]["xpath"],
        "type_material": data["items"]["fields"]["product"]["material"]["xpath_type"],

        "xpath_color": data["items"]["fields"]["product"]["color"]["xpath"],
        "type_color": data["items"]["fields"]["product"]["color"]["xpath_type"],

        "xpath_description": data["items"]["fields"]["product"]["description"]["xpath"],
        "type_description": data["items"]["fields"]["product"]["description"]["xpath_type"],

        "xpath_specifications": data["items"]["fields"]["product"]["specifications"]["xpath"],
        "type_specifications": data["items"]["fields"]["product"]["specifications"]["xpath_type"],

        "xpath_thumbnail": data["items"]["fields"]["product"]["thumbnail"]["xpath"],
        "type_thumbnail": data["items"]["fields"]["product"]["thumbnail"]["xpath_type"],

        "xpath_breadcrumb": data["items"]["fields"]["product"]["breadcrumb"]["xpath"],
        "type_breadcrumb": data["items"]["fields"]["product"]["breadcrumb"]["xpath_type"],

        "xpath_sizes": data["items"]["fields"]["product"]["sizes"]["xpath"],
        "type_sizes": data["items"]["fields"]["product"]["sizes"]["xpath_type"],

      }


    return self.render_to_response({
      "page":"websites",
      "default_data": default_data
    })

  def post(self, request, website, *args, **kwargs):
    with open('eComCrawl/jsons/' + website + ".json", 'r+') as data_file:    
      data = json.load(data_file)

      page_3_data = request.POST
      pagination_dict = {}
      listing_dict = {}
      product_dict = {}

      listing_dict['product_title'] = {"xpath":page_3_data.get('xpath_product_title',''),"xpath_type":page_3_data.get('','')}
      listing_dict['url'] = {"xpath":page_3_data.get('xpath_url',''),"xpath_type":page_3_data.get('type_url','')}
      listing_dict['image'] = {"xpath":page_3_data.get('xpath_image',''),"xpath_type":page_3_data.get('type_image','')}
      product_dict['product_name'] = {"xpath":page_3_data.get('xpath_product_name',''),"xpath_type":page_3_data.get('type_product_name','')}
      product_dict['product_id'] = {"xpath":page_3_data.get('xpath_product_id',''),"xpath_type":page_3_data.get('type_product_id','')}
      product_dict['rating'] = {"xpath":page_3_data.get('xpath_rating',''),"xpath_type":page_3_data.get('type_rating','')}
      product_dict['review_url'] = {"xpath":page_3_data.get('xpath_review_url',''),"xpath_type":page_3_data.get('type_review_url','')}
      product_dict['mrp'] = {"xpath":page_3_data.get('xpath_mrp',''),"xpath_type":page_3_data.get('type_mrp','')}
      product_dict['discount'] = {"xpath":page_3_data.get('xpath_discount',''),"xpath_type":page_3_data.get('type_discount','')}
      product_dict['selling_price'] = {"xpath":page_3_data.get('xpath_selling_price',''),"xpath_type":page_3_data.get('type_selling_price','')}
      product_dict['images'] = {"xpath":page_3_data.get('xpath_images',''),"xpath_type":page_3_data.get('type_images','')}
      product_dict['shipping_charge'] = {"xpath":page_3_data.get('xpath_shipping_charge',''),"xpath_type":page_3_data.get('type_shipping_charge','')}
      product_dict['delivery_time'] = {"xpath":page_3_data.get('xpath_delivery_time',''),"xpath_type":page_3_data.get('type_delivery_time','')}
      product_dict['material'] = {"xpath":page_3_data.get('xpath_material',''),"xpath_type":page_3_data.get('type_material','')}
      product_dict['color'] = {"xpath":page_3_data.get('xpath_color',''),"xpath_type":page_3_data.get('type_color','')}
      product_dict['description'] = {"xpath":page_3_data.get('xpath_description',''),"xpath_type":page_3_data.get('type_description','')}
      product_dict['specifications'] = {"xpath":page_3_data.get('xpath_specifications',''),"xpath_type":page_3_data.get('type_specifications','')}
      product_dict['thumbnail'] = {"xpath":page_3_data.get('xpath_thumbnail',''),"xpath_type":page_3_data.get('type_thumbnail','')}
      product_dict['breadcrumb'] = {"xpath":page_3_data.get('xpath_breadcrumb',''),"xpath_type":page_3_data.get('type_breadcrumb','')}
      product_dict['sizes'] = {"xpath":page_3_data.get('xpath_sizes',''),"xpath_type":page_3_data.get('type_sizes','')}
      paginate_parameters = {}
      pagination_type = page_3_data.get("paginationType","")

      if pagination_type:
        paginate_parameters['scroll_time_wait'] = int(page_3_data.get("pagination_pause_time",5))
        paginate_parameters['page_listing'] = int(page_3_data.get("pagination_items_per_page",20))
        paginate_parameters["products_path_count"] = page_3_data.get("xpath_product_count")
        paginate_parameters['load_more_xpath'] = page_3_data.get("xpath_next_button","")
        pagination_dict = {"type":pagination_type,"paginate_parameters":paginate_parameters}

      
      data["items"]["fields"] = {'listing':listing_dict,'product':product_dict}
      data["items"]["xpath"] = page_3_data.get("items_xpath_1","")
      data["items"]['xpath_2'] = page_3_data.get("items_xpath_2","")

      data["pagination"] = pagination_dict


      data_file.seek(0)        # <--- should reset file position to the beginning.
      json.dump(data, data_file, indent=4)
      data_file.truncate()     # remove remaining part

      return HttpResponseRedirect(reverse("websites"))

class WebsiteCategory(TemplateView):
  template_name = "dashboard/websites/website_category.html"
  def get(self, request, website, category, *args, **kwargs):
    db = DB()
    # get dat  from database
    db_handle =db.get_cursor(website+"_categories")
    category_dict = db.read_data(db_handle,{website:{'$exists':True}})[0][website][category]
    final_dict = {}
    running_list = []
    running_urls = []
    try:
      running_urls = db.get_cursor("running_urls")
      running_list = db.read_data(running_urls,{})[0]['urls']
    except:
      running_list = []
    for category_list in category_dict:
      # category_dict[category].append([category_url,False,0,0,"N/A"])
      if category_list[0] in running_list:
        final_dict[category_list[0]] = {"crawled_status":category_list[1],"items_gathered":category_list[2],
                                      "total_count":category_list[3],"last_crawled":category_list[5],
                                      "unique_items":category_list[4],"current_status":"running"}
      else:
        final_dict[category_list[0]] = {"crawled_status":category_list[1],"items_gathered":category_list[2],
                                      "total_count":category_list[3],"last_crawled":category_list[5],
                                      "unique_items":category_list[4],"current_status":"ready"}

    return self.render_to_response({
      "page": "websites",
      "website_name": website,
      "category": category,
      "urls": final_dict
    })

    # return self.render_to_response({
    #   "page": "websites",
    #   "website_name": website,
    #   "category": category,
    #   "urls": {
    #     'http://www.jabong.com/women/new-products/?source=topnav_women': {
    #       'crawled_status': False,
    #       "last_crawled" : "5 hours ago",
    #       "items_gathered": 0,
    #       "total_count":"2",
    #       "unique_items":"3",
    #       "current_status": "running"
    #     }, 
    #     'http://www.jabong.com/women/new-products/?source=blabla':{
    #       'crawled_status':False,
    #       "last_crawled":"10 hours ago",
    #       "items_gathered":0,
    #       "total_count":"12",
    #       "unique_items":"5",
    #       "current_status": "ready"
    #     }
    #   }
    # })

class MonitorCrawlers(TemplateView):
  template_name = 'dashboard/monitor_crawlers/monitor_crawlers.html'

  def get(self, request, *args, **kwargs):
    return self.render_to_response({
      "page": "monitor_crawlers",
    })

def MonitorCrawlersApi(request):
  return JsonResponse(tasksOutput(), safe = False)
  # return JsonResponse([{
  #   "task": "some task name",
  #   "site": "google.com",
  #   "status": "success",
  #   "started": "starting time",
  #   "completed": "completed time",
  #   "elapsed": "elapsed time"
  # }, {
  #   "task": "some task name",
  #   "site": "google.com",
  #   "status": "failure",
  #   "started": "starting time",
  #   "completed": "completed time",
  #   "elapsed": "elapsed time"
  # }], safe = False)

class Logs(TemplateView):
  template_name = 'dashboard/logs/logs.html'

  def get(self, request, *args, **kwargs):
    log_text = open(BASE_DIR+"/eComCrawl/celery.log","r").read()
    log_text = log_text.split("\n")[::-1]
    # log_text = ["Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", "THis is another text here", "Heres another"]

    return self.render_to_response({
      "page": "logs",
      "log_data" : log_text,
    })



class StartCrawl(View):
  def post(self, request, *args, **kwargs):
    data_dict = {}
    category_url = request.POST.get("url")
    website_name = request.POST.get("site")
    # print ("site",website_name)
    # print ("url",category_url)
    db = DB()
    running_list = []
    running_urls = db.get_cursor("running_urls")
    try:
      running_list = db.read_data(running_urls,{})[0]['urls']
    except:
      running_list = []
    if running_list:
      running_list.append(category_url)

      db.replace_cateogrical_data(running_urls,"urls",{"urls":running_list})
    else:
      db.replace_cateogrical_data(running_urls,"urls",{"urls":[category_url]})
    data_dict = viewdata(category_url,website_name,test=False)
    # TODO: grab the url and start crawler
    # append the url to "Running" table

    return HttpResponse("running")

class Recent(TemplateView):
  template_name = 'dashboard/recent/recent.html'

  def get(self, request, *args, **kwargs):
    website_data = []
    db = DB()
    running_list = []
    running_urls = db.get_cursor("running_urls")
    try:
      running_list = db.read_data(running_urls,{})[0]['urls']
    except:
      running_list = []
    print (running_list)
    if running_list:
      for cat_url in running_list:
        print (cat_url)
        website_name = urllib.parse.urlparse(cat_url)
        website_name = website_name.netloc
        website_name = website_name.split(".")[-2]
        print (website_name)
        end_date = datetime.now()-timedelta(days=1)
        read_cursor = db.get_cursor(website_name.lower())
        data = db.read_data(read_cursor,{'crawled_date':{'$gte':end_date.strftime("%Y-%m-%d %H:%M:%S"),'$lt':datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
        print (data)
        for each_data in data:
          del each_data["_id"]
          website_data.append(each_data)
          print (each_data)

    data = [{'product_name': ['Khaki Solid Slim Fit Chinos'], 'description': ['\n'], 'url': 'http://www.jabong.com/blackberrys-Khaki-Solid-Slim-Fit-Chinos-300077005.html?pos=1&cid=BL114MA03YFRINDFAS', 'product_brand': ['Blackberrys'], 'product_title': ['Blackberrys '], 'images': ['http://static2.jassets.com/p/Blackberrys-Khaki-Solid-Slim-Fit-Chinos-8761-500770003-1-pdp_slider_m.jpg', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['2195'], 'price': ['1756'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fit</span><span>Slim</span></li><li><span class="product-info-left">Color</span><span>Khaki</span></li><li><span class="product-info-left">Wash Care</span><span>Machine Wash, Do Not Bleach, Do Not Tumble Dry, Cool Iron, Dry Clean</span></li><li><span class="product-info-left">Style</span><span>Solid</span></li><li><span class="product-info-left">SKU</span><span>BL114MA03YFRINDFAS</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>Blackberrys authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['1756'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/trousers/"><span itemprop="name">Trousers</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/trousers/casual-trousers/"><span itemprop="name">Casual Trousers</span></a></li></ol>\'', 'discount': ['(-20%)'], 'id': '5949635e52ab721620f392ff'},
           {'product_name': ['Black Solid Slim Fit Formal Trouser'], 'description': ['\n'], 'url': 'http://www.jabong.com/John_Player-Black-Solid-Slim-Fit-Formal-Trouser-300076981.html?pos=2&cid=JO423MA95BKVINDFAS', 'product_brand': ['John Players'], 'product_title': ['John Players '], 'images': ['http://static2.jassets.com/p/John-Players-Black-Solid-Slim-Fit-Formal-Trouser-2961-189670003-1-pdp_slider_m.webp', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['1999'], 'price': ['1000'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fabric</span><span>Blended</span></li><li><span class="product-info-left">Fit</span><span>Slim</span></li><li><span class="product-info-left">Color</span><span>Black</span></li><li><span class="product-info-left">Wash Care</span><span>Machine Wash, Do Not Bleach, Do Not Tumble Dry, Cool Iron, Dry Clean</span></li><li><span class="product-info-left">Style</span><span>Solid</span></li><li><span class="product-info-left">SKU</span><span>JO423MA95BKVINDFAS</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>John Players authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['1000'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/trousers/"><span itemprop="name">Trousers</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/trousers/formal-trousers/"><span itemprop="name">Formal Trousers</span></a></li></ol>\'', 'discount': ['(-50%)'], 'id': '5949638252ab721620f39300'},
           {'product_name': ['Orange Checked Regular Fit Casual Shirt'], 'description': [], 'url': 'http://www.jabong.com/Tommy_Hilfiger-Orange-Checked-Regular-Fit-Casual-Shirt-300074043.html?pos=3&cid=TO348MA16JACINDFAS', 'product_brand': ['Tommy Hilfiger'], 'product_title': ['Tommy Hilfiger '], 'images': ['http://static2.jassets.com/p/Tommy-Hilfiger-Orange-Checked-Regular-Fit-Casual-Shirt-1959-340470003-1-pdp_slider_m.webp', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['4299'], 'price': ['3226'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fit</span><span>Regular</span></li><li><span class="product-info-left">Color</span><span>Orange</span></li><li><span class="product-info-left">Sleeves</span><span>Full Sleeves</span></li><li><span class="product-info-left">Wash Care</span><span>Machine Wash, Do Not Bleach, Do Not Tumble Dry, Cool Iron, Dry Clean</span></li><li><span class="product-info-left">Fabric</span><span>Cotton</span></li><li><span class="product-info-left">Style</span><span>Checked</span></li><li><span class="product-info-left">SKU</span><span>TO348MA16JACINDFAS</span></li><li><span class="product-info-left">Model Stats</span><span>Model is wearing size M and his height is 6\\\'0", chest 37" and waist 32".</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>Tommy Hilfiger authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['3226'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shirts/"><span itemprop="name">Shirts</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shirts/casual-shirts/"><span itemprop="name">Casual Shirts</span></a></li></ol>\'', 'discount': ['(-25%)'], 'id': '594963a452ab721620f39301'},
           {'product_name': ['Pink Solid Slim Fit Casual Shirt'], 'description': ['\n'], 'url': 'http://www.jabong.com/John_Player-Pink-Solid-Slim-Fit-Casual-Shirt-300082745.html?pos=4&cid=JO423MA16QDSINDFAS', 'product_brand': ['John Players'], 'product_title': ['John Players '], 'images': ['http://static2.jassets.com/p/John-Players-Pink-Solid-Slim-Fit-Casual-Shirt-9288-547280003-1-pdp_slider_m.webp', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['1799'], 'price': ['900'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fit</span><span>Slim</span></li><li><span class="product-info-left">Color</span><span>Pink</span></li><li><span class="product-info-left">Sleeves</span><span>Full Sleeves</span></li><li><span class="product-info-left">Wash Care</span><span>Machine Wash, Do Not Bleach, Do Not Tumble Dry, Cool Iron, Dry Clean</span></li><li><span class="product-info-left">Fabric</span><span>Cotton</span></li><li><span class="product-info-left">Style</span><span>Solid</span></li><li><span class="product-info-left">SKU</span><span>JO423MA16QDSINDFAS</span></li><li><span class="product-info-left">Model Stats</span><span>Model is wearing size 40 and his height is 6\\\'1", chest 36" and waist 32".</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>John Players authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['900'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shirts/"><span itemprop="name">Shirts</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shirts/casual-shirts/"><span itemprop="name">Casual Shirts</span></a></li></ol>\'', 'discount': ['(-50%)'], 'id': '594963b852ab721620f39302'},
           {'product_name': ['Club Black Training Shorts'], 'description': [], 'url': 'http://www.jabong.com/Adidas-Club-Black-Training-Shorts-300074465.html?pos=5&cid=AD004MA47YDRINDFAS', 'product_brand': ['Adidas'], 'product_title': ['Adidas '], 'images': ['http://static2.jassets.com/p/Adidas-Club-Black-Training-Shorts-7710-564470003-1-pdp_slider_m.webp', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/img1x1.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png', 'http://static1.jabong.com/live/images/zoom.png'], 'mrp': ['1899'], 'price': ['1299'], 'specifications': 'b\'<ul class="prod-main-wrapper"><li><span class="product-info-left">Fabric</span><span>Polyester</span></li><li><span class="product-info-left">Fit</span><span>Regular</span></li><li><span class="product-info-left">Color</span><span>Black</span></li><li><span class="product-info-left">Style</span><span>Solid</span></li><li><span class="product-info-left">SKU</span><span>AD004MA47YDRINDFAS</span></li><li><span class="product-info-left">Model Stats</span><span>Model is wearing size M and his height is 6\\\'1", chest 40" and waist 32".</span></li><li class="authorized-brand"><span class="product-info-left">Authorization</span><span>Adidas authorized online sales partner. <div class="brand-authorization"><a href="javascript:void()" class="authorized-link" target="_blank" id="certificate">View Certificate</a></div></span></li></ul>                                        \'', 'selling_price': ['1299'], 'breadcrumb': 'b\'<ol itemscope="" itemtype="http://schema.org/BreadcrumbList" class="breadcrumb"><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com//"><span itemprop="name">Home</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/"><span itemprop="name">Men</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/"><span itemprop="name">Clothing</span></a></li><li itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a itemprop="url" href="http://www.jabong.com/men/clothing/shorts-34ths/"><span itemprop="name">Shorts &amp; 3/4ths</span></a></li></ol>\'', 'discount': ['(-32%)'], '_id': '594963c052ab721620f39303'}]

    if website_data!=[]:
      data = website_data
    return self.render_to_response({
      "page": "recent",
      "data": data
    }) 