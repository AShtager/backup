import json
import requests
import tqdm


class VKUser:

    url_base_vk = "https://api.vk.com/method/"

    def __init__(self):
        self.id_user = input("Введите Ваш id: ")
        self.vk_token = input("Введите Ваш токен вк: ")

    def _user_photos_get(self):
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
        all_data_photos = self._user_photos_get()
        info_photos = {}

        for photos_particulars in all_data_photos["response"]["items"]:
            if photos_particulars["likes"]["count"] not in info_photos:
                dict_info = {
                    photos_particulars["likes"]["count"]: {
                        "size": f"{photos_particulars['sizes'][-1]['type']}",
                        "url": f"{photos_particulars['sizes'][-1]['url']}"}
                }
                info_photos.update(dict_info)
            else:
                dict_info = {
                    str(photos_particulars["likes"]["count"]) + str(photos_particulars["date"]): {
                        "size": f"{photos_particulars['sizes'][-1]['type']}",
                        "url": f"{photos_particulars['sizes'][-1]['url']}"}
                }
                info_photos.update(dict_info)
        return info_photos


class YanDiscUser(VKUser):

    url_base = "https://cloud-api.yandex.net"

    def _user_name_photos(self):
        all_data_photos = self._user_photo_info()
        name_photos = []

        for k, v in all_data_photos.items():
            name_photo = {"file_name": f"{k}.jpg", "size": v['size']}
            name_photos.append(name_photo)

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(name_photos, file)

    def loanding_photo(self):
        self._user_name_photos()
        info_photo = self._user_photo_info()
        self.name_folder = input("Введите название папки: ")

        url_create_folder = f"{self.url_base}/v1/disk/resources"
        url_loading = f"{self.url_base}/v1/disk/resources/upload"
        params = {"path": self.name_folder}
        headers = {"Authorization": f"OAuth {input("Введите ваш токен Яндекс диска: ")}"}
        requests.put(url_create_folder, params=params, headers=headers)
        
        for name, info in tqdm.tqdm(info_photo.items()):
            params_loand = {
                "path": f"{self.name_folder}/{name}.jpg",
                "url": info["url"]
            }
            requests.post(url_loading, params=params_loand, headers=headers)
        return f"Фотографии загружены"
            

user_1 = YanDiscUser()
print(user_1.loanding_photo())
