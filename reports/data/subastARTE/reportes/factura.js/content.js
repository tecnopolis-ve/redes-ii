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
    const fac = await client.query(
        `select 
        f.numero,
        to_char(f.fecha, 'DD-MM-YYYY') fecha_factura,
        f.total_monto,
        f.total_manejo_envio,
        concat(c.nombre, ' ', c.segundo_nombre, ' ', c.apellido, ' ', c.segundo_apellido) nombre_coleccionista,
        c.telefono telefono_coleccionista,
        pac.nombre pais_coleccionista,
        mst.nombre nombre_tienda,
        mst.email email_tienda,
        mst.telefono telefono_tienda,
        pat.nombre pais_tienda

        from msi_subastarte_factura f 
        inner join msi_subastarte_cliente msc 
        on f.cliente_id = msc.num_exp_unico 
        inner join msi_subastarte_tienda mst 
        on msc.tienda_id = mst.id 
        inner join msi_subastarte_coleccionista c 
        on f.coleccionista_id = c.user_id 
        inner join msi_subastarte_pais pac 
        on c.vive_id = pac.id 
        inner join msi_subastarte_pais pat 
        on mst.pais_id = pat.id 
        where f.numero = ${req.data.factura_id}`
    );

    const items = await client.query(
        `select 
        mso.bid,
        mso.pintura_id,
        mso.moneda_id,
        msp.nur nur_pintura,
        msp.estilo, 
        msp.titulo, 
        msp.titulo_original, 
        msp.anyo, 
        concat(msp.ancho, 'cm x ', msp.alto, 'cm') dimensiones,
        msm.nur nur_moneda,
        msm.nombre nombre_moneda,
        msm.denominacion, 
        msm.forma, 
        msm.metal, 
        msm.canto, 
        msm.diametro, 
        msm.peso, 
        msm.anyo_emision, 
        msm.org_acunyacion, 
        msm.motivo, 
        msm.anverso, 
        msm.reverso, 
        msm.divisa_id, 
        msm.pais_acunyacion_id

        from msi_subastarte_itemfactura msi 
        inner join msi_subastarte_objetosubastaevento mso
        on msi.objeto_subasta_evento_id = mso.id 
        inner join msi_subastarte_evento mse 
        on mso.evento_id = mse.id 
        left join msi_subastarte_pintura msp 
        on mso.pintura_id = msp.nur 
        left join msi_subastarte_moneda msm 
        on mso.moneda_id = msm.nur
        where msi.factura_id = ${req.data.factura_id}
        order by nur_moneda, nur_pintura`
    );

    const manejo_envio = await client.query(
        `select 
        msc.seguro,
        msc.embalaje,
        msc.recargo_envio,
        msc.costo_extra,
        SUM((mso.bid * COALESCE(msc.costo_extra, 0) / 100)) rec_extra,
        SUM((mso.bid * COALESCE(msc.recargo_envio, 0) / 100)) rec_envio,
        SUM((mso.bid * COALESCE(msc.embalaje, 0) / 100)) rec_embalaje,
        SUM((mso.bid * COALESCE(msc.seguro, 0) / 100)) rec_seguro

        from msi_subastarte_itemfactura msi 
        inner join msi_subastarte_objetosubastaevento mso
        on msi.objeto_subasta_evento_id = mso.id 
        inner join msi_subastarte_evento mse 
        on mso.evento_id = mse.id 
        left join msi_subastarte_costoenviootros msc 
        on mse.id = msc.evento_id 
        where msi.factura_id = ${req.data.factura_id}
        group by msc.costo_extra,
        msc.recargo_envio,
        msc.embalaje,
        msc.seguro,mse.id`
    );
    await client.end();

    const total_factura = fac.rows[0].total_monto + 
    fac.rows[0].total_manejo_envio;

    Object.assign(req.data, { data: fac.rows[0], items: items.rows, manejo_envio: manejo_envio.rows[0], total_factura: total_factura });         
}
