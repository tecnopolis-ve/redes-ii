from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastas_redes.models import Factura, ItemFactura
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile
import requests
import json
from django.http import HttpResponse

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def list(request):
    facturas = Factura.objects.filter(coleccionista=request.user.pk)
    return render(request, "usuario/facturas/list.html", {
        'data': facturas,
    })

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def detail(request, factura_id):

	url = 'http://192.168.1.8:5488/api/report'
	headers = { 'Content-Type': 'application/json' }
	body = {
		"template": { "shortid": "4oppBFQZ3x" },
		"data": { "factura_id": factura_id }
	}

	response = requests.post(url, data=json.dumps(body), headers=headers)

	django_response = HttpResponse(
		content=response.content,
		status=response.status_code,
		content_type=response.headers['Content-Type']
	)

	return django_response

    # factura = Factura.objects.filter(coleccionista=request.user.pk, pk=factura_id).prefetch_related('coleccionista').first()
    # item_factura = ItemFactura.objects.filter(factura=factura.pk).prefetch_related('objeto_subasta_evento').all()

    # html_string = render_to_string('usuario/facturas/factura.html', {'factura': factura, 'item_factura': item_factura})
    # html = HTML(string=html_string)
    # result = html.write_pdf()

    # response = HttpResponse(content_type='application/pdf;')
    # response['Content-Disposition'] = 'inline; filename=factura.pdf'
    # response['Content-Transfer-Encoding'] = 'binary'
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = open(output.name, 'rb')
    #     response.write(output.read())

    # return response
