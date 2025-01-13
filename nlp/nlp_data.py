raw_database = [
    # Tour definitions
    "(TOUR PQ Phú_Quốc)",
    "(TOUR DN Đà_Nẵng)",
    "(TOUR NT Nha_Trang)",
    
    # Tour schedules
    "(DTIME PQ HCMC \"7AM 1/7\")",
    "(ATIME PQ PQ \"9AM 1/7\")",
    "(DTIME PQ HCMC \"8AM 5/7\")",
    "(ATIME PQ PQ \"10AM 5/7\")",
    
    "(DTIME DN HCMC \"7AM 1/7\")",
    "(ATIME DN DN \"9AM 1/7\")",
    "(DTIME DN HCMC \"7AM 4/7\")",
    "(ATIME DN DN \"9AM 4/7\")",
    
    "(DTIME NT HCMC \"7AM 1/7\")",
    "(ATIME NT NT \"12AM 1/7\")",
    "(DTIME NT HCMC \"7AM 5/7\")",
    "(ATIME NT NT \"12AM 5/7\")",
    
    # Duration information
    "(RUN-TIME PQ HCMC PQ \"2:00 HR\")",
    "(RUN-TIME DN HCMC DN \"2:00 HR\")",
    "(RUN-TIME NT HCMC NT \"5:00 HR\")",
    
    # Transportation modes
    "(BY PQ airplane)",
    "(BY DN airplane)",
    "(BY NT train)"
]

def categorize_database(database):
    """
    Categorize raw database to collections of FLIGHT, ATIME and DTIME
    ----------------------------------------------------------------
    Args:
        database: raw database from assignments (List of string values)
    """
    #Remove ( )
    flights = [data.replace('(','').replace(')','') for data in database if 'FLIGHT' in data]
    arrival_times = [data.replace('(','').replace(')','') for data in database if 'ATIME' in data]
    departure_times = [data.replace('(','').replace(')','') for data in database if 'DTIME' in data]
    return {'flights': flights, 
            'arrival':arrival_times, 
            'departure':departure_times}

def retrieve_result(semantics):
    """
    Retrieve result list from procedure semantics
    ---------------------------------------------
    Args:
        semantics: dictionary created from nlp_parser.parse_to_procedure()
    """
    procedure_semantics = semantics
    
    if procedure_semantics.get('type') == 'transport':
        destination = procedure_semantics['destination']
        # Create a mapping for city codes
        city_codes = {
            'PhuQuoc': 'PQ',
            'DaNang': 'DN',
            'NhaTrang': 'NT'
        }
        dest_code = city_codes.get(destination)
        
        if dest_code:
            # Find transportation mode in raw_database
            for entry in raw_database:
                if entry.startswith('(BY') and entry.split()[1] == dest_code:
                    # Extract the mode of transportation
                    mode = entry.split()[2].strip(')')
                    return [mode]
        return ['No transportation mode found']
    
    if procedure_semantics.get('type') == 'count':
        destination = procedure_semantics['destination']
        # Create a mapping for city codes
        city_codes = {
            'PhuQuoc': 'PQ',
            'DaNang': 'DN',
            'NhaTrang': 'NT'
        }
        dest_code = city_codes.get(destination)
        
        if dest_code:
            # Count DTIME entries for the specified destination
            count = sum(1 for entry in raw_database 
                       if entry.startswith('(DTIME') and 
                       entry.split()[1] == dest_code)
            return [str(count)]
        return ['0']
    
    elif procedure_semantics.get('type') == 'list':
        result = []
        # Get all DTIME entries
        for dtime in raw_database:
            if dtime.startswith('(DTIME'):
                d_parts = dtime.split()
                dest = d_parts[1]  # Get destination code (DN, NT, PQ)
                time = d_parts[4]  # Get time
                
                # Find matching ATIME
                for atime in raw_database:
                    if (atime.startswith('(ATIME') and 
                        atime.split()[1] == dest and 
                        atime.split()[4] == time):
                        result.append(f"{dtime} {atime}\n")
                        break
        
        # Sort by destination code and time
        result.sort(key=lambda x: (x.split()[1], x.split()[4]))
        return result
    
    elif procedure_semantics.get('type') == 'duration':
        source = procedure_semantics['source']
        destination = procedure_semantics['destination']
        
        # Create a mapping for city codes
        city_codes = {
            'HCMC': 'HCMC',
            'DaNang': 'DN',
            'NhaTrang': 'NT',
            'PhuQuoc': 'PQ'
        }
        
        # Convert city names to codes
        dest_code = city_codes.get(destination)
        
        # Look for duration in raw_database
        for entry in raw_database:
            if entry.startswith('(RUN-TIME'):
                parts = entry.strip('()').split('"')
                route_parts = parts[0].split()
                duration = parts[1] if len(parts) > 1 else "2:00 HR"
                
                if source in route_parts and dest_code in route_parts:
                    return [duration.strip()]
                    
        return ["2:00 HR"]
    
    elif procedure_semantics.get('type') == 'dates':
        destination = procedure_semantics['destination']
        # Create a mapping for city codes
        city_codes = {
            'PhuQuoc': 'PQ',
            'DaNang': 'DN',
            'NhaTrang': 'NT'
        }
        dest_code = city_codes.get(destination)
        
        if dest_code:
            # Find all departure dates for the destination
            dates = []
            for entry in raw_database:
                if entry.startswith('(DTIME') and entry.split()[1] == dest_code:
                    # Extract the date (last part in quotes, remove quotes and get date part)
                    date = entry.split('"')[1].split()[1]
                    dates.append(date)
            # Sort dates and remove duplicates
            dates = sorted(set(dates))
            return dates if dates else ['No available dates found']
        return ['No available dates found']
    
    # Original flight query logic
    query = procedure_semantics['query']
    result_type = 'flight'
    
    for arg in list(procedure_semantics.keys()):
        if '?' in procedure_semantics[arg] and procedure_semantics[arg] != query:
            procedure_semantics[arg] = ''
        elif procedure_semantics[arg] == query and arg != 'query':
            procedure_semantics[arg] = ''
            result_type = arg
                 
    #Iterate after FLIGHT, ATIME and DTIME to have result
    flight_check_result = [f.split()[1] for f in database['flights'] if procedure_semantics['flight'] in f] # type: ignore

    arrival_flight_result = [a.split()[1] for a in database['arrival'] # type: ignore
                            if procedure_semantics['arrival_location'] in a
                            and procedure_semantics['arrival_time'] in a
                            and a.split()[1] in flight_check_result]

    departure_flight_result = [d.split()[1] for d in database['departure']  # type: ignore
                              if procedure_semantics['departure_location'] in d
                              and procedure_semantics['departure_time'] in d
                              and d.split()[1] in arrival_flight_result]

    if result_type == 'flight':
        result = departure_flight_result
    elif result_type == 'arrival_time':
        result = [a.split()[3] for a in database['arrival'] if a.split()[1] in departure_flight_result] # type: ignore
    else:
        result = [d.split()[3] for d in database['departure'] if d.split()[1] in departure_flight_result] # type: ignore
    return result