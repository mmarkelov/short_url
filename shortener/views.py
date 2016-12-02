from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import KirrURL
from .forms import SubmitUrlForm
from analytics.models import ClickEvent

# Create your views here.


#def kirr_redirerect_view(request, shortcode=None, *args, **kwargs): #function based view
#	obj = get_object_or_404(KirrURL, shortcode=shortcode)
#	return HttpResponseRedirect(obj.url)

class HomeView(View):
	def get(self, request, *args, **kwargs):
		the_form = SubmitUrlForm()
		#bg_image = 'http://fonday.ru/images/tmp/8/9/original/8953x4JtBH4z55vxznf6JSO9PAKETkiy.jpg'
		context = {
			"title": "Short Your URL",
			"form": the_form,
			#"bg_image": bg_image,
		}
		return render(request, "shortener/home.html", context)

	def post(self, request, *args, **kwargs):
		form = SubmitUrlForm(request.POST)
		context = {
			"title": "Short Your URL",
			"form": form,
		}
		template = "shortener/home.html"

		if form.is_valid():
			new_url = form.cleaned_data.get("url")
			obj, created = KirrURL.objects.get_or_create(url=new_url)
			context = {
				"object": obj,
				"created": created,
			}
			if created:
				template = "shortener/success.html"
			else:
				template = "shortener/already-exists.html"

		return render(request, template, context)

class URLRedirectView(View): #class based view 
	def get(self, request, shortcode=None, *args, **kwargs):
		obj = get_object_or_404(KirrURL, shortcode=shortcode)
		ClickEvent.objects.create_event(obj)
		return HttpResponseRedirect(obj.url)



'''

def kirr_redirerect_view(request, shortcode=None, *args, **kwargs): #function based view
	#try:
	#	obj = KirrURL.objects.get(shortcode=shortcode)
	#except:
	#	obj =KirrURL.objects.all().first()

	obj = get_object_or_404(KirrURL, shortcode=shortcode)
	#obj_url = obj.url

	#obj_url = None
	#qs = KirrURL.objects.filter(shortcode__iexact=shortcode.upper())
	#if qs.exists() and qs.count() == 1:
	#	obj = qs.first()
	#	obj_url = obj.url

	return HttpResponse("hello {sc}".format(sc=obj.url))

'''