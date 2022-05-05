from models import db, User, Characters, Characters_Fav, Planets, Planets_Fav, Ships, Ships_Fav
def get_user_favorites(uid, List_Fav, name_of_item_id, List):
    all_favorite = List_Fav.query.all()
    all_favorite = list(map(lambda x: x.serialize(), all_favorite))
    all_favorite_from_user = list(filter(lambda x: x["id_user"] == uid, all_favorite))
    id_all_favorite_from_user = [x[name_of_item_id] for x in all_favorite_from_user]
    
    all_items = List.query.all()
    all_items = list(map(lambda x: x.serialize(), all_items))
    
    result = []
    for item in all_items:
        if item["id"] in id_all_favorite_from_user:
            result.append(item)

   
    return result