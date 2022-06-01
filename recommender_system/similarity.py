from sklearn.metrics.pairwise import cosine_similarity


def items_rating(events):
    data = {}
    for event in events:
        user_id = event['user_id']
        item_id = event['item_id']
        rating = event['rating']
        try:
            data[item_id][user_id] = rating
        except:
            data[item_id] = {}
            data[item_id][user_id] = rating

    return data

def users_rating(events):
    data = {}
    for event in events:
        user_id = event['user_id']
        item_id = event['item_id']
        try:
            data[user_id].append(item_id)
        except:
            data[user_id] = []
            data[user_id].append(item_id)

    return data

def combinations(items, users):
    combinations = []
    for item_key, item_value in items.items():
        temp = []
        for user_id, rating in item_value.items():

            if item_key in users[user_id]:
                temp.extend(users[user_id])

        temp = list(set(temp))
        temp.remove(item_key)
        temp = [(item_key, x) for x in temp]
        combinations.extend(temp)

    return combinations


def items_cosine_similarity_calculation(data, combinations):
    similarity_dicts = []
    for pair in combinations:
        item_1 = pair[0]
        item_2 = pair[1]
        vector_1 = [data[item_1][x] for x in data[item_1] if x in data[item_2]]
        vector_2 = [data[item_2][x] for x in data[item_2] if x in data[item_1]]
        if len(vector_1) > 1 and len(vector_2) > 1:
            similarity = cosine_similarity([vector_1], [vector_2])
            similarity_dict = {'item_1': item_1, 'item_2': item_2, 'similarity': similarity.item()}
            similarity_dicts.append(similarity_dict)

    return similarity_dicts

