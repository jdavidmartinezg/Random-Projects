# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:45:38 2020

@author: Juan David Martinez Gordillo
"""

import pyforest # imports data science libraries on-demand
from scipy import sparse # Deal with sparse ratings matrix
from sklearn.metrics.pairwise import cosine_similarity
import os




# ............ DATA LOAD ......................................................

ratings = pd.read_csv("ratings.csv",
                      dtype = {'quiz_type':'category'})
# Check column types
ratings.dtypes

# Subset dataframe to create user-item matrix

ratings_s = ratings[['user_id','question_number','item_id','rating']]

ratings_s['counter'] = 1


# ............ SANITY CHECKS ..................................................

# Are there items that are presented more than once to a user?

item_count_peruser = ratings_s.groupby(['user_id', 'item_id'], 
                           as_index = False).agg({'counter':'sum'})

pd.crosstab(index = item_count_peruser['counter'], columns =  'Freq')

# There are several cases (12,962) in which the user has been presented a repeated item


# I assume the likes of a user are static, hence, I will take only one rating for each item
# Also, I will take the last item rating as it is the most recent record


# Keep only last item rating recorded for every user and ever item

ratings_s_striped = ratings_s.sort_values('question_number', 
                        ascending = False).drop_duplicates(['user_id', 'item_id'],keep='first')

                                                           
ratings_clean = ratings_s_striped[['user_id','item_id','rating']]


# Create ratings matrix

ratings_matrix = ratings_clean.pivot(index='user_id', columns='item_id', values='rating')

ratings_matrix.shape
# There are 20000 users and 5000 items


# How sparse is the matrix?

np.isnan(np.array(ratings_matrix)).sum()/np.prod(np.array(ratings_matrix).shape)
# The sparsity of 98.89%




# Encode the ratings as: 1:like, -1:dislike, 0:norating

# Replace 0 by -1

ratings_matrix = ratings_matrix.replace(0, -1)

# Replace nan by 0

ratings_matrix = ratings_matrix.fillna(0)




# ............ SIMPLE RECOMMENDER .............................................



class Recommender:

    def __init__(self, ratings_mat):
        """     

        Parameters
        ----------
        ratings_mat : Pandas dataframe 
            Dataframe with users in the index and items in the columns. The values
            in each cell correspond to the ratings.

        Returns
        -------
        None.

        """
        self.ratings_mat = ratings_mat
        self.sim_matrix  = self.__Similarity()
        
    # ............ ITEM-ITEM CALCULATIONS .....................................
    
    # Cosine similarity:
    def __Similarity(self):
        """
        
        Column-wise cosine similarity for a sparse matrix.

        Returns
        -------
        sim_matrix : Pandas dataframe
            Item-Item cosine similarity matrix.

        """
            
        data_sparse = sparse.csr_matrix(self.ratings_mat)
        similarities = cosine_similarity(data_sparse.transpose())
        sim_matrix = pd.DataFrame(data=similarities, index= self.ratings_mat.columns, columns= self.ratings_mat.columns)
        # np.fill_diagonal(sim_matrix.values, np.nan) # Information in diagonal its just ones
        return sim_matrix

    # Build the similarity matrix
    # item_sim_matrix = Similarity()  

    def ItemBasedRecommendation(self, item, n_items = 10):
        """
        
        Item-Item based recommendation.

        Parameters
        ----------
        item : integer
            Item id of the item to make the recommendations from.
        n_items : integer, optional
            Number of items to recommend. The default is 10.

        Returns
        -------
        None.

        """
        
        assert ((item >= min(self.ratings_mat.columns.values))&(item <= max(self.ratings_mat.columns.values))),"Item does not exist"
        assert (n_items > 0),"Negative n_items value"
        assert (n_items <= (len(self.ratings_mat.columns.values)-1)),"Number of items to recommend greater than total items"          
                
        # print(self.sim_matrix)
        
        top_i = pd.DataFrame(self.sim_matrix.loc[item].nlargest(n_items+1)[1:]) # Exclude first item, as it is self 
        top_i.columns = ['Similarity Score']
        
        print("\n\nTop {n_items} recommended items similar to item {item_id}:\n\n".format(n_items = n_items, item_id = item))
        print(top_i.to_markdown())        
    
    # ............ USER-ITEM CALCULATIONS .....................................
    
    def UserItemRecommendation(self, user, n_items = 10, past = True, top = True, bottom = True):
        """

        Takes cosine similarity item-item matrix and computes the likability score 
        of every unmarked item for the user.


        Parameters
        ----------
        user : integer
            The id of the user for whom we want to generate recommendations of items.
        n_items : integer, optional
            Number of items to recommend. The default is 10.
        past : bool, optional
            Whether to print already liked items. The default is True.
        top : bool, optional
            Whether to print the top items to recommend. The default is True.
        bottom : bool, optional
            Whether to print the top items to NOT recommend. The default is True.

        Returns
        -------
        top_items : Pandas dataframe
            Top items to recommend for the user.
        bottom_items : Pandas dataframe
            Bottom items to NOT recommend for the user.

        """
        
        assert ((user >= min(self.ratings_mat.index.values))&(user <= max(self.ratings_mat.index.values))),"User does not exist"
        assert (n_items > 0),"Negative n_items value"
        assert (n_items <= sum(self.ratings_mat.iloc[user] == 0)),"Number of items to recommend greater than user's unscored items"          
        
        # Get the items the user has liked
        known_user_likes = self.ratings_mat.iloc[user]
        known_user_likes = known_user_likes[known_user_likes != 0].index.values
        
        # Users likes for all items as a sparse vector.
        user_rating_vector = self.ratings_mat.iloc[user]
        
        # Calculate the score.
        # score = self.sim_matrix.dot(user_rating_vector).div(self.sim_matrix.sum(axis=1)) # <-- Avoid. Yields inf values
        score = self.sim_matrix.dot(user_rating_vector)
        
        # Remove the known likes from the recommendation.
        score = score.drop(known_user_likes)
        
        score = pd.DataFrame(score, columns = ['Likability Score'])
        
        #score = score.replace([np.inf, -np.inf], np.nan)
        
        top_items = score.sort_values(['Likability Score'], ascending = False).head(n_items)
        bottom_items = score.sort_values(['Likability Score']).head(n_items)
        
        
        # Print the known likes and the top 10 recommendations
        
        if past == True:
            print("\nUser {id} has scored the following {num_items} items:\n\n".format(id = user, num_items = len(known_user_likes)),known_user_likes)
        if top == True:
            print("\n\n.....................\n\n\nTop 10 items to recommend user {id}:\n\n".format(id = user)) 
            print(top_items.to_markdown())
        if bottom == True:
            print("\n\n.....................\n\n\nTop 10 items to NOT recommend user {id}:\n\n".format(id = user)) 
            print(bottom_items.to_markdown())
    
        return top_items, bottom_items






# ............  TRY RECOMMENDER   .............................................





sfix = Recommender(ratings_matrix)

sfix.ItemBasedRecommendation(item = 20)

top_recommendations, bottom_recommendations = sfix.UserItemRecommendation(user = 5)


# Test cases:

sfix.ItemBasedRecommendation(item = -20)
sfix.ItemBasedRecommendation(item = 3, n_items = - 10)
sfix.ItemBasedRecommendation(item = 3, n_items = 10000)

top_recommendations, bottom_recommendations = sfix.UserItemRecommendation(user = 85000)
top_recommendations, bottom_recommendations = sfix.UserItemRecommendation(user = 5, n_items = -5)
top_recommendations, bottom_recommendations = sfix.UserItemRecommendation(user = 5, n_items = 4995)


