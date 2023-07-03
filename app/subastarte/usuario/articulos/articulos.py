from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastarte.models import ObjetoSubastaEvento
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
    objeto_subasta_evento = ObjetoSubastaEvento.objects.filter(ganador_id=request.user.pk)
    monedas = objeto_subasta_evento.filter(moneda__isnull=False)
    pinturas = objeto_subasta_evento.filter(pintura__isnull=False)
    return render(request, "usuario/articulos/list.html", {
        'monedas': monedas,
        'pinturas': pinturas,
    })

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def detail(request, ose_id):

	url = 'http://192.168.1.8:5488/api/report'
	headers = { 'Content-Type': 'application/json' }
	body = {
		"template": { "shortid": "QnC3-i6Y1J" },
		"data": { "ose_id": ose_id }
	}

	response = requests.post(url, data=json.dumps(body), headers=headers)

	django_response = HttpResponse(
		content=response.content,
		status=response.status_code,
		content_type=response.headers['Content-Type']
	)

	return django_response

    # evento = ObjetoSubastaEvento.objects.filter(ganador=request.user.pk, pk=articulo_id).prefetch_related('ganador').first()

    # html_string = render_to_string('usuario/articulos/certificado.html', {'evento': evento})
    # html = HTML(string=html_string)
    # result = html.write_pdf()

    # response = HttpResponse(content_type='application/pdf;')
    # response['Content-Disposition'] = 'inline; filename=certificado.pdf'
    # response['Content-Transfer-Encoding'] = 'binary'
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = open(output.name, 'rb')
    #     response.write(output.read())

    # return response