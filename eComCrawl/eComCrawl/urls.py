"""eComCrawl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from panel.views import Dashboard, AddWebsite, AddWebsiteGenerateCategories, AddWebsiteGenerateCategoriesSiteMap, Page2Verify, Websites, EditWebsite, WebsiteCategory, MonitorCrawlers, MonitorCrawlersApi, Logs, StartCrawl, resetNewWebste, Recent
from crawlers.views import form,save_xpath_data

urlpatterns = [
    url(r'^$', Dashboard.as_view(), name="dashboard"),
    url(r'^admin/', admin.site.urls),
    url(r'^form/', form, name = "category_form"),


    url(r'^dashboard/$', Dashboard.as_view(), name="dashboard"),
    url(r'^dashboard/websites/new/$', AddWebsite.as_view(subpage = "1"), name="add_website"),
    url(r'^dashboard/websites/new/1$', AddWebsite.as_view(subpage = "1"), name="add_website_1"),
    url(r'^dashboard/websites/new/2$', AddWebsite.as_view(subpage = "2"), name="add_website_2"),
    url(r'^dashboard/websites/new/3$', AddWebsite.as_view(subpage = "3"), name="add_website_3"),
    url(r'^dashboard/websites/new/4$', AddWebsite.as_view(subpage = "4"), name="add_website_4"),
    url(r'^dashboard/websites/$', Websites.as_view(), name="websites"),

    url(r'^dashboard/websites/new/page1_generate_categories$', AddWebsiteGenerateCategories.as_view(), name="add_website_generate_categories"),
    url(r'^dashboard/websites/new/page1_generate_categories_sitemap$', AddWebsiteGenerateCategoriesSiteMap.as_view(), name="add_website_generate_categories_sitemap"),

    url(r'^dashboard/websites/page_2_verify$', Page2Verify.as_view(), name="page_2_verify"),


    url(r'^dashboard/websites/edit/(?P<website>.+)$', EditWebsite.as_view(), name="edit_website"),


    url(r'^dashboard/recent/$', Recent.as_view(), name="recent"),

    url(r'^dashboard/websites/reset', resetNewWebste, name="reset_new_website"),

    # url(r'^dashboard/websites/(?P<string>[\w\-]+)/(?P<string>[\w\-]+)/$', WebsiteCategory.as_view(), name="website_category"),
    url(r'^dashboard/websites/(?P<website>.+)/(?P<category>.+)$', WebsiteCategory.as_view(), name="website_category"),

    url(r'^dashboard/monitor_crawlers/$', MonitorCrawlers.as_view(), name="monitor_crawlers"),
    url(r'^dashboard/monitor_crawlers_api/$', MonitorCrawlersApi, name="monitor_crawlers_api"),

    url(r'^dashboard/logs/$', Logs.as_view(), name="logs"),

    url(r'^startcrawl/$', StartCrawl.as_view(), name="start_crawl"),
    url(r'^save_xpaths/$', save_xpath_data, name="save_xpath"),
]

