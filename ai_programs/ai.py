import os
import json

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

class AiClient:
    version: str
    parent_dir: str

    def __init__(self, version: str):
        self.version = version
        self.parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    def load_model(self):
        model_path = os.path.join(self.parent_dir, f"model/{self.version}/model.keras")
        return tf.keras.models.load_model(model_path)
    def format_data(self, datas):
        result = []
        for data in datas:
            result.append(data[0])
        return result
    def prediction_rank(self, datas):
        model = self.load_model()
        all_data = []
        result = {}

        for data in datas["horse"]:
            data["title"] = datas["title"]
            all_data.append(data)

        combined_data = pd.concat([pd.DataFrame(data) for data in all_data], ignore_index=True)

        features_scaled, _ = self.preprocess_data(combined_data)

        predictions = model.predict(features_scaled)

        combined_data["predicted_rank"] = predictions.flatten()
        combined_data["predicted_rank"] = combined_data["predicted_rank"].rank(method="min", ascending=True)

        for _, row in combined_data.iterrows():
            horse = row["horse"]
            rank = int(row["predicted_rank"])
            result[horse] = rank

        return result
    def createModel(self):
        files = os.listdir(os.path.join(self.parent_dir, "db\jra\\"))
        jsons = self.preprocess_jsons(files)
        combined_data = pd.concat([pd.DataFrame(data) for data in jsons], ignore_index=True)
        x, y = self.preprocess_data(combined_data)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        model = self.build_model(x_train.shape[1])
        model.fit(x_train, y_train, epochs=250, batch_size=32, validation_split=0.2, shuffle="batch")

        predictions = model.predict(x_test)

        for i in range(len(predictions)):
            print(f"予測: {round(int(predictions[i][0]))}, 実際: {int(y_test.flatten()[i])}")

        model.save(os.path.join(self.parent_dir, f"model/{self.version}/model.keras"))
        model.save(os.path.join(self.parent_dir, f"model/{self.version}/model.h5"))
    def preprocess_jsons(self, jsons: list[str]):
        all_data = []
        for json_data in jsons:
            datas = self.load_data(os.path.join(self.parent_dir, f"db\jra\{json_data}"))
            for data in datas["horse"]:
                data["title"] = datas["title"]
                all_data.append(data)

        return all_data
    def preprocess_data(self, data: pd.DataFrame):
        horse_data = {}

        horse_infos = data.copy()
        horse_infos["time"] = horse_infos["time"].apply(self.convert_time_to_seconds)
        horse_info_list = ["horse", "age", "jockey", "pop", "title", "weight", "h_weight", "f_time"]

        for column in ["horse", "age", "jockey", "pop", "title"]:
            horse_infos[column] = self.LabelEncode(horse_infos[column])

        horse_infos["weight"] = horse_infos["weight"].astype(float)
        horse_infos["h_weight"] = horse_infos["h_weight"].astype(float)
        horse_infos["f_time"] = horse_infos["f_time"].astype(float)

        for column in horse_info_list:
            horse_infos[column].dropna(inplace=True)

        for column in horse_info_list:
            horse_data[column] = horse_infos[column]

        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(pd.DataFrame(horse_data))

        return features_scaled, horse_infos["rank"].astype(float).values if "rank" in horse_infos else None
    def load_data(self, file_path: str):
        with open(file_path, "r", encoding="UTF-8") as f:
            return json.loads(f.read())
    def convert_time_to_seconds(self, time_str: str):
        minutes, seconds = map(float, time_str.split(":"))
        return minutes * 60 + seconds
    def LabelEncode(self, series):
        le = LabelEncoder()
        return le.fit_transform(series)
    def build_model(self, input_shape):
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(input_shape,)),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1),  # 回帰問題の場合は必須
        ])
        model.compile(optimizer="adam", loss="mean_squared_error")
        return model
