autocompletar = function() {

    $(".autocompletar").each(function() {
      const self = $(this);
      const source = self.data('url'); //.split("_").pop();
      const target = self.data('target');
      //const children = $(this).attr('children');
      $(this).autocomplete({
        //search: _buscar(children),
        messages: {
          noResults: '',
          results: function() {
          }
        },
        source: function(request, response) {
          _fuente(request, response, source, target, parent)
        },
        select: function(event, ui) {
          _seleccionar(event, ui, target)
        },
        open: function() {
          $(this).css('z-index', 100);
          return false;
        },
        width: 300,
        delay: 10,
        cacheLength: 0,
        scroll: false,
        highlight: true,
        minLength: 3
      }).data('ui-autocomplete')._renderItem = _render;
    });
  }
  
  _render = function(ul, item) {
    const re = new RegExp(this.term, "gi");
    const t = item.label.replace(re, '<span class="bold_autocomplete">' + '$&' + '</span>');
    const t2 = (item.path != null) ? item.path.replace(re, '<span class="bold_autocomplete">' + '$&' + '</span>') : null;
    return $('<li></li>').data('ui-autocomplete-item', item).append('<a>' + t + ((t2 != null) ? '<span class="path">' + t2 + '</span>' : '') + '</a>').appendTo(ul);
  }
  
  _buscar = function(children) {
    if (typeof children != 'undefined') {
      const pieces = children.split(',');
      $(pieces).each(function(i) {
        $('#' + pieces[i] + '_hidden', '#' + pieces[i]).val('');
        $('#' + pieces[i]).val('');
      });
    }
  }
  
  _seleccionar = function(event, ui, target) {
    if (ui.item.valido == true) {
      $(this).val(ui.item.label);
      $('#' + target).val(ui.item.id);
    }
    return false;
  }
  
  _fuente = function(request, response, source, target, parent) {
    $.ajax({
      url: source,
      dataType: "json",
      data: {
        val: request.term,
        //p: $('#' + parent).val()
      },
      type: 'post',
      error: function() {
        result = [{
          label: 'Sin resultados para: ' + request.term,
          path: null,
          value: null,
          id: null,
          valido: false
        }];
      },
      success: function(data) {
        let result = [];
        if (data !== null && data.length > 0) {
          $.map(data, function(item) {
            const id = item.id;
            const path = item.path;
            const value = (typeof item.nombre != 'undefined') ? item.nombre : item.descripcion;
            result.push({
              label: value,
              path: path,
              value: value,
              id: id,
              valido: true
            });
            //$('#' + target).val('');
          });
        } else {
          result = [{
              label: 'Sin resultados para: ' + request.term,
              path: null,
              value: null,
              id: null,
              valido: false
            }];
        }
        response(result);
      }
    });
  }
  
  $(document).ready(function() {
  
    autocompletar();
  
  });