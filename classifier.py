import pickle
from typing import List, Dict
import nltk
import numpy as np
from scipy.sparse import hstack


def load_model(path: str):
    with open(path, 'rb') as f:
        return pickle.load(f)


class Classifier:
    def __init__(self):
        nltk.download('wordnet')
        np.random.seed(42)
        self.lemmatizer = nltk.WordNetLemmatizer()
        self.random_forest = load_model('models/random_forest.sav')
        self.tfidf = load_model('models/tfidf.sav')

    def predict_all(self, data: List) -> Dict[str, str]:
        label_dict = {0: 'Large', 1: 'Medium', 2: 'X-Small'}
        data_matrix = self._prepare_data(data)
        y_pred = self.random_forest.predict(data_matrix)
        task_wh_pair = {}
        for i, pred_label in enumerate(y_pred):
            task_wh_pair[data[i].task_id] = label_dict.get(pred_label)
        return task_wh_pair

    def _prepare_data(self, data: List):
        data_lol = []
        tenant_list = []
        task_id_list = []
        for item in data:
            data_lol.append([item.duration, item.number_of_campaigns, item.number_of_customers])
            tenant_list.append(self._process_text_row(item.tenant_name))
            task_id_list.append(self._process_text_row(item.task_id))

        np_arr = np.array(data_lol)
        tenant_vectors = self.tfidf.transform(tenant_list)
        task_id_vectors = self.tfidf.transform(task_id_list)
        return hstack((np_arr, tenant_vectors, task_id_vectors)).tocsr()

    def _process_text_row(self, text: str) -> str:
        text = text.lower()
        text_list = text.split("_")
        final_text = " ".join([self.lemmatizer.lemmatize(t) for t in text_list])
        return final_text.strip()
