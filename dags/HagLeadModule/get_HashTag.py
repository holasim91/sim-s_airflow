import re
import pandas as pd

class Extract_HashTag:
    
    def __init__(self, df):
        self.df = df
        
        
    def find_tags(self):
        
        df = self.df
        df['tags'] = [0]*len(df)
        
        def make_tags(text):
            if type(text) == str:
                return re.findall('#\w+', text)
            else:
                return []
                
        df['tags'] = df['text'].map(lambda x: make_tags(x)) + df['hash_tag'].map(lambda x: make_tags(x))
        
        result = []
        
        def tag():
            for i in range(len(df)):
                result.extend(df.loc[i, 'tags'])
            return result
        
        
        tag_df = pd.DataFrame(tag())
        
        

        return tag_df
    
        
