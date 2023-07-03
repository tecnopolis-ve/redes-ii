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

    let query_str = `select mse.nombre,
    to_char(mse.fecha, 'DD-MM-YYYY HH:MI:SS AM') fecha_evento,
    mse.id,
    concat(mse.horas, ' horas') horas,
    mse.tipo,
    mse.cancelado,
    mse.costo_ins_client,
    mse.costo_ins_general,
    mse.lugar_subasta,
    mse.nombre,
    (select count(id) from msi_subastarte_objetosubastaevento mso where mso.evento_id = mse.id) total_objetos,
    (select count(id) from msi_subastarte_objetosubastaevento mso where mso.evento_id = mse.id and mso.ganador_id is not null) total_objetos_vendidos,
    (select count(id) from msi_subastarte_participante msp where msp.evento_id = mse.id) total_participantes
    from msi_subastarte_organiza mso inner join msi_subastarte_evento mse 
    on mso.evento_id = mse.id 
    where mso.tienda_id =  ${req.data.tienda_id}`

    if (req.data.fecha_minima){
        query_str += ` and mse.fecha::date >= '${req.data.fecha_minima}'`
    }

    if (req.data.fecha_maxima){
        query_str += ` and mse.fecha::date <= '${req.data.fecha_maxima}'`
    }

    if (req.data.cancelado){
        query_str += ` and mse.cancelado = true`
    }

    if (req.data.tipo){
        const check = ["PRESENCIAL", "VIRTUAL"];
        if(check.includes(req.data.tipo)){
            query_str += ` and mse.tipo = '${req.data.tipo}'`
        }
    }

    const eventos = await client.query(
        query_str
    );

    await client.end()
    Object.assign(req.data, { eventos: eventos.rows, fecha_desde: req.data.fecha_minima, fecha_hasta: req.data.fecha_maxima });         
}
