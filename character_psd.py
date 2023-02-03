
from multiprocessing.dummy import Array
from PIL import Image
from numpy import character
from pip import main
import psd_tools
import os

class CharacterPsd:

    def __init__(self,psd_file_path) -> None:

        if not os.path.exists( psd_file_path ) :
            raise CharacterPsdException("指定されたパスが存在しません。")
        
        # psd 読み込み
        self.name = os.path.splitext(os.path.basename( psd_file_path ))[0]
        self.psd = psd_tools.PSDImage.open(psd_file_path)
        self.size = [self.psd.numpy().shape[1],self.psd.numpy().shape[0]]
        # レイヤーを保存
        self.groups = []
        
        count = 0
        for layer in self.psd:
            if layer.is_group() :
                group = CharacterLayerGroup(layer,CharacterGroupNumber(count))
                self.groups.append(group)
                count += 1
            pass
    
    def export(self) -> Array :

        character_images = {}
        character_layer_counters = { -1 : None }
        main_counter = None

        for i in range(len(self.groups)) :
            counter = CharacterLayerCounter( self.groups[i].layer_length() , character_layer_counters[i-1] )
            character_layer_counters[i] = counter
            main_counter = counter
        character_layer_counters.pop(-1)

        while not main_counter.is_max():
            
            image = Image.new("RGBA",self.size)
            image_name = ""

            for i in range(len(self.groups)) :
                canvas_image = Image.new("RGBA",self.size)
                character_layer = self.groups[i].get_layer(character_layer_counters[i].get_count())

                image_name += character_layer.get_layer_name() + "_"

                layer = character_layer.layer
                layer_image = layer.composite()
                canvas_image.paste(layer_image,layer.offset)
                image = Image.alpha_composite( image , canvas_image )
            image_name += ".png"

            print(image_name + " exported(" + str(main_counter.all_get_count()) + "/" + str(main_counter.all_get_max_count()) + ")" )
            character_images[image_name] = image
            main_counter.count_up()
		
        return character_images

    def export_save(self,directory_path):

        character_layer_counters = { -1 : None }
        main_counter = None

        for i in range(len(self.groups)) :
            counter = CharacterLayerCounter( self.groups[i].layer_length() , character_layer_counters[i-1] )
            character_layer_counters[i] = counter
            main_counter = counter
        character_layer_counters.pop(-1)

        while not main_counter.is_max():
            
            image = Image.new("RGBA",self.size)
            image_name = ""
            count_data = main_counter.count_data()
            count_data.reverse()

            for i in range(len(self.groups)) :
                canvas_image = Image.new("RGBA",self.size)
                character_layer = self.groups[i].get_layer(character_layer_counters[i].get_count())

                image_name += character_layer.get_layer_name() + "_"

                layer = character_layer.layer
                layer_image = layer.composite()
                canvas_image.paste(layer_image,layer.offset)
                image = Image.alpha_composite( image , canvas_image )
            image_name += ".png"
            image_name = "".join(['{:0=2}'.format(_) for _ in count_data]) + "_" + image_name
            print(image_name + " exported(" + str(main_counter.all_get_count()) + "/" + str(main_counter.all_get_max_count()) + ")" )
            
            #------------save--------------
            image.save("%s/%s.png" % ( directory_path , image_name ) )

            main_counter.count_up()

    def export_group_save(self,directory_path):
        
        for group in self.groups:
            group_dic_path = directory_path + "/" + group.get_group_name()
            if not os.path.exists( group_dic_path ):
                os.makedirs( group_dic_path )
            
            for i in range(0,group.layer_length()):
                canvas_image = Image.new("RGBA",self.size)
                part_layer = group.get_layer(i)
                layer_path = group_dic_path + "/" + part_layer.get_layer_name() + ".png"

                print( group_dic_path + "/" + part_layer.get_layer_name() )

                layer = part_layer.layer
                layer_image = layer.composite()
                canvas_image.paste(layer_image,layer.offset)
                canvas_image.save(layer_path)

class CharacterLayerGroup:

    def __init__(self , group , group_number) -> None:

        self.group = group
        self.group_number = group_number
        self.layers = []
        count = 0
        
        for layer in group:
            character_layer = CharacterLayer(layer,CharacterLayerNumber(count))
            self.layers.append(character_layer)
            count += 1

    def get_layer(self,number):
        return self.layers[number]

    def layer_length(self):
        return len(self.layers)

    def get_group_name(self):
        return "%03d_"%self.group_number.get_group_number() + self.group.name

class CharacterLayer:
    def __init__(self,layer,layer_number) -> None:
        self.layer = layer
        self.layer_number = layer_number

        self.layer.visible = True
    
    def get_layer_name(self):
        return "%03d_"%self.layer_number.get_layer_number() + self.layer.name

class CharacterGroupNumber:
    def __init__(self,number) -> None:
        self.group_number = number
    def get_group_number(self):
        return self.group_number

class CharacterLayerNumber:
    def __init__(self,number) -> None:
        self.layer_number = number
    def get_layer_number(self):
        return self.layer_number

class CharacterLayerCounter:
    def __init__( self , max , counter = None ) -> None:
        self.max = max
        self.count = 0
        self.next_counter = counter
    
    def get_count(self):
        return self.count

    def all_get_count( self , before_max = 1 ):
        if self.next_counter != None:
            return self.count * before_max + self.next_counter.all_get_count(self.max * before_max)
        else:
            return self.count * before_max + 1

    def all_get_max_count( self , before_max = 1 ):
        if self.next_counter != None:
            return self.max * before_max + self.next_counter.all_get_max_count(self.max * before_max)
        else:
            return self.max * before_max

    def count_up(self):
        if self.count != self.max:
            self.count += 1
        if self.count == self.max and self.next_counter != None :
            self.count = 0
            self.next_counter.count_up()

    def is_max(self):
        if self.next_counter != None :
            return self.next_counter.is_max()
        else:
            return self.count == self.max

    def count_data(self) -> Array:
        if self.next_counter != None :
            return [self.count] + self.next_counter.count_data()
        else:
            return [self.count]

    def count_max_data(self) -> Array:
        if self.next_counter != None :
            return [self.max] + self.next_counter.count_max_data()
        else:
            return [self.max]

class CharacterPsdException(Exception):
    pass