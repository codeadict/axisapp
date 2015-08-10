def get_client_visits(client):
    """
    Gets a list of visits for some client.
    :param client: Client model instance
    :return: Visits model queryset
    """
    return client.visits.all()


def add_visit_to_client(client, visit):
    """
    Registers a visit to a client.
    :param client: Client model instance
    :param visit: Visits model instance
    :return:
    """
    client.visits.add(visit)


def remove_visit_from_client(client, visit):
    """
    Removes a Visit from a Client
    :param client: Client model instance
    :param visit: Client model instance
    :return:
    """
    client.visits.remove(visit)
