sql_create_tasks_table = """ CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name varchar(255) NOT NULL,
                                    begin_date datetime,
                                    end_date datetime IS NULL
                                ); """

sql_create_datas_table = """ CREATE TABLE IF NOT EXISTS data (
                                    id integer PRIMARY KEY,
                                    task_id integer NOT NULL,
                                    measurment varchar(255),
                                    created_at datetime,
                                    FOREIGN KEY (task_id) REFERENCES tasks (id)
                                ); """

sql_instert_task = """INSERT INTO tasks(name,begin_date,end_date) VALUES(?,?,?) """
sql_instert_data = """INSERT INTO tasks(task_id,measurment,end_date) VALUES(?,?,?) """

