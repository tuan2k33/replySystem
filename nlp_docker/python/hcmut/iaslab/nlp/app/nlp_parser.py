def parse_to_procedure(logical_tree):
    """
    Parse logical tree to procedure semantics
    ----------------------------------------------------------
    Args:
        logical_tree: nltk.tree.Tree created from nltk.parser.parser_one()
    """
    logical_expression = logical_tree.label()['SEM']
    gap = '?' + str(logical_tree.label()['GAP'])
    
    # Get the query type from the expression
    try:
        query_type = logical_expression.name
    except AttributeError:
        # Handle the case where it's an ApplicationExpression
        expr_str = str(logical_expression)
        if 'TIMEQUERY' in expr_str:
            # Extract source and destination from the expression
            src = expr_str.split("'")[1]  # Get 'HCMC'
            dest = expr_str.split("'")[3]  # Get 'NhaTrang'
            duration = expr_str.split("'")[5] if len(expr_str.split("'")) > 5 else '2:00HR'
            
            return {
                'query': gap,
                'type': 'duration',
                'source': src,
                'destination': dest,
                'duration': duration,
                'str': f"(DURATION {src} {dest})"
            }
        elif 'LISTQUERY' in expr_str:
            return {
                'query': gap,
                'type': 'list',
                'str': "(LIST-ALL-TOURS)"
            }
        elif 'COUNTQUERY' in expr_str:
            # Extract destination from the expression
            dest = expr_str.split("'")[1] if "'" in expr_str else "PhuQuoc"
            return {
                'query': gap,
                'type': 'count',
                'destination': dest,
                'str': f"(COUNT {dest})"
            }
        elif 'TRANSQUERY' in expr_str:
            # Extract destination from the expression
            dest = expr_str.split("'")[1] if "'" in expr_str else "NhaTrang"
            return {
                'query': gap,
                'type': 'transport',
                'destination': dest,
                'str': f"(TRANSPORT {dest})"
            }
        elif 'DATEQUERY' in expr_str:
            # Extract destination from the expression
            dest = expr_str.split("'")[1] if "'" in expr_str else "NhaTrang"
            return {
                'query': gap,
                'type': 'dates',
                'destination': dest,
                'str': f"(DATES {dest})"
            }

    if query_type == 'TIMEQUERY':
        # Handle time duration queries
        src, dest, duration = [str(arg) for arg in logical_expression.args]
        return {
            'query': gap,
            'type': 'duration',
            'source': src,
            'destination': dest,
            'duration': duration,
            'str': f"(DURATION {src} {dest})"
        }
    elif query_type == 'YESNOQUERY':
        # Handle listing queries
        return {
            'query': gap,
            'type': 'list',
            'str': "(LIST-ALL-TOURS)"
        }
    
    # ... rest of the function ...
    