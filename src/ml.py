from utils import elastic_utils
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
REGION_KEYWORD = "REGIONCODE.keyword"


#TODO : complete this section with more details, precision/recall/ROC
#TODO : move to an other place
# TODO: randomise test set random.choices(res['adress'].split()) get on n_random
class Region(object):
    def __init__(self):
        self.region_code = elastic_utils.get_unique_value_field(REGION_KEYWORD)

    def train(self):
        self.trainning = {key : elastic_utils.get_all_hits_field_match(REGION_KEYWORD,key)for key in self.region_code}
        self.X = []
        self.y = []
        for train_ex in self.trainning:
            for item in self.trainning[train_ex]:
                self.y.append(train_ex)
                self.X.append(item['_source']['adress'])
        self.n_train = len(self.X)
        self.model = SVC(C=1.0)
        self.X_train = TfidfVectorizer().fit_transform(self.X)
        self.model.fit(self.X_train,self.y)
        print self.model.predict(self.X_train) == self.y



region = Region()
region.train()
print region.n_train






