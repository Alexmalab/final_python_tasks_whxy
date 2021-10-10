import io
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import PIL



def world_map():
    data = pd.read_json('cpi_bing.json')
    data_transposed = data.T
    # data_transposed.index.name = 'country'
    world = gpd.read_file('map/World_Map.shp')
    # print(data_transposed)
    #replace country name
    world.replace('Central African Republic','Middle Africa',inplace=True)
    world.replace('Iran (Islamic Republic of)','Iran',inplace=True)
    world.replace('Congo','Congo (Brazzaville)',inplace=True)
    world.replace('Libyan Arab Jamahiriya','Libya',inplace=True)
    world.replace('Syrian Arab Republic','Syria',inplace=True)
    world.replace('United Republic of Tanzania','Tanzania',inplace=True)
    world.replace('Bangladesh','bengali',inplace=True)
    world.replace('Micronesia, Federated States of','Micronesia (Federated States of).',inplace=True)
    world.replace('Netherlands Antilles','Curaçao',inplace=True)
    world.replace('Republic of Moldova','Moldova',inplace=True)
    world.replace('Brunei Darussalam','Brunei',inplace=True)
    world.replace('Fiji','Fiji Islands',inplace=True)
    world.replace('Swaziland','Eswatini',inplace=True)
    world.replace('Bosnia and Herzegovina','Bosnia',inplace=True)
    world.replace('''Cote d'Ivoire''','''Côte d’Ivoire''',inplace=True)
    world.replace('Burma','Myanmar',inplace=True)
    world.replace('Romania','Romanian',inplace=True)
    world.replace('''Lao People's Democratic Republic''','Laos',inplace=True)
    world.replace('Saint Martin','Sint Maarten of the Netherlands',inplace=True)
    world.replace('Viet Nam','Vietnam',inplace=True)
    world.replace('United Arab Emirates','U.A.E',inplace=True)
    world.replace('Korea, Republic of','Korea',inplace=True)
    world.replace('The former Yugoslav Republic of Macedonia','Macedonia',inplace=True)
    # print(world.head(3).to_string())
    #CHECKING
    # for index,row in data_transposed.iterrows():
    #     if index not in world['NAME'].to_list():
    #         print(index+':is not in the list')
    #     else:
    #         pass
    #merging data with world geopandas frame
    merge = world.join(data_transposed,on='NAME',how='right')
    # print(merge.head(3).to_string())
    image_frames = []
    for dates in merge.columns.to_list()[2:63]:#循环62年的数据
    #plot
        ax = merge.plot(column = dates,
                        cmap = 'bwr',
                        # cmap = 'OrRd',
                        figsize = (14,14),
                        legend = True,
                        scheme = 'user_defined',
                        classification_kwds={'bins':[-50,-20,-10,-5,0,5,10,50,100,500,10000,50000]},
                        edgecolor = 'black',
                        linewidth = 0.4)
        ax.set_title('CPI of World Countries in '+str(dates),fontdict = {'fontsize':20},pad = 12.5)
        ax.get_legend().set_bbox_to_anchor((0.18,0.6))
        ax.get_legend().set_title('CPI Unit:  %')
        ax.set_axis_off()
        ##create each img
        img = ax.get_figure()
        f = io.BytesIO()
        img.savefig(f,format = 'png',bbox_inches = 'tight')
        f.seek(0)
        image_frames.append(PIL.Image.open(f))
        # plt.show()
    #*create and save a GIF file
    image_frames[0].save('Dynamic CPI Map2.gif',format='GIF',
                         append_images = image_frames[1:],
                         save_all = True,duration = 300,
                         loop = 3)
    f.close()
    print("World Map Generate success")

def line_chart():
    data = pd.read_json('cpi.json')
    # print(data)
    data.astype(float)
    ax = data.plot(y = ['中国','美国','日本','英国'],use_index = True,figsize = (10,8),marker='.')
    ax.set_title('中美日英四国1960到2021年CPI变化图')
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.show()

if __name__ == '__main__':
    try:
        #generate a line chart
        # line_chart()
        #generate a dynamic world map
        world_map()
    except Exception as e:
        print(e)