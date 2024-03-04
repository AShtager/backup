import json
import requests
import tqdm
from operator import itemgetter


class VKUser:
    """
    запрашиваем id и token пользователя вк 
    """
    url_base_vk = "https://api.vk.com/method/"

    def __init__(self):
        self.id_user = input("Введите Ваш id: ")
        self.vk_token = input("Введите Ваш токен вк: ")

    def _user_photos_get(self):
        """
        API метод вк, функция вернет json файл с информацией по фотографиям
        """
        name_method = "photos.get"
        url_method_api = self.url_base_vk + name_method
        params = {
            "access_token": self.vk_token,
            "owner_id": self.id_user,
            "album_id": "profile",
            "extended": 1,
            "count": 5,
            "v": 5.199
        }
        response = requests.get(url_method_api, params=params)
        return response.json()

    def _user_photo_info(self):
        """
        сохраням информацию фотографий пользователя в словаря ключ количество лайков, 
        значение словарь со значениями: размер и url
        """
        all_data_photos = self._user_photos_get()
        info_photos = {}

        for photos_particulars in all_data_photos["response"]["items"]:
            sorted_size_all = sorted(photos_particulars["sizes"], key=itemgetter("height"))
            if photos_particulars["likes"]["count"] not in info_photos:
                dict_info = {
                    photos_particulars["likes"]["count"]: {
                        "size": f"{sorted_size_all[-1]['type']}",
                        "url": f"{sorted_size_all[-1]['url']}"}
                }
                info_photos.update(dict_info)
            else:
                dict_info = {
                    str(photos_particulars["likes"]["count"]) + str(photos_particulars["date"]): {
                        "size": f"{sorted_size_all[-1]['type']}",
                        "url": f"{sorted_size_all[-1]['url']}"}
                    }
                info_photos.update(dict_info)
        return info_photos


class YanDiscUser(VKUser):
    """
    взаимодействует с родительским классом, загружаем фотографии пользователя на яндекс диск.
    пример использования:
    user_1 = YanDiscUser()
    user_1.loanding_photo()
    """
    url_base = "https://cloud-api.yandex.net"

    def _user_name_photos(self):
        """
        сохраняем информацию по загруженным фотографиям в json файл
        """
        all_data_photos = self._user_photo_info()
        name_photos = []

        for k, v in all_data_photos.items():
            name_photo = {"file_name": f"{k}.jpg", "size": v['size']}
            name_photos.append(name_photo)

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(name_photos, file)

    def loanding_photo(self):
        """
        загружаем фотографии пользователя на его яндекс диск
        """
        self._user_name_photos()
        info_photo = self._user_photo_info()
        self.name_folder = input("Введите название папки: ")

        url_create_folder = f"{self.url_base}/v1/disk/resources"
        url_loading = f"{self.url_base}/v1/disk/resources/upload"
        params = {"path": self.name_folder}
        headers = {"Authorization": f"OAuth {input('Введите Ваш токен Яндекс диска: ')}"}
        requests.put(url_create_folder, params=params, headers=headers)
        
        for name, info in tqdm.tqdm(info_photo.items()):
            params_loand = {
                "path": f"{self.name_folder}/{name}.jpg",
                "url": info["url"]
            }
            requests.post(url_loading, params=params_loand, headers=headers)
        return 
            

user_1 = YanDiscUser()
user_1.loanding_photo()