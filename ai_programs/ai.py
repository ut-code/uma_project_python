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
    def __init__(self):
        pass
    def createModel(self):
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

        data = self.load_data(os.path.join(parent_dir, "db\jra\datafile-seiseki-g1-afs-result-afs2023.html.json"))
        x, y = self.preprocess_data(pd.DataFrame(data), data)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        model = self.build_model(x_train.shape[1])
        model.fit(x_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

        predictions = model.predict(x_test)

        for i in range(len(predictions)):
            print(f"予測: {predictions[i]}, 実際: {y_test[i]}")
    def load_data(self, json_file: str):
        with open(json_file, "r", encoding="UTF-8") as f:
            return json.loads(f.read())
    def preprocess_data(self, df, data):
        horses = pd.DataFrame(data["horse"])
        horse_infos = horses[["rank", "umaban", "horse", "age", "weight", "jockey", "time", "h_weight", "f_time", "pop"]].copy()

        horse_infos["time"] = horse_infos["time"].apply(self.convert_time_to_seconds)

        for column in ["horse", "age", "jockey", "pop"]:
            horse_infos[column] = self.LabelEncode(horse_infos[column])

        horse_infos["weight"] = horse_infos["weight"].astype(float)
        horse_infos["h_weight"] = horse_infos["h_weight"].astype(float)
        horse_infos["f_time"] = horse_infos["f_time"].astype(float)

        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(horse_infos)

        return features_scaled, self.LabelEncode(df["title"])
    def convert_time_to_seconds(self, time_str):
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
 