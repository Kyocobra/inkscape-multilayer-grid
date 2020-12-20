import os
import inkex
import math
from lxml import etree
from copy import deepcopy

class MultilayerGrid(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)

    # this is required for receiving .inx input
    def add_arguments(self, pars):
        # add param "name"s from .inx file
        # must have double "--" (not sure why)
        pars.add_argument("--rows", type=int) 
        pars.add_argument("--cols", type=int)
        pars.add_argument("--max_layers", type=int)
        pars.add_argument("--delete_source", type=bool)
     
    # automatically runs after add_arguments
    def effect(self):
        # import row and col from .inx window
        rows = self.options.rows
        cols = self.options.cols
        max_layers = self.options.max_layers
        delete_source = self.options.max_layers
        
        layer = self.svg.get_current_layer()
                
        selection = self.svg.get_selected()
        n_selected = len(selection)
        if not n_selected:
            inkex.errormsg("Please select at least one object")
        
        # side note: bounding_box() outputs mm!
        # bbox top left location *almost* same as UI; maybe small page margin?    

        # get dimensions of page
        page_bb = self.svg.get_page_bbox()
        page_width, page_height = self.get_dimensions(page_bb)
        
        # get dimensions of reference object (first in selection)
        # "selection" is an ordered dictionary, grab first element
        sample_bb = next(iter(selection)).bounding_box()
        obj_width, obj_height = self.get_dimensions(sample_bb)
        
        # distance from edge of page to center of periphery objects
        margin_width = (page_width - obj_width * (cols - 1))/2
        margin_height = (page_height - obj_height * (rows - 1))/2
        
        # calculate grid center points for rows and cols
        y_points = []
        for r in range(rows):
            y_points.append(margin_height + r * obj_height)
        
        x_points = []
        for c in range(cols):
            x_points.append(margin_width + c * obj_width)
                            
        layer_count = 0
        
        count, r, c = 0, 0, 0 # current element, current row, current col
        for elem in selection:
        
            if count == n_selected or count == rows*cols*max_layers:
                break
        
            if count % (rows*cols) == 0:
                layer_count += 1
                layer = self.create_layer(layer_count)
                self.msg('NEW LAYER! #%s' % layer_count)
        
            elem_copy = deepcopy(elem)
            
            # Append to new layer
            layer.append(elem_copy)
            
            # self.msg(n_selected)
            
            self.msg('row, col, count: (%d %d %d)' % (r, c, count))
            
            x_loc = x_points[c] # column (x location)
            y_loc = y_points[r] # row (y location)
            self.msg('Target: (%.2f, %.2f)' % (x_loc, y_loc))
            
            bbox = elem_copy.bounding_box() # money maker
            x, y = bbox.center
            self.msg('Current: (%.2f, %.2f)' % (bbox.center_x, bbox.center_y))
            
            # calculate delta x, delta y, and translate object
            translate_cmd = 'translate(%.2f, %.2f)' % (x_loc - x, y_loc - y)
            elem_copy.set('transform', translate_cmd)
            self.msg(translate_cmd)
            
            new_bbox = elem_copy.bounding_box() # update bounding box
            self.msg('New: (%.2f, %.2f)' % (new_bbox.center_x, new_bbox.center_y))
            self.msg('---------------------------------')
            
            # Delete source element?
            if(delete_source == True):
                elem.getparent().remove(elem)  
            
            count += 1 # new element placed
            
            # set next col and row
            c = count % cols
            r = math.floor(count / cols) % rows
        
    def create_layer(self, layer_count):
        svg = self.document.xpath('//svg:svg',namespaces=inkex.NSS)[0]
        
        layer_width  = svg.unittouu(svg.get('width'))
        layer_height  = svg.unittouu(svg.get('height'))
            
        layer_name = str(layer_count)    
        
        # Create layer element
        layer = etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), '%s' % (layer_name))
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        
        return layer
        
    def get_dimensions(self, bbox):
        min_vect = bbox.minimum # upper left
        max_vect = bbox.maximum # bottom right

        x1 = min_vect.x
        x2 = max_vect.x
        width = x2 - x1

        y1 = min_vect.y
        y2 = max_vect.y
        height = y2 - y1
            
        return width, height

if __name__ == '__main__':
    MultilayerGrid().run()