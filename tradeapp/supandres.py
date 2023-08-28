import numpy as np

def sup_res(df):
    # Create two functions to calculate if a level is SUPPORT or a RESISTANCE level through fractal identification
    def is_Suppport_Level(df, i):
        support = df['low'][i] < df['low'][i - 1] and df['low'][i] < df['low'][i + 1] and df['low'][i + 1] < df['low'][i + 2] and df['low'][i - 1] < df['low'][i - 2]
        return support


    def is_Resistance_Level(df, i):
        resistance = df['high'][i] > df['high'][i - 1] and df['high'][i] > df['high'][i + 1] and df['high'][i + 1] > df['high'][i + 2] and df['high'][i - 1] > df['high'][i - 2]
        return resistance

    # Creating a list and feeding it the identified support and resistance levels via the Support and Resistance functions
    levels = []
    level_types = []
    for i in range(2, df.shape[0] - 2):

        if is_Suppport_Level(df, i):
            levels.append((i, df['low'][i].round(2)))
            level_types.append('Support')

        elif is_Resistance_Level(df, i):
            levels.append((i, df['high'][i].round(2)))
            level_types.append('Resistance')

        # Clean noise in data by discarding a level if it is near another
        # (i.e. if distance to the next level is less than the average candle size for any given day - this will give a rough estimate on volatility)
    mean = np.mean(df['high'] - df['low'])

    # This function, given a price value, returns True or False depending on if it is too near to some previously discovered key level.
    def distance_from_mean(level):
        return np.sum([abs(level - y) < mean for y in levels]) == 0

    # Optimizing the analysis by adjusting the data and eliminating the noise from volatility that is causing multiple levels to show/overlapp
    levels = []
    level_types = []
    for i in range(2, df.shape[0] - 2):

        if is_Suppport_Level(df, i):
            level = df['low'][i].round(2)

            if distance_from_mean(level):
                levels.append((i, level))
                level_types.append('Support')

        elif is_Resistance_Level(df, i):
            level = df['high'][i].round(2)

            if distance_from_mean(level):
                levels.append((i, level))
                level_types.append('Resistance')
    
    return levels

