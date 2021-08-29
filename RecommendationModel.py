import pandas as pd
# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

# df = pd.read_csv('Papers data1.csv', encoding='cp1252')
from sqlalchemy import create_engine
con=create_engine("sqlite:///users.sqlite3").connect()
df=pd.read_sql_table("article",con)
df.abstract.head()
df.abstract.shape[0]


def recommendation_func(value1, v_indx=df.abstract.shape[0]):
    df1 = df.abstract.copy()
    df1[v_indx] = value1
    print(df1.shape, df.shape)
    # print(df1)

    # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')

    # Replace NaN with an empty string
    df1 = df1.fillna('')

    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(df1)

    # #Output the shape of tfidf_matrix
    print(tfidf_matrix.shape)

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    print(cosine_sim[v_indx].shape, cosine_sim[v_indx])

    dd1 = pd.Series(cosine_sim[v_indx])
    dd1 = dd1.sort_values(ascending=False)
    indx = dd1[1:11].index
    print(df.iloc[1])
    print("\nhello\n", df.loc[indx])
    return df.loc[indx]


value1 = '''
In this paper we consider the application of machine learning of graphical models and feature selection for developing better drug-design strategies. The work discussed in this paper is based on utilizing partial prior knowledge available through KEGG signalling pathway database in tan dim with our recent developed ensemble feature selection methods for a better regularisation of the lasso estimate. This work adds an extra layer of previously unseen knowledge in KEGG signalling pathways that embodies infering the underlying connectivity between gene-families implicated in breast cancer in MAPK-signalling pathway in response to application of anti-cancer drugs "neoadjuvant docetaxel".'''

l1 = recommendation_func(value1)
print(l1.title.values)
