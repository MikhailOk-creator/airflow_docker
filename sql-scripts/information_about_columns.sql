SELECT
    table_schema,
    column_name,
    ordinal_position,
    is_nullable,
    data_type,
    is_identity,
    identity_generation,
    identity_start,
    identity_increment,
    identity_maximum,
    identity_minimum,
    identity_cycle,
    is_updatable
FROM
    information_schema.columns
WHERE
    table_name = '%s';