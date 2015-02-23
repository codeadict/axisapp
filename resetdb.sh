#!/bin/sh
psql -h localhost -U postgres -c "DROP DATABASE axisapp"
psql -h localhost -U postgres -c "CREATE DATABASE axisapp"
psql -h localhost -U postgres -d 'censo_clientes' -c "CREATE EXTENSION postgis;"
psql -h localhost -U postgres -d 'censo_clientes' -c "CREATE EXTENSION postgis_topology;"