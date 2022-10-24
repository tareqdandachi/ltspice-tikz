import js
from js import document, FileReader, localStorage
from pyodide import create_proxy

from file_interface import parser
from exporter import HTML_Canvas_Exporter
from symbols import WebSymbolStash
from circuit import CircuitSchematic
from styling import Color

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")
CANVAS = HTML_Canvas_Exporter(ctx)

tooltips_canvas = js.tooltips_canvas

def set_running():
    pass # TODO: change this to a visual thing.
	# document.getElementById("status").innerHTML = 'Python loaded and running ...'
 
def click_canvas(event):
    
    selected_element = None
    
    for elem in document.schematic.geometries:
        
        if elem.is_inside(event.x, event.y):
            print("YAY")
            selected_element = elem
            
    print(selected_element)
    
    if selected_element:
        document.element_selected = {"x": selected_element.pt1[0], "y": selected_element.pt1[1], "x2": selected_element.pt2[0], "y2": selected_element.pt2[1]}
    else:
        document.element_selected = None
        
    js.tooltip_redraw(event)
    
 
def read_complete(event):
    # event is ProgressEvent

    content = document.getElementById("source_code_value")
    content.innerText = event.target.result
    
    document.schematic = parser(event.target.result, symbolstash=WebSymbolStash(localStorage, "symbols", symbol_missing_method))
    
    redraw(None)

def get_color_target():
    
    return js.toColorObject().lower().split(",")

def redraw(event):
    # TODO: make this more efficient by caching schematic
    
    canvas =  document.getElementById("canvas")
    ctx = canvas.getContext("2d")
    
    ctx.save()
    ctx.setTransform(1,0,0,1,0,0)
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.restore()
    
    target, color = get_color_target(), Color(js.colorPicker.color.hexString)
    
    if "schematic" in target:
        document.schematic.color = color
    
    if "background" in target:
        document.schematic.backgroundColor = color
        
    if "text" in target:
        document.schematic.commentColor = color
        document.schematic.commandColor = color
        
    if "comment" in target:
        document.schematic.commentColor = color
        
    if "command" in target:
        document.schematic.commandColor = color
    
    if document.schematic:
        CANVAS.draw(document.schematic)

async def process_file(x):
    fileList = document.getElementById('file-upload').files

    for f in fileList:

        reader = FileReader.new()

        onload_event = create_proxy(read_complete)

        reader.onload = onload_event

        reader.readAsText(f)

        return

def symbol_missing_method(title, msg):
    js.missing_symbol_error()
    print("-----", title, "-----", msg)

def add_symbol_from_source(event):
    stash = WebSymbolStash(localStorage, "symbols", symbol_missing_method)
    stash.add(event.target.filename.replace(".asy", ""), event.target.result)

def add_symbols(event):
    fileList = document.getElementById('symbol-upload').files
    
    for f in fileList:
        
        reader = FileReader.new()
        
        onload_event = create_proxy(add_symbol_from_source)
        
        reader.filename = f.name
        
        reader.onload = onload_event
        
        reader.readAsText(f)

def main():
    
    document.schematic = CircuitSchematic(WebSymbolStash(localStorage, "symbols", symbol_missing_method))
    
    set_running()
    # Create a Python proxy for the callback function
    file_event = create_proxy(process_file)
    symbol_event = create_proxy(add_symbols)
    redraw_event = create_proxy(redraw)
    ui_click = create_proxy(click_canvas)

    # Set the listener to the callback
    e = document.getElementById("file-upload")
    e.addEventListener("change", file_event, False)
    
    e = document.getElementById("symbol-upload")
    e.addEventListener("change", symbol_event, False)
    
    canvas.addEventListener("redraw", redraw_event, False)
    tooltips_canvas.addEventListener("ui_click", ui_click, False)

main()