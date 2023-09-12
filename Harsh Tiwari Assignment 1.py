# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uc9wrXGPRhKhIRoBMUuInhlM6kWKyEMF
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import roc_curve, roc_auc_score, auc

"""**TASK 1**"""

df = pd.read_csv("Dataset-Python.csv") #reading the data set into pandas data frame

print(df)

df = df.drop_duplicates() # Removed the duplicates if existing in the data set

df.dropna(inplace=True) # Removed the null values if existing in the data set

print(df[:10])

"""**TASK 2**"""

job_counts = df['job'].value_counts() # count the number of people in different job roles.
plt.figure(figsize=(8, 4))
job_counts.plot(kind='bar')
plt.title('Job Roles Distribution')
plt.xlabel('Job Role')
plt.ylabel('Count')
plt.show()

gender_counts = df['gender'].value_counts() # gender wise count
plt.figure(figsize=(8, 4))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Gender')
plt.axis('equal')
plt.show()

education_counts = df['education'].value_counts() # counts the people having different education level
plt.figure(figsize=(8, 4))
education_counts.plot(kind='bar')
plt.title('Education Level Distribution')
plt.xlabel('Education Levels')
plt.ylabel('Count')
plt.show()

english_speaker_counts = df['English speaker'].value_counts() # count of people speaking english and non english speakers
plt.figure(figsize=(8, 4))
plt.pie(english_speaker_counts, labels=english_speaker_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('English and Non-English Speakers')
plt.axis('equal')
plt.show()

jobRolePercentage = (df['job'].value_counts() / len(df)) * 100

educationPercentage = (df['education'].value_counts() / len(df)) * 100

genderPercentage = (df['gender'].value_counts() / len(df)) * 100

englishSpeakerPercentage = (df['English speaker'].value_counts() / len(df)) * 100

print(jobRolePercentage)

print(educationPercentage)

print(genderPercentage)

print(englishSpeakerPercentage)

"""**TASK 3**"""

gender_groups = df.groupby('gender') # groupby() function is used to group data by the gender and then find mean of education column
averageEducationOfGender = gender_groups['education'].mean()
print(averageEducationOfGender)

genderJobCounts = df.groupby(['gender', 'job']).size().unstack()
ax = genderJobCounts.plot(kind='bar', stacked=True, figsize=(8, 4))
plt.title('Distribution of Job Roles')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.legend(title='Job Roles', bbox_to_anchor=(1, 1), loc='upper left')
plt.show()

englishSpeakers = df[df['English speaker'] == 'yes']
nonEnglishSpeakers = df[df['English speaker'] == 'no']
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(12, 6))
axis1.hist(englishSpeakers['education'], bins=10, alpha=0.5, color='green')
axis1.set_title('Distribution of Education Levels Among English Speakers')
axis1.set_xlabel('Education Levels')
axis1.set_ylabel('Frequency')

axis2.hist(nonEnglishSpeakers['education'], bins=10, alpha=0.5, color='blue')
axis2.set_title('Distribution of Education Levels Among Non-English Speakers')
axis2.set_xlabel('Education Levels')
axis2.set_ylabel('Frequency')
plt.tight_layout()

plt.show()

english_speakers = df[df['English speaker'] == 'yes']
non_english_speakers = df[df['English speaker'] == 'no']
plt.figure(figsize=(8, 4))
plt.hist(english_speakers['education'],alpha=0.5, label='English Speakers', color='green')
plt.hist(non_english_speakers['education'],alpha=0.5, label='Non-English Speakers', color='blue')
plt.title('Distribution of Education Levels Among Different Language Speakers')
plt.xlabel('Education Levels')
plt.ylabel('Frequency')
plt.legend()
plt.show()

"""**TASK 4**"""

# Perform one-hot encoding for categorical variables
df_encoded = pd.get_dummies(df, columns=['job', 'education', 'gender', 'English speaker'])
print(df_encoded.head())

# Separating the features (X) and the target variable (y)
X = df_encoded.drop('gender_male', axis=1) # dropping gender_male column
X = X.drop('gender_female', axis=1) # dropping gender_female column
X = X.drop('Sno', axis=1) #And also dropping the Sno column
y = df_encoded['gender_male']
# Splitting the data set.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialzing the decision tree clasifier
clf = DecisionTreeClassifier(random_state=42)

# Train the classifier on the training data
clf.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_report_str = classification_report(y_test, y_pred)

# Print the evaluation results
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report_str)

feature_importance = clf.feature_importances_

# Creating a DataFrame to display feature names and their importance scores
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})

# Sorting feature importance in descneding order
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)


plt.figure(figsize=(8, 4))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
plt.xlabel('Importance Score')
plt.ylabel('Feature')
plt.title('Feature Importance for Gender Prediction (Decision Tree)')
plt.show()

# Display the sorted feature importance DataFrame
print("Feature Importance:\n", feature_importance_df)

y_pred_proba = clf.predict_proba(X_test)[:, 1]
# Calculate the ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
# Calculate the AUC score
roc_auc = auc(fpr, tpr)
# Plot the ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()


print("AUC Score:", roc_auc)

"""Summary:-
The model's performance and feature significance ratings provide insightful information about the gender prediction model's capabilities and underlying factors:-

Accuracy (0.74): The model's accuracy of 0.74 indicates that it correctly predicts the gender of approximately 74% of the dataset's individuals. This suggests that the model's predictive ability is adequate.

AUC Score (0.763): The AUC score of 0.763 for the ROC curve demonstrates that the model is reasonably effective at distinguishing between various gender groups. A greater AUC score indicates superior discrimination ability.

Importance of Features: The model's features have varying degrees of significance. Features with greater importance play a greater role in determining the gender accurately.

Insights Relating to Gender: The significance of particular characteristics may provide valuable gender-related insights. Features related to job roles, education levels, and English-speaking status are likely significant determinants of gender predictions.

The accuracy and AUC score of the model indicate its utility for gender prediction based on the provided features. It has multiple applications, including demographic analysis and targeted marketing.
"""