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
    const rs = await client.query(
        `select 
        ose.id,
        ose.bid,
        ose.pintura_id,
        ose.moneda_id,
        t.nombre nombre_tienda,
        t.email email_tienda,
        t.telefono telefono_tienda,
        pa.nombre pais_tienda,
        concat(c.nombre, ' ', c.segundo_nombre, ' ', c.apellido, ' ', c.segundo_apellido) nombre_coleccionista,
        concat(p.ancho, 'cm x ', p.alto, 'cm') dimensiones,
        p.nur nur_pintura,
        p.estilo, 
        p.titulo, 
        p.titulo_original, 
        p.anyo, 
        p.imagen_thumb pintura_thumb,
        m.nur nur_moneda,
        m.nombre,
        m.denominacion, 
        m.forma, 
        m.metal, 
        m.canto, 
        concat(m.diametro, ' mm') diametro, 
        concat(m.peso, ' g') peso, 
        m.anyo_emision, 
        m.org_acunyacion, 
        m.motivo, 
        m.anverso, 
        m.reverso, 
        m.total_mintage, 
        m.imagen_thumb moneda_thumb,
        m_div.nombre pais_divisa,
        pa_acu.nombre pais_acunyacion,
        to_char(e.fecha, 'DD-MM-YYYY') fecha_evento

        from msi_subastarte_objetosubastaevento ose
        inner join msi_subastarte_evento e
        on ose.evento_id = e.id
        inner join msi_subastarte_tienda t
        on ose.tienda_id = t.id
        inner join msi_subastarte_coleccionista c 
        on ose.ganador_id = c.user_id 
        left join msi_subastarte_pintura p 
        on ose.pintura_id = p.nur
        left join msi_subastarte_moneda m 
        on ose.moneda_id = m.nur
        left join msi_subastarte_pais pa
        on t.pais_id = pa.id
        left join msi_subastarte_pais pa_acu
        on m.pais_acunyacion_id = pa_acu.id
        left join msi_subastarte_divisa m_div
        on m.divisa_id = m_div.id
        where ose.id = ${req.data.ose_id}`
    );

    const artistas = await client.query(
        `select concat(msa2.nombre, ' ', msa2.apellido) nombre_artista, 
        msa2.nombre_artistico from 
        msi_subastarte_artistapintura msa 
        inner join msi_subastarte_artista msa2 
        on msa.artista_id = msa2.id
        where msa.pintura_id = ${rs.rows[0].pintura_id}
        order by msa2.nombre`
    )

    await client.end()
    Object.assign(req.data, { data: rs.rows[0], artistas: artistas.rows });         
}
