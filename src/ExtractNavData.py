'''
Created on Feb 9, 2020

@author: waxcruz
'''


from pathlib  import Path


def processGeoNames(geoFile):
    # read GIS Geo Names (http://download.geonames.org/export/dump/) and extract elements for WaxNav database
    fileNameGeoNames = geoFile+"/US.txt"
    fileNameGeoSQL = geoFile+"/geoSQLWithState.tsv"
    geoNamesFile = open(fileNameGeoNames, 'r', encoding='utf8')

    metersToFeet = 3.28084
    tab = '\t'
    locations = []
    # The main 'geoname' table has the following fields :
    # ---------------------------------------------------
    #  0. geonameid         : integer id of record in geonames database
    #  1. name              : name of geographical point (utf8) varchar(200)
    #  2. asciiname         : name of geographical point in plain ascii characters, varchar(200)
    #  3. alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
    #  4. latitude          : latitude in decimal degrees (wgs84)
    #  5. longitude         : longitude in decimal degrees (wgs84)
    #  6. feature class     : see http://www.geonames.org/export/codes.html, char(1)
    #  7. feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
    #  8. country code      : ISO-3166 2-letter country code, 2 characters
    #  9. cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
    # 10. admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
    # 11. admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
    # 12. admin3 code       : code for third level administrative division, varchar(20)
    # 13. admin4 code       : code for fourth level administrative division, varchar(20)
    # 14. population        : bigint (8 byte int) 
    # 15. elevation         : in meters, integer
    # 16. dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed 18 cgiar/ciat.
    # 17. timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
    # 18. modification date : date of last modification in yyyy-MM-dd format

    # feature classes:
    # A: country, state, region,...
    # H: stream, lake, ...
    # L: parks,area, ...
    # P: city, village,...
    # R: road, railroad 
    # S: spot, building, farm
    # T: mountain,hill,rock,... 
    # U: undersea
    # V: forest,heath,...

    for line in geoNamesFile:
        line = line.replace('"','')
        parts = line.split('\t')
        # convert elevation to feet
        if "" == parts[15]:
            elevation = 0
        else:
            elevation = float(parts[15])*metersToFeet
        # build tab separated output
        location = parts[1] + tab   # name
        location += parts[4] + tab  #latitude
        location += parts[5] + tab  #longitude
        location += parts[6] + tab  #feature class
        location += str(elevation) + tab
        if "US" == parts[8]:
            location += parts[10] + '\n' #State
        else:
            location += "??"
            print("Not USA state")
        locations.append(location)
    geoNamesFile.close()
    # write locations to file
    with open(fileNameGeoSQL, 'w', encoding='utf8') as geoNamesFormattedForSQL_File:
        geoNamesFormattedForSQL_File.writelines(locations)
    
    print("# of locations is",len(locations))
    return
#===============================================================================
# Main 
#===============================================================================
#
#
#

home = str(Path.home())+"/Developer/WaxNavGeoNames/US"
#
# retrieve AHNowData as counts and events
#
processGeoNames(home)


print("Finished Where2Look backend processing")
