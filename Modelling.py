
# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("all_mixes.csv")
sns.set_theme(style="darkgrid", palette="Paired")

# %%
df['name_cat'] = df['name'].astype('category').cat.codes

# %%
from statsmodels.formula.api import mnlogit  # use this for multinomial logit in statsmodels library, instead of glm for binomial.
# Sample use/syntax:
# model = mnlogit(formula, data)
modelLogit = mnlogit(formula =  'name_cat ~ danceability + loudness + valence + duration_ms + artist_pop + C(mode)+ release_year', data=df)
modelLogitFit = modelLogit.fit()
print( modelLogitFit.summary() )

# %%
yDf = df[['name_cat']]
xDf = df[['danceability', 'energy', 'loudness', 'speechiness' , 'instrumentalness' , 'liveness', 'valence', 'tempo' , 'duration_ms' , 'artist_pop',  'mode' , 'release_year']]

from sklearn.model_selection import train_test_split

X_train1, X_test1, y_train1, y_test1 = train_test_split(xDf, yDf, test_size = 0.33, random_state=12)

#%%
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=3) # instantiate with n value given
knn.fit(X_train1, y_train1)
ytest_pred = knn.predict(X_test1)
ytest_pred
print('3-NN model accuracy (with the test set):', knn.score(X_test1, y_test1))
print('3-NN model accuracy (with the train set):', knn.score(X_train1, y_train1))

# %%
import numpy as np
from sklearn.model_selection import cross_val_score
cv_results = cross_val_score(knn, xDf, yDf, cv=10)
print(cv_results) 
print('3-NN model cross validation results:',np.mean(cv_results)) 

# %%
