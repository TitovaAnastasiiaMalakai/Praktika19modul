import os
from api import PetFriends
from settings import valid_email, valid_password
from tests import images

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_create_pet_simple(name='dark', animal_type='sova', age='3'):
    """Проверяем возможность добавления питомца без фото /api/create_pet_simple"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['pet_photo'] == ""


def test_successful_add_new_pet_no_photo(email=valid_email, password=valid_password):
    """Проверяем, что успешно добавили нового питомца"""
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.add_pet_no_photo(auth_key, name='dark', animal_type='sova', age='3')
    assert status == 200
    assert result['name'] == 'dark'

def test_successful_add_pet_photo(email=valid_email, password=valid_password):
    """Проверяем, что успешно добавили фото питомца"""
    _, auth_key = pf.get_api_key(email, password)
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = result['pets'][0]['id']
    pet_photo = 'images/sova.jpeg'
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] is not None
    assert 'jpeg' in result['pet_photo']

def test_delete_all_pets():
    """Проверяем возможность удаления всех своих питомцев"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    while len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
    print("питомцев нет")




