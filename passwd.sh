#!/bin/bash
sudo docker exec -it airflow bash -lc "cat /opt/airflow/standalone_admin_password.txt"
