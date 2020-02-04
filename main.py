import requests
import json
import pandas as pd
import numpy as np
import re
from argparse import ArgumentParser
from src.variab import genders_csv
from src.variab import regions
from src.variab import books
from src.functionsGoT import cleanGender
from src.functionsGoT import apiToDf
from src.functionsGoT import regionName


def death_house(house,book, dead,characters_DF):

    for libro in books.items():
        if libro[0] == str(book):
            titulo=libro[1]
    
    numero_muertos = dead.loc[(dead['house']==house) & (dead['Book of Death']==str(book))].shape[0]
    gente_casa = characters_DF[(characters_DF['house']==house)].shape[0]
    porc_muertes = int((numero_muertos/gente_casa)*100)
    
    return f'The {house} has {porc_muertes}% of the deaths in "{titulo}" book'

def parser():
    
    parser = ArgumentParser(description="Porcentaje de muertos por casa en cada libro")
    
    parser.add_argument("house",type=str, nargs=1,help='Introducir una casa de GoT')
    parser.add_argument("book",type=int, nargs=1, help='Introducir el numero del libro que quieras')

    args = parser.parse_args()
    house = args.house
    book = args.book
    
    return house[0], book[0]

def main():
    house, book = parser()
    #csv characters
    characters_csv = pd.read_csv('src/character-deaths.csv')
    characters_csv = characters_csv[['Name', 'Book of Death', 'Gender']]
    characters_csv.Gender = cleanGender(characters_csv.Gender,genders_csv)
    characters_csv['Book of Death']=characters_csv['Book of Death'].fillna(0).astype(int).astype(str)
    #API characters
    characters_df = apiToDf("https://api.got.show/api/book/characters")
    characters_df = characters_df[['name','gender', 'house', 'alive']].rename(columns={'name':'Name','gender':'Gender'})
    #DF characters
    characters_DF = pd.merge_ordered(characters_df,characters_csv, on=['Name','Gender'])
    characters_DF = characters_DF.fillna('-')
    characters_DF['house'] = characters_DF['house'].replace(regex={r'(&apos;)':"'",r'(\[\d\])':''})
    #DF houses
    houses_DF = apiToDf('https://api.got.show/api/book/houses')
    houses_DF = houses_DF[['name','region','overlords']]
    houses_DF['region'] = houses_DF['region'].fillna('Unknown')
    houses_DF['region'] = regionName(houses_DF['region'])

    dead = characters_DF[(characters_DF['alive']!=True) & (characters_DF['Book of Death']!=('-'))]
    print(death_house(house,book,dead,characters_DF))


if __name__=='__main__':
    
     main()
        

