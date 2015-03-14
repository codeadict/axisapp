/* Function to create the sub areas */
CREATE OR REPLACE FUNCTION generate_subareas(costumers_number INT, area_id INT) RETURNS void
AS $$
DECLARE
	rec RECORD;
	rec1 RECORD;
	areas_amount INT := 0;
	calculation_rest INT := 0;
	temp_clients_amount INT := 0;
	temp_presales_dist INT := 0;
	area RECORD;
BEGIN
    /* Get the area */
    SELECT * FROM base_area WHERE base_area.id = area_id INTO area;

    /* Get all the clients inside the area */
    SELECT COUNT(censo_cliente.partner_ptr_id) FROM censo_cliente
	WHERE ST_Contains(area.poligono, censo_cliente.geom) INTO temp_clients_amount;

    /* Divide the clients amount inside the area buy the costumers_number
       to get the number of sub areas to create */
    IF temp_clients_amount = 0 THEN
	/* Avoid the divide by cero */
	areas_amount := 1;
    ELSE
	areas_amount := temp_clients_amount / costumers_number;
    END IF;

    IF temp_clients_amount % costumers_number != 0 THEN
	areas_amount := areas_amount + 1;
    END IF;

    /* First delete the censo_presalesdistribution_clients */
    DELETE FROM censo_presalesdistribution_clients
	WHERE censo_presalesdistribution_clients.presalesdistribution_id IN
		(SELECT censo_presalesdistribution.id
			FROM censo_presalesdistribution
			WHERE ST_Contains(area.poligono, censo_presalesdistribution.polygon));

    /* Then delete all the rows inside the area especified */
    DELETE FROM censo_presalesdistribution
	WHERE ST_Contains(area.poligono, censo_presalesdistribution.polygon);

    /* I dont know why this must be execute */
    DROP TABLE IF EXISTS kmeans_table;

    /* Create kmeans table with client id, kmean group and point */
    CREATE TEMP TABLE kmeans_table AS (SELECT censo_cliente.partner_ptr_id as client_id, kmeans(ARRAY[ST_X(geom), ST_Y(geom)], areas_amount) OVER (), geom
                   FROM censo_cliente WHERE ST_X(geom) IS NOT NULL AND ST_Y(geom) IS NOT NULL
                   AND ST_Contains(area.poligono, censo_cliente.geom));

    /* Loop to create the presales_dist_table */
    FOR rec IN
	SELECT kmeans AS kmeans_group, count(*), ST_ConvexHull(ST_Collect(geom)) AS geom
	FROM kmeans_table
	GROUP BY kmeans_group
	ORDER BY kmeans_group
    LOOP
	INSERT INTO censo_presalesdistribution (name, polygon) VALUES (area.nombre || rec.kmeans_group, rec.geom::geometry);
	SELECT CURRVAL(pg_get_serial_sequence('censo_presalesdistribution', 'id')) INTO temp_presales_dist;

	FOR rec1 IN
		SELECT *
		FROM kmeans_table
		WHERE kmeans_table.kmeans = rec.kmeans_group
	LOOP
		RAISE NOTICE 'kmeans222 %s', rec1.kmeans || '///' || rec1.client_id || ']]';
		RAISE NOTICE 'presales_id222 %s', temp_presales_dist;

		INSERT INTO censo_presalesdistribution_clients (presalesdistribution_id, cliente_id)
			VALUES (temp_presales_dist, rec1.client_id);
	END LOOP;
    END LOOP;
END
$$ language 'plpgsql';