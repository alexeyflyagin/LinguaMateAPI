def set_block_row_if(query, condition: bool):
    return query.with_for_update() if condition else query
