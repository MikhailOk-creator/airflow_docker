select *
from
    information_schema.table_constraints tc,
    information_schema.key_column_usage kc
where
    tc.table_name  = '%s'
    and kc.table_name = tc.table_name and kc.table_schema = tc.table_schema
    and kc.constraint_name = tc.constraint_name