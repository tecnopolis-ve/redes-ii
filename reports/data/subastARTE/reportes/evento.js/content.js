const { Client } = require('pg');

const config = {
    user: 'user',
    host: 'localhost',
    database: 'subastarte_db',
    password: 'dummypass',
    port: 5432,
}

async function beforeRender(req, res) {

    const client = new Client(config);
    await client.connect();
    const evento = await client.query(
        `select to_char(mse.fecha, 'DD-MM-YYYY HH:MI:SS AM') fecha_evento,
        mse.horas,
        mse.tipo,
        mse.nombre,
        mse.cancelado, 
        mse.costo_ins_client, 
        mse.costo_ins_general,
        mse.lugar_subasta,
        count (msp.id) total_participantes

        from msi_subastarte_organiza mso 
        inner join msi_subastarte_evento mse 
        on mso.evento_id = mse.id 
        left join msi_subastarte_participante msp
        on mso.evento_id = msp.evento_id
        where mso.evento_id = ${req.data.evento_id} and 
        mso.tienda_id = ${req.data.tienda_id}
        group by mse.fecha,
        mse.horas,
        mse.tipo,
        mse.nombre,
        mse.cancelado, 
        mse.costo_ins_client, 
        mse.costo_ins_general,
        mse.lugar_subasta`
    );

    const objeto_subasta_evento = await client.query(
        `select 
        mso.tipo_puja,
        mso.precio,
        mso.bid,
        mso.ask,
        mso.orden,
        mso.ganador_id,
        mso.pintura_id,
        mso.moneda_id,
        msp.nur nur_pintura,
        msp.estilo, 
        msp.titulo, 
        msp.titulo_original, 
        msp.anyo, 
        concat(msp.ancho, 'cm x ', msp.alto, 'cm') dimensiones,
        msm.nombre nombre_moneda,
        msm.nur nur_moneda,
        msm.denominacion,
        msc.num_exp_unico,
        concat(msco.nombre, ' ', msco.segundo_nombre, ' ', msco.apellido, ' ', msco.segundo_apellido) nombre_coleccionista
        from msi_subastarte_objetosubastaevento mso 

        left join msi_subastarte_pintura msp 
        on mso.pintura_id = msp.nur 
        left join msi_subastarte_moneda msm 
        on mso.moneda_id = msm.nur
        left join msi_subastarte_cliente msc
        on mso.ganador_id = msc.coleccionista_id and msc.tienda_id = mso.tienda_id
        left join msi_subastarte_coleccionista msco
        on msc.coleccionista_id = msco.user_id
        where 
        mso.tienda_id = ${req.data.tienda_id} and 
        mso.evento_id = ${req.data.evento_id}
        order by bid desc, ask desc`
    );

    let total_ventas = 0;
    let total_vendidos = 0;
    let total_precio_salida = 0;
    let total_precio_articulo = 0;

    for (item in objeto_subasta_evento.rows) {
        if(objeto_subasta_evento.rows[item].ganador_id){
            total_vendidos += 1;
            total_ventas += objeto_subasta_evento.rows[item].bid;
            total_precio_salida += objeto_subasta_evento.rows[item].ask;
            total_precio_articulo += objeto_subasta_evento.rows[item].precio;
        }
    }

    const estadisticas = {
        total_vendidos,
        total_ventas,
        total_precio_salida,
        total_ganancia_minima: total_precio_salida - total_precio_articulo,
        total_ganancia: total_ventas - total_precio_articulo,
        total_ganancia_perc: parseFloat(total_ventas * 100 / total_precio_articulo - 100).toFixed(2),
        total_precio_articulo
    }

    await client.end()
    Object.assign(req.data, { evento: evento.rows[0], objeto_subasta_evento: objeto_subasta_evento.rows, estadisticas });         
}
