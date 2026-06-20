from tensorflow.keras.models import Model
from tensorflow import keras
from utils.utils import read_yaml
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class BaseModel:

    def __init__(self,config_path):
        try:
            self.config = read_yaml(config_path)
            logger.info("Loaded configuration from config.yaml")
        except Exception as e:
            raise CustomException("Error loading configuration", e)
        
    def RecommenderNet(self, n_users, n_anime):
        "Recommender network architecture"
        try:
            embedding_size = self.config["model"]["embedding_size"]

            user = keras.layers.Input(name="user",shape=(1,))
            anime = keras.layers.Input(name="anime",shape=(1,))

            user_embedding = keras.layers.Embedding(name="user_embedding", input_dim=n_users, output_dim=embedding_size)(user)
            anime_embedding = keras.layers.Embedding(name="anime_embedding", input_dim=n_anime, output_dim=embedding_size)(anime)

            user_vec = keras.layers.Flatten()(user_embedding)
            anime_vec = keras.layers.Flatten()(anime_embedding)

            x = keras.layers.Concatenate()([user_vec, anime_vec])
            x = keras.layers.Dense(256, activation='relu')(x)
            x = keras.layers.BatchNormalization()(x)
            x = keras.layers.Dropout(0.3)(x)
            x = keras.layers.Dense(128, activation='relu')(x)
            x = keras.layers.Dropout(0.3)(x)

            output = keras.layers.Dense(1, activation='sigmoid')(x)

            model = Model(inputs=[user,anime], outputs=output)
            model.compile(
                loss = self.config["model"]["loss"],
                optimizer = self.config["model"]["optimizer"],
                metrics = self.config["model"]["metrics"]
            )

            logger.info("Model created sucesfully....")

            return model
        except Exception as e:
            logger.error(f"Error occurfed during model architecture {e}")
            raise CustomException("Failed to create model",e)

