from django.shortcuts import render
from models import Urls_DB
from django.conf.urls import patterns, include, url
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, \
HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

def processPost(url):
	if url == "":
		form = "<form action='' method='POST'>\n"
		form += "Url a acortar: <input type='text' name='url' value=''><br>\n"
		form += "<input type='submit' value='enviar'>\n"
		form += "</form>\n"
		response = "<h1> Introduzca Url a acortar </h1></br></br>" + form
		return HttpResponse(response)
	elif not url.startswith("http://") and not url.startswith("https://"):
		url = "http://" + url
	try:
		new_Url = Urls_DB.objects.get(url=url)
	except Urls_DB.DoesNotExist:
		new_Url = Urls_DB(url=url)
		new_Url.save()

	response = "<p>url original: <a href=" + url + ">" + url + "</a></p>"
	response += "<p>url acortada: <a href=" + str(new_Url.id) + ">" +\
					str(new_Url.id) + "</a></p>"
	return HttpResponse(response)


@csrf_exempt
def contentapp(request, resourceName):
	urls = ""

	if request.method == "GET":
		urlList = Urls_DB.objects.all()
		urls += "<a>Listado URLs:</a></br>"
		for url in urlList:
			urls += "<pre>" + url.url + "\t\t" + str(url.id) + "<br/>"

		urls += "<br/>"
		form = "<form action='' method='POST'>\n"
		form += "Url a acortar: <input type='text' name='url' value='" + resourceName + "'><br>\n"
		form += "<input type='submit' value='enviar'>\n"
		form += "</form>\n"
		return HttpResponse(urls + form)
	elif request.method == "POST":
		url = request.POST.get("url")
		response = processPost(url)
		return response
	else:
		return HttpResponseNotAllowed("Method not allowed")


def redirect(request, id):
	try:
		url = Urls_DB.objects.get(id=id)
	except Urls_DB.DoesNotExist:
		return HttpResponseNotFound(str(id) + " not found")
	return HttpResponseRedirect(url.url)


