import datetime
from gramps.gen.lib import EventType


def completeness_calculator(database, person):
    filled_fields = 0

    # name checking
    name = person.get_primary_name()
    first = name.get_first_name().strip()
    surnames = [s.get_surname().strip() for s in name.get_surname_list()]
    if first or any(surnames):
        filled_fields += 1

    # birth date checking
    birth_ref = person.get_birth_ref()
    if birth_ref:
        birth_event = database.get_event_from_handle(birth_ref.ref)
        if not birth_event.get_date_object().is_empty():
            filled_fields += 1

    # death date checking
    death_ref = person.get_death_ref()
    if death_ref:
        death_event = database.get_event_from_handle(death_ref.ref)
        if not death_event.get_date_object().is_empty():
            filled_fields += 1
    else:
        filled_fields += 1  

    # multimedia checking
    if person.get_media_list():
        filled_fields += 1

    # events checking 
    for event_ref in person.get_event_ref_list():
        event = database.get_event_from_handle(event_ref.ref)
        if event.get_type() not in (EventType.BIRTH, EventType.DEATH):
            filled_fields += 1
            break

    coefficient = 20 # (for each of the five fields worth is 20% (20% * 5 = 100%))
    return filled_fields * coefficient


def people_collector(database): 
    today = datetime.date.today()
    result = []

    for handle in database.get_person_handles():
        person = database.get_person_from_handle(handle)

        birth_ref = person.get_birth_ref()
        if not birth_ref:
            continue
        birth_event = database.get_event_from_handle(birth_ref.ref)
        birth_date = birth_event.get_date_object()
        if birth_date.is_empty():
            continue

        birth_year = birth_date.get_year()
        birth_month = birth_date.get_month() or 1
        birth_day = birth_date.get_day() or 1

        death_ref = person.get_death_ref()
        is_alive = death_ref is None

        if is_alive:
            age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
        else:
            death_event = database.get_event_from_handle(death_ref.ref)
            death_date = death_event.get_date_object()
            if death_date.is_empty():
                continue
            death_year = death_date.get_year()
            death_month = death_date.get_month() or 1
            death_day = death_date.get_day() or 1
            age = death_year - birth_year - ((death_month, death_day) < (birth_month, birth_day))


        profile_completeness = completeness_calculator(database, person)
        birth_key = birth_year * 10000 + birth_month * 100 + birth_day
        result.append((birth_key, age, is_alive, profile_completeness))

    result.sort(reverse=True)
    return result