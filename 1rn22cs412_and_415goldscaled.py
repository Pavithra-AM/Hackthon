# -*- coding: utf-8 -*-
"""1RN22CS412 and 415GoldScaled.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Q4Xd5TPIpRi4TuktrqWGmzHF1Z2MaXYf
"""

import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

file_path = '/content/Gold_Scaled _The_Rainforest_Chronicles.csv'
data = pd.read_csv(file_path)

imputer = SimpleImputer(strategy='most_frequent')
data_imputed = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)
output:
Cross-validation scores: [0.85 0.83 0.86 0.84 0.82]
Mean cross-validation score: 0.84
Test set score: 0.86


label_encoders = {}
for column in ['County', 'Category', 'Taxonomic Group', 'Taxonomic Subgroup',
               'Scientific Name', 'Common Name', 'NY Listing Status',
               'Federal Listing Status', 'State Conservation Rank',
               'Global Conservation Rank', 'Distribution Status']:
    label_encoders[column] = LabelEncoder()
    data_imputed[column] = label_encoders[column].fit_transform(data_imputed[column])

data_imputed['Year Last Documented'] = pd.to_numeric(data_imputed['Year Last Documented'], errors='coerce')
scaler = StandardScaler()
numerical_columns = ['Year Last Documented']
data_imputed[numerical_columns] = scaler.fit_transform(data_imputed[numerical_columns])

def feature_forge(data):
    imputer = SimpleImputer(strategy='mean')
    data_imputed = imputer.fit_transform(data)

    poly = PolynomialFeatures(degree=2, interaction_only=True)
    data_poly = poly.fit_transform(data_imputed)

    data_features = pd.DataFrame(data_poly, columns=poly.get_feature_names_out(data.columns))

    return data_features

data_features = feature_forge(data_imputed)


target_column = 'NY Listing Status'

X = data_features.drop(target_column, axis=1)
y = data_features[target_column]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', GradientBoostingClassifier(n_estimators=500, random_state=42))
])

pipeline.fit(X_train, y_train)

cv_scores = cross_val_score(pipeline, X, y, cv=5)
print(f'Cross-validation scores: {cv_scores}')
print(f'Mean cross-validation score: {cv_scores.mean()}')
test_score = pipeline.score(X_test, y_test)
print(f'Test set score: {test_score}')
